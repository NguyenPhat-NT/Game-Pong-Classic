# graphics.py

import pygame
import config

pygame.font.init()
SCORE_FONT = pygame.font.Font(None, 74)
MESSAGE_FONT = pygame.font.Font(None, 50)
SUB_MESSAGE_FONT = pygame.font.Font(None, 30) # <-- Font nhỏ hơn cho hướng dẫn

def draw_game_state(screen, state):
    """
    Vẽ toàn bộ trạng thái game lên màn hình.
    Args:
        screen: Đối tượng screen của pygame.
        state (dict): Dictionary chứa thông tin trạng thái game từ server.
    """
    screen.fill(config.BLACK)

    if not state:
        return

    status = state.get("Status")

    if status == "Waiting":
        # --- Màn hình chờ mới ---
        message_text = MESSAGE_FONT.render("Waiting for players...", True, config.WHITE)
        message_rect = message_text.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 - 20))
        
        sub_text = SUB_MESSAGE_FONT.render("Controls: UP / DOWN Arrow Keys", True, config.WHITE)
        sub_rect = sub_text.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 + 30))

        screen.blit(message_text, message_rect)
        screen.blit(sub_text, sub_rect)

    elif status == "Ended":
        # --- Màn hình kết thúc mới ---
        message = state.get("Message", "")
        message_text = MESSAGE_FONT.render(message, True, config.WHITE)
        message_rect = message_text.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 - 20))

        sub_text = SUB_MESSAGE_FONT.render("Click the button to play again!", True, config.WHITE)
        sub_rect = sub_text.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 + 30))

        screen.blit(message_text, message_rect)
        screen.blit(sub_text, sub_rect)

    elif status == "PLAYING":
        # --- Vẽ trạng thái đang chơi ---
        player1_y = state.get("Player1Y", config.SCREEN_HEIGHT / 2)
        player2_y = state.get("Player2Y", config.SCREEN_HEIGHT / 2)
        
        player1_rect = pygame.Rect(
            config.PADDLE_PADDING,
            player1_y,
            config.PADDLE_WIDTH,
            config.PADDLE_HEIGHT
        )
        pygame.draw.rect(screen, config.WHITE, player1_rect)

        player2_rect = pygame.Rect(
            config.SCREEN_WIDTH - config.PADDLE_PADDING - config.PADDLE_WIDTH,
            player2_y,
            config.PADDLE_WIDTH,
            config.PADDLE_HEIGHT
        )
        pygame.draw.rect(screen, config.WHITE, player2_rect)

        # Vẽ quả bóng
        pygame.draw.circle(
            screen,
            config.WHITE,
            (state.get("BallX", config.SCREEN_WIDTH / 2), state.get("BallY", config.SCREEN_HEIGHT / 2)),
            config.BALL_RADIUS
        )

        # Vẽ điểm số
        score1_text = SCORE_FONT.render(str(state.get("Score1", 0)), True, config.WHITE)
        screen.blit(score1_text, (config.SCREEN_WIDTH / 4, 20))

        score2_text = SCORE_FONT.render(str(state.get("Score2", 0)), True, config.WHITE)
        screen.blit(score2_text, (config.SCREEN_WIDTH * 3 / 4 - score2_text.get_width(), 20))

# --- HÀM MỚI ĐỂ VẼ NÚT BẤM ---
def draw_play_again_button(screen):
    """Vẽ nút Play Again và trả về Rect của nó."""
    button_rect = pygame.Rect(0, 0, 200, 50)
    button_rect.center = (config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 + 100)
    
    # Vẽ viền nút với góc bo tròn
    pygame.draw.rect(screen, config.WHITE, button_rect, 2, 5)
    
    text = SUB_MESSAGE_FONT.render("Play Again", True, config.WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    
    return button_rect