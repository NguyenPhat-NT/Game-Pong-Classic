// GameServer.cs (Đã sửa cho việc nhấn giữ)
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using PongServer.Models;

namespace PongServer
{
    public class GameServer
    {
        private readonly TcpListener listener;
        private readonly GameState state = new GameState();
        private readonly object stateLock = new object();
        private readonly List<ClientHandler> clients = new List<ClientHandler>();
        private readonly List<StreamWriter> writers = new List<StreamWriter>();
        private const int PaddleSpeed = 7; // Tốc độ di chuyển của paddle

        public GameServer()
        {
            listener = new TcpListener(IPAddress.Any, Config.Port);
            ResetGameForWaiting();
        }

          private void ResetGameForWaiting()
        {
            state.Status = "Waiting";
            state.Message = "Waiting for players...";
            state.Score1 = 0;
            state.Score2 = 0;
            state.Player1Y = (Config.ScreenHeight - Config.PaddleHeight) / 2;
            state.Player2Y = (Config.ScreenHeight - Config.PaddleHeight) / 2;
        }
        private void ResetGameForPlaying()
        {
            Console.WriteLine("Both players ready. Resetting the game!");
            state.Status = "PLAYING";
            state.Message = "";
            state.Score1 = 0;
            state.Score2 = 0;
            state.Player1Y = (Config.ScreenHeight - Config.PaddleHeight) / 2;
            state.Player2Y = (Config.ScreenHeight - Config.PaddleHeight) / 2;
            GameLogic.ResetBall(state);

            // Reset trạng thái của các handler để không bị lặp lại việc reset game
            foreach (var client in clients)
            {
                client.ResetPlayAgainStatus();
            }
        }
        public async Task StartAsync()
        {
            listener.Start();
            Console.WriteLine($"Server started on port {Config.Port}.");

            _ = AcceptClientsAsync();

            var interval = TimeSpan.FromSeconds(1.0 / Config.TickRate);
            while (true)
            {
                var loopStart = DateTime.UtcNow;

                lock (stateLock)
                {
                    if (state.Status == "Ended")
                    {
                        // Chỉ kiểm tra khi có đủ 2 người chơi kết nối
                        if (clients.Count(c => c.IsConnected) >= 2)
                        {
                            // Nếu tất cả người chơi đều muốn chơi lại
                            if (clients.All(c => c.WantsToPlayAgain))
                            {
                                ResetGameForPlaying();
                            }
                        }
                    }
                    else if (state.Status == "Waiting" && clients.Count(c => c.IsConnected) >= 2)
                    {
                        Console.WriteLine("Two players connected. Starting game!");
                        state.Status = "PLAYING";
                        state.Message = "";
                        GameLogic.ResetBall(state);
                    }

                    if (state.Status == "PLAYING")
                    {
                        // Lấy hướng di chuyển từ ClientHandlers
                        int p1Dir = clients.Count > 0 ? clients[0].Direction : 0;
                        int p2Dir = clients.Count > 1 ? clients[1].Direction : 0;

                        // Cập nhật vị trí paddles và bóng
                        GameLogic.UpdatePaddlePosition(state, p1Dir, p2Dir, PaddleSpeed);
                        GameLogic.UpdateBall(state);

                    }
                }

                await BroadcastStateAsync();

                var waitTime = interval - (DateTime.UtcNow - loopStart);
                if (waitTime > TimeSpan.Zero)
                {
                    await Task.Delay(waitTime);
                }
            }
        }

        private async Task AcceptClientsAsync()
        {
            while (clients.Count < 2)
            {
                TcpClient tcpClient = await listener.AcceptTcpClientAsync();
                int playerNumber = clients.Count + 1;
                Console.WriteLine($"Player {playerNumber} is connecting...");
                
                // ClientHandler giờ không cần truy cập GameState và lock nữa
                var handler = new ClientHandler(tcpClient, playerNumber);
                var writer = new StreamWriter(tcpClient.GetStream(), new UTF8Encoding(false)) { AutoFlush = true };

                lock (stateLock)
                {
                    clients.Add(handler);
                    writers.Add(writer);
                }

                _ = handler.ListenForCommandsAsync();
                Console.WriteLine($"Player {playerNumber} connected and handler started.");
            }
        }

        private async Task BroadcastStateAsync()
        {
            string jsonState;
            lock (stateLock)
            {
                jsonState = state.ToJson();
            }

            for (int i = writers.Count - 1; i >= 0; i--)
            {
                if (!clients[i].IsConnected)
                {   
                    Console.WriteLine($"Player {i + 1} has disconnected. Resetting game to waiting state.");
                    writers.RemoveAt(i);
                    lock (stateLock)
                    {
                        clients.RemoveAt(i);
                    ResetGameForWaiting(); }
                    continue;
                }
                
                try
                {
                    await writers[i].WriteLineAsync(jsonState);
                }
                catch { /* Client đã ngắt kết nối */ }
            }
        }
    }
}