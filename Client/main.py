# main.py

import pygame
import asyncio
import json
import sys
import config
import graphics
import os

async def main():
    """
    Hàm chính khởi tạo game, kết nối server và chạy vòng lặp chính.
    """
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Client")

    # --- KHỞI TẠO BIẾN CHO HIỆU ỨNG VÀ NÚT BẤM ---
    flash_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    flash_surface.set_alpha(100)
    flash_surface.fill((255, 255, 255))
    flash_timer = 0
    play_again_button_rect = None

    # --- NẠP CÁC FILE ÂM THANH VÀ NHẠC NỀN ---
    try:
        # Hiệu ứng âm thanh ngắn
        paddle_hit_sound = pygame.mixer.Sound(os.path.join("assets", "paddle_hit.wav"))
        wall_hit_sound = pygame.mixer.Sound(os.path.join("assets", "wall_hit.wav"))
        score_sound = pygame.mixer.Sound(os.path.join("assets", "score.mp3"))
        game_start_sound = pygame.mixer.Sound(os.path.join("assets", "game_start.ogg"))
        game_end_sound = pygame.mixer.Sound(os.path.join("assets", "game_end.wav"))
        
        # Nhạc nền chờ - Cập nhật thành .ogg
        pygame.mixer.music.load(os.path.join("assets", "waiting_music.ogg"))

    except pygame.error as e:
        print(f"Lỗi: không thể nạp file âm thanh hoặc nhạc. Hãy chắc chắn bạn có thư mục 'assets'. {e}")
        class DummySound:
            def play(self): pass
        paddle_hit_sound = wall_hit_sound = score_sound = game_start_sound = game_end_sound = DummySound()
    # -----------------------------

    # Khởi tạo trạng thái game
    current_state = {}
    previous_state = {}

    # --- KẾT NỐI TỚI SERVER ---
    try:
        print(f"Connecting to server at {config.SERVER_IP}:{config.SERVER_PORT}...")
        reader, writer = await asyncio.open_connection(config.SERVER_IP, config.SERVER_PORT)
        print("Connection successful!")
    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")
        screen.fill(config.BLACK)
        error_font = pygame.font.Font(None, 36)
        error_text = error_font.render("Connection Failed. Server not found.", True, config.WHITE)
        error_rect = error_text.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2))
        screen.blit(error_text, error_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

        # --- VÒNG LẶP CHÍNH CỦA GAME ---
    running = True
    while running:
        # --- XỬ LÝ INPUT TỪ NGƯỜI DÙNG ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Khi game đã kết thúc -> hiện nút PLAY AGAIN
                if current_state.get("Status") == "Ended":
                    if play_again_button_rect and play_again_button_rect.collidepoint(event.pos):
                        print("Sending PLAY_AGAIN command to server...")
                        writer.write("PLAY_AGAIN\n".encode())
                        current_state["Message"] = "Waiting for other player..."

                # Khi game đang ở trạng thái chờ -> hiện nút START
                elif current_state.get("Status") == "Waiting":
                    if start_button_rect and start_button_rect.collidepoint(event.pos):
                        print("Sending START command to server...")
                        writer.write("START\n".encode())
                        current_state["Message"] = "Waiting for other player..."
            
            # --- Điều khiển bàn ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    writer.write("MOVE_UP\n".encode())
                elif event.key == pygame.K_DOWN:
                    writer.write("MOVE_DOWN\n".encode())
            
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    writer.write("STOP\n".encode())
        
        await writer.drain()


        # --- NHẬN DỮ LIỆU TỪ SERVER ---
        try:
            data = await asyncio.wait_for(reader.readline(), timeout=0.001)
            
            if not data:
                print("Server closed the connection.")
                running = False
            else:
                current_state = json.loads(data.decode('utf-8-sig'))

                # --- LOGIC ÂM THANH & HIỆU ỨNG ---
                if previous_state:
                    current_status = current_state.get("Status")
                    previous_status = previous_state.get("Status")

                    if current_state.get("Score1") > previous_state.get("Score1", 0) or \
                       current_state.get("Score2") > previous_state.get("Score2", 0):
                        score_sound.play()

                    if current_state.get("BallVelocityY") != previous_state.get("BallVelocityY") or \
                       current_state.get("BallVelocityX") != previous_state.get("BallVelocityX"):
                        if current_status == "PLAYING":
                            if current_state.get("BallVelocityX") != previous_state.get("BallVelocityX"):
                                paddle_hit_sound.play()
                            else:
                                wall_hit_sound.play()
                            flash_timer = 3
                        
                    if current_status == "PLAYING" and previous_status != "PLAYING":
                        game_start_sound.play()
                        pygame.mixer.music.stop()
                    
                    if (current_status == "Ended" and previous_status != "Ended") or \
                       (current_status == "Waiting" and previous_status != "Waiting"):
                        if current_status == "Ended":
                           game_end_sound.play()
                        pygame.mixer.music.play(-1)

                previous_state = current_state.copy()

        except asyncio.TimeoutError:
            pass
        except Exception as e:
            print(f"An error occurred: {e}")
            running = False

        # --- CẬP NHẬT ĐỒ HỌA ---
        graphics.draw_game_state(screen, current_state)
        
        if current_state.get("Status") == "Ended":
            play_again_button_rect = graphics.draw_play_again_button(screen)

        if flash_timer > 0:
            screen.blit(flash_surface, (0, 0))
            flash_timer -= 1

        if current_state.get("Status") == "Waiting":
            start_button_rect = graphics.draw_start_button(screen)

            
        pygame.display.flip()
        
        await asyncio.sleep(0)

    # --- DỌN DẸP VÀ KẾT THÚC ---
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