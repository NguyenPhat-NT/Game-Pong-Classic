# main.py

import pygame
import asyncio
import json
import sys
import config
import graphics

async def main():
    """
    Hàm chính khởi tạo game, kết nối server và chạy vòng lặp chính.
    """
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Client")

    # Khởi tạo trạng thái rỗng ban đầu để vẽ màn hình chờ
    current_state = {}

    try:
        print(f"Connecting to server at {config.SERVER_IP}:{config.SERVER_PORT}...")
        reader, writer = await asyncio.open_connection(config.SERVER_IP, config.SERVER_PORT)
        print("Connection successful!")
    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")
        # Hiển thị thông báo lỗi trên cửa sổ pygame
        screen.fill(config.BLACK)
        error_font = pygame.font.Font(None, 36)
        error_text = error_font.render("Connection Failed. Server not found.", True, config.WHITE)
        error_rect = error_text.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2))
        screen.blit(error_text, error_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    running = True
    while running:
        # --- Xử lý Input từ người dùng (Luôn chạy để cửa sổ không bị treo) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    writer.write("MOVE_UP\n".encode())
                elif event.key == pygame.K_DOWN:
                    writer.write("MOVE_DOWN\n".encode())
            
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    writer.write("STOP\n".encode())
        
        # Gửi đi bất kỳ lệnh nào đang chờ
        await writer.drain()

        # --- Nhận trạng thái từ Server (Không chặn) ---
        try:
            # Chờ dữ liệu trong một khoảng thời gian rất ngắn (0.001s)
            # Nếu không có dữ liệu, nó sẽ ném ra TimeoutError và vòng lặp tiếp tục
            data = await asyncio.wait_for(reader.readline(), timeout=0.001)
            
            if not data:
                print("Server closed the connection.")
                running = False
            else:
                current_state = json.loads(data.decode('utf-8-sig'))

        except asyncio.TimeoutError:
            # Đây là trường hợp bình thường khi server chưa gửi dữ liệu.
            # Bỏ qua và tiếp tục vòng lặp để pygame được cập nhật.
            pass
        except Exception as e:
            print(f"An error occurred: {e}")
            running = False

        # --- Cập nhật đồ họa ---
        # Luôn vẽ trạng thái hiện tại, dù nó có được cập nhật ở vòng lặp này hay không
        graphics.draw_game_state(screen, current_state)
        pygame.display.flip()

        # --- Kiểm tra điều kiện kết thúc game ---
        if current_state.get("Status") == "Ended":
            print("Game has ended. Closing client.")
            pygame.time.wait(4000) # Giữ màn hình cuối trong 4 giây
            running = False
        
        # Nhường quyền điều khiển ngắn cho asyncio
        await asyncio.sleep(0)

    # Dọn dẹp và đóng kết nối
    print("Closing connection...")
    writer.close()
    await writer.wait_closed()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient closed by user.")