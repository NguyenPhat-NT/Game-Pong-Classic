// Config.cs
using System;

namespace PongServer
{
    /// <summary>
    /// Chứa các hằng số cấu hình cho game Pong Multi-Client server.
    /// </summary>
    public static class Config
    {
        /// <summary>Cổng lắng nghe kết nối.</summary>
        public const int Port = 5000;
        /// <summary>Số lần cập nhật trạng thái mỗi giây.</summary>
        public const int TickRate = 60;
        /// <summary>Chiều rộng màn hình (pixel).</summary>
        public const int ScreenWidth = 800;
        /// <summary>Chiều cao màn hình (pixel).</summary>
        public const int ScreenHeight = 600;
        /// <summary>Chiều rộng paddle (pixel).</summary>
        public const int PaddleWidth = 15;
        /// <summary>Chiều cao paddle (pixel).</summary>
        public const int PaddleHeight = 100;
        /// <summary>Bán kính quả bóng (pixel).</summary>
        public const int BallRadius = 10;
        /// <summary>Điểm đạt được để chiến thắng.</summary>
        public const int WinningScore = 5;
        public const int PaddlePadding = 30;
         
    }
}
