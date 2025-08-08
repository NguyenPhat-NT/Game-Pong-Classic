// GameLogic.cs (Đã sửa lỗi va chạm)
using System;
using PongServer.Models;

namespace PongServer
{
    public static class GameLogic
    {
        private const int InitialBallSpeed = 5;
        private static readonly Random RandomGen = new Random();

        // Cập nhật vị trí paddle (logic này sẽ được chuyển sang GameServer)
        public static void UpdatePaddlePosition(GameState state, int player1Dir, int player2Dir, int speed)
        {
            state.Player1Y += player1Dir * speed;
            state.Player2Y += player2Dir * speed;

            // Giới hạn di chuyển trong màn hình
            state.Player1Y = Math.Clamp(state.Player1Y, 0, Config.ScreenHeight - Config.PaddleHeight);
            state.Player2Y = Math.Clamp(state.Player2Y, 0, Config.ScreenHeight - Config.PaddleHeight);
        }
        
        public static void UpdateBall(GameState state)
        {
            if (state.Status != "PLAYING") return;

            // Di chuyển bóng
            state.BallX += state.BallVelocityX;
            state.BallY += state.BallVelocityY;

            // Va chạm tường trên/dưới
            if (state.BallY - Config.BallRadius <= 0 || state.BallY + Config.BallRadius >= Config.ScreenHeight)
            {
                state.BallVelocityY *= -1;
            }

            // === LOGIC VA CHẠM PADDLE ĐÃ SỬA LỖI ===
            // Vị trí mặt trong của paddle 1
            int paddle1InnerEdge = Config.PaddlePadding + Config.PaddleWidth;
            if (state.BallVelocityX < 0 && state.BallX - Config.BallRadius <= paddle1InnerEdge)
            {
                if (state.BallY > state.Player1Y && state.BallY < state.Player1Y + Config.PaddleHeight)
                {
                    state.BallVelocityX *= -1;
                }
            }

            // Vị trí mặt trong của paddle 2
            int paddle2InnerEdge = Config.ScreenWidth - Config.PaddlePadding - Config.PaddleWidth;
            if (state.BallVelocityX > 0 && state.BallX + Config.BallRadius >= paddle2InnerEdge)
            {
                if (state.BallY > state.Player2Y && state.BallY < state.Player2Y + Config.PaddleHeight)
                {
                    state.BallVelocityX *= -1;
                }
            }
            // === KẾT THÚC SỬA LỖI VA CHẠM ===

            // Ghi điểm
            if (state.BallX < 0)
            {
                state.Score2++;
                ResetBall(state);
            }
            else if (state.BallX > Config.ScreenWidth)
            {
                state.Score1++;
                ResetBall(state);
            }

            CheckForWinner(state);
        }

        private static void CheckForWinner(GameState state)
        {
            if (state.Score1 >= Config.WinningScore)
            {
                state.Status = "Ended";
                state.Message = "Player 1 wins!";
            }
            else if (state.Score2 >= Config.WinningScore)
            {
                state.Status = "Ended";
                state.Message = "Player 2 wins!";
            }
        }

        public static void ResetBall(GameState state)
        {
            state.BallX = Config.ScreenWidth / 2;
            state.BallY = Config.ScreenHeight / 2;
            state.BallVelocityX = (RandomGen.Next(0, 2) == 0 ? 1 : -1) * InitialBallSpeed;
            int velY;
            do { velY = RandomGen.Next(-InitialBallSpeed, InitialBallSpeed + 1); } while (velY == 0);
            state.BallVelocityY = velY;
        }
    }
}