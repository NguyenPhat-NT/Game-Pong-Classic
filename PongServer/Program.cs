// Program.cs
using System;
using System.Threading.Tasks;

namespace PongServer
{
    /// <summary>Điểm khởi động ứng dụng Pong Multi-Client Server.</summary>
    public class Program
    {
        /// <summary>Main entry cho ứng dụng.</summary>
        public static async Task Main(string[] args)
        {
            var server = new GameServer();
            Console.WriteLine("Server is starting...");
            await server.StartAsync();
        }
    }
}
