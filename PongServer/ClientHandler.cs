// ClientHandler.cs (Đã sửa cho việc nhấn giữ)
using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace PongServer
{
    public class ClientHandler
    {
        private readonly TcpClient client;
        private readonly int playerNumber;
        
        public bool IsConnected => client.Connected;
        
        /// <summary>
        /// Hướng di chuyển hiện tại: -1 (lên), 1 (xuống), 0 (đứng yên).
        /// public để GameServer có thể đọc được.
        /// </summary>
        public int Direction { get; private set; } = 0;
        public bool WantsToPlayAgain { get; private set; } = false;

        public ClientHandler(TcpClient client, int playerNumber)
        {
            this.client = client;
            this.playerNumber = playerNumber;
        }
         public void ResetPlayAgainStatus()
        {
            WantsToPlayAgain = false;
        }


        public async Task ListenForCommandsAsync()
        {
            try
            {
                using var reader = new StreamReader(client.GetStream(), Encoding.UTF8);
                while (IsConnected)
                {
                    var command = await reader.ReadLineAsync();
                    if (command == null) break;

                    switch (command)
                    {
                        case "MOVE_UP":
                            Direction = -1;
                            break;
                        case "MOVE_DOWN":
                            Direction = 1;
                            break;
                        case "STOP":
                            Direction = 0;
                            break;
                        case "PLAY_AGAIN":
                            Console.WriteLine($"Player {playerNumber} wants to play again.");
                            WantsToPlayAgain = true;
                            break;
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Player {playerNumber} connection error: {ex.Message}");
            }
            finally
            {
                Console.WriteLine($"Player {playerNumber} disconnected.");
                client.Close();
            }
        }
    }
}