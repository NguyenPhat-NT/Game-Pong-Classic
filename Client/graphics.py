# graphics.py

import pygame
import config

pygame.font.init()
SCORE_FONT = pygame.font.Font(None, 74)
MESSAGE_FONT = pygame.font.Font(None, 50)

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

    if status in ["Waiting", "Ended"]:
        message = state.get("Message", "")
        text = MESSAGE_FONT.render(message, True, config.WHITE)
        text_rect = text.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)

    elif status == "PLAYING":
        player1_y = state.get("Player1Y", config.SCREEN_HEIGHT / 2)
        player2_y = state.get("Player2Y", config.SCREEN_HEIGHT / 2)
        
        # Sửa lỗi chính tả: PaddlePadding -> PADDLE_PADDING
        player1_rect = pygame.Rect(
            config.PADDLE_PADDING, # Sửa ở đây
            player1_y,
            config.PADDLE_WIDTH,
            config.PADDLE_HEIGHT
        )
        pygame.draw.rect(screen, config.WHITE, player1_rect)

        # Sửa lỗi chính tả: PaddlePadding -> PADDLE_PADDING
        player2_rect = pygame.Rect(
            config.SCREEN_WIDTH - config.PADDLE_PADDING - config.PADDLE_WIDTH, # Sửa ở đây
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