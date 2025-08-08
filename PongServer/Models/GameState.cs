// Models/GameState.cs
using Newtonsoft.Json;

namespace PongServer.Models
{
    /// <summary>
    /// Trạng thái chung của trò chơi Pong.
    /// </summary>
    public class GameState
    {
        /// <summary>Vị trí dọc của paddle người chơi 1.</summary>
        public int Player1Y { get; set; }
        /// <summary>Vị trí dọc của paddle người chơi 2.</summary>
        public int Player2Y { get; set; }
        /// <summary>Tọa độ X của bóng.</summary>
        public int BallX { get; set; }
        /// <summary>Tọa độ Y của bóng.</summary>
        public int BallY { get; set; }
        /// <summary>Vận tốc theo trục X của bóng.</summary>
        public int BallVelocityX { get; set; }
        /// <summary>Vận tốc theo trục Y của bóng.</summary>
        public int BallVelocityY { get; set; }
        /// <summary>Điểm số của người chơi 1.</summary>
        public int Score1 { get; set; }
        /// <summary>Điểm số của người chơi 2.</summary>
        public int Score2 { get; set; }
        /// <summary>Trạng thái hiện tại của trò chơi ("Waiting", "PLAYING", "Ended").</summary>
        public string Status { get; set; }
        /// <summary>Thông điệp hiển thị (ví dụ "Player 1 wins!").</summary>
        public string Message { get; set; }

        /// <summary>
        /// Chuyển GameState thành chuỗi JSON.
        /// </summary>
        public string ToJson()
        {
            return JsonConvert.SerializeObject(this);
        }

        /// <summary>
        /// Tạo GameState từ chuỗi JSON.
        /// </summary>
        public static GameState FromJson(string json)
        {
            return JsonConvert.DeserializeObject<GameState>(json);
        }
    }
}
