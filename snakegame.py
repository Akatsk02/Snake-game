import pygame
import time
import random
import os

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)
BROWN = (139, 69, 19)

BG_LIGHT_GREEN = (170, 215, 81)
BG_DARK_GREEN = (162, 209, 73)

# Visual options used on the skin selection screen
SKINS = [
    {"name": "Blue", "head": (72, 117, 227), "body": (20, 30, 100)},
    {"name": "Red", "head": (255, 0, 0), "body": (139, 0, 0)},
    {"name": "Yellow", "head": (255, 255, 0), "body": (150, 150, 0)},
    {"name": "Purple", "head": (128, 0, 128), "body": (60, 0, 60)},
    {"name": "Green", "head": (0, 128, 0), "body": (0, 50, 0)},
]

PATTERNS = ["Solid", "Gradient"]

# Layout / gameplay constants
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 40
FPS = 60
SNAKE_UPDATE_RATE = 8

HIGH_SCORE_FILE = "highscore.txt"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game 🐍")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 40)
big_font = pygame.font.SysFont("comicsansms", 80)
small_font = pygame.font.SysFont("arial", 35)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
apple_path = os.path.join(BASE_DIR, "apple.png")

apple_img = pygame.image.load(apple_path)
apple_img = pygame.transform.scale(apple_img, (BLOCK_SIZE, BLOCK_SIZE))

def load_high_score():
    with open(HIGH_SCORE_FILE, "r") as f:
        return int(f.read())


def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))


def lerp_color(color1, color2, fraction):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int(r1 + (r2 - r1) * fraction)
    g = int(g1 + (g2 - g1) * fraction)
    b = int(b1 + (b2 - b1) * fraction)
    return (r, g, b)


def draw_snake(snake_list, dx, dy, head_color, body_color, pattern):
    head = snake_list[-1]

    # draw body segments
    if pattern == "Solid" or len(snake_list) <= 1:
        for pos in snake_list[:-1]:
            pygame.draw.circle(
                screen,
                head_color,
                (pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE // 2),
                BLOCK_SIZE // 2,
            )

    elif pattern == "Gradient":
        num_segments = len(snake_list) - 1
        if num_segments > 0:
            for i, pos in enumerate(snake_list[:-1]):
                fraction = (i + 1) / (num_segments + 1)
                segment_color = lerp_color(body_color, head_color, fraction)
                pygame.draw.circle(
                    screen,
                    segment_color,
                    (pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE // 2),
                    BLOCK_SIZE // 2,
                )

    # head
    head_center_x = head[0] + BLOCK_SIZE // 2
    head_center_y = head[1] + BLOCK_SIZE // 2
    pygame.draw.circle(screen, head_color, (head_center_x, head_center_y), BLOCK_SIZE // 2)

    eye_radius = 4
    eye_offset = 12

    if dx > 0:
        eye1 = (head_center_x + eye_offset, head_center_y - eye_offset)
        eye2 = (head_center_x + eye_offset, head_center_y + eye_offset)
    elif dx < 0:
        eye1 = (head_center_x - eye_offset, head_center_y - eye_offset)
        eye2 = (head_center_x - eye_offset, head_center_y + eye_offset)
    elif dy > 0:
        eye1 = (head_center_x - eye_offset, head_center_y + eye_offset)
        eye2 = (head_center_x + eye_offset, head_center_y + eye_offset)
    elif dy < 0:
        eye1 = (head_center_x - eye_offset, head_center_y - eye_offset)
        eye2 = (head_center_x + eye_offset, head_center_y - eye_offset)
    else:
        eye1 = (head_center_x - eye_offset, head_center_y - eye_offset)
        eye2 = (head_center_x + eye_offset, head_center_y - eye_offset)

    pygame.draw.circle(screen, BLACK, eye1, eye_radius)
    pygame.draw.circle(screen, BLACK, eye2, eye_radius)



def draw_text(msg, color, x, y, font_type=font, center=True):
    text = font_type.render(msg, True, color)
    if center:
        screen.blit(text, text.get_rect(center=(x, y)))
    else:
        screen.blit(text, [x, y])


def draw_background(screen):
    for y in range(0, HEIGHT, BLOCK_SIZE):
        for x in range(0, WIDTH, BLOCK_SIZE):
            x_idx = x // BLOCK_SIZE
            y_idx = y // BLOCK_SIZE
            color = BG_LIGHT_GREEN if (x_idx + y_idx) % 2 == 0 else BG_DARK_GREEN
            pygame.draw.rect(screen, color, [x, y, BLOCK_SIZE, BLOCK_SIZE])


def skin_selection_screen():
    current_skin_index = 0
    current_pattern_index = 0
    selection = True

    while selection:
        current_skin = SKINS[current_skin_index]
        current_pattern = PATTERNS[current_pattern_index]
        head_color = current_skin["head"]
        body_color = current_skin["body"]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_skin_index = (current_skin_index - 1) % len(SKINS)
                elif event.key == pygame.K_RIGHT:
                    current_skin_index = (current_skin_index + 1) % len(SKINS)
                elif event.key == pygame.K_UP:
                    current_pattern_index = (current_pattern_index - 1) % len(PATTERNS)
                elif event.key == pygame.K_DOWN:
                    current_pattern_index = (current_pattern_index + 1) % len(PATTERNS)
                elif event.key == pygame.K_SPACE:
                    selection = False

        screen.fill(BLACK)
        draw_text("Choose Your Snake", WHITE, WIDTH / 2, 80, big_font)

        draw_text("Color", WHITE, WIDTH / 2, 180, small_font)
        draw_text(f"<< {current_skin['name']} >>", YELLOW, WIDTH / 2, 220, font_type=font)

        draw_text("Pattern", WHITE, WIDTH / 2, 280, small_font)
        draw_text(f"<< {current_pattern} >>", YELLOW, WIDTH / 2, 320, font_type=font)

        preview_snake = [
            (WIDTH / 2 - BLOCK_SIZE * 1.5, HEIGHT / 2 + 50),
            (WIDTH / 2 - BLOCK_SIZE / 2, HEIGHT / 2 + 50),
        ]
        draw_snake(preview_snake, BLOCK_SIZE, 0, head_color, body_color, current_pattern)

        draw_text("Use Left/Right Arrows for Color", WHITE, WIDTH / 2, HEIGHT - 180, small_font)
        draw_text("Use Up/Down Arrows for Pattern", WHITE, WIDTH / 2, HEIGHT - 130, small_font)
        draw_text("Press SPACE to Select & Play", RED, WIDTH / 2, HEIGHT - 60, font_type=font)

        pygame.display.update()
        clock.tick(FPS)

    return head_color, body_color, current_pattern


def game_loop(head_color, body_color, pattern):
    game_over = False
    high_score = load_high_score()

    while not game_over:
        game_close = False

        x = WIDTH / 2
        y = HEIGHT / 2
        dx = BLOCK_SIZE
        dy = 0

        snake = [[x, y]]
        length = 1
        score = 0

        foodx = random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE
        foody = random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
        food_rect = pygame.Rect(foodx, foody, BLOCK_SIZE, BLOCK_SIZE)

        while not game_close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and dx != BLOCK_SIZE:
                        dx, dy = -BLOCK_SIZE, 0
                    elif event.key == pygame.K_RIGHT and dx != -BLOCK_SIZE:
                        dx, dy = BLOCK_SIZE, 0
                    elif event.key == pygame.K_UP and dy != BLOCK_SIZE:
                        dx, dy = 0, -BLOCK_SIZE
                    elif event.key == pygame.K_DOWN and dy != -BLOCK_SIZE:
                        dx, dy = 0, BLOCK_SIZE

            # Check bounds before moving
            if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
                game_close = True

            x += dx
            y += dy

            snake_head_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)

            snake.append([x, y])
            if len(snake) > length:
                del snake[0]

            for segment in snake[:-1]:
                segment_rect = pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE)
                if snake_head_rect.colliderect(segment_rect):
                    game_close = True
                    break

            if snake_head_rect.colliderect(food_rect):
                foodx = random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE
                foody = random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
                food_rect = pygame.Rect(foodx, foody, BLOCK_SIZE, BLOCK_SIZE)

                length += 1
                score = length - 1

            draw_background(screen)

            screen.blit(apple_img, (food_rect.x, food_rect.y))

            draw_snake(snake, dx, dy, head_color, body_color, pattern)

            draw_text(f"Score: {score}", BLACK, 80, 30, center=False, font_type=font)
            draw_text(f"High Score: {high_score}", BLACK, WIDTH - 220, 30, center=False, font_type=font)

            pygame.display.update()

            # Dynamic speed based on score instead of frame-decoupling counter
            clock.tick(10 + score)

        if game_over:
            break

        new_high_score_achieved = score > high_score
        if new_high_score_achieved:
            high_score = score
            save_high_score(high_score)

        screen.fill(BLACK)
        draw_text("Game Over", RED, WIDTH / 2, HEIGHT / 3, big_font)
        draw_text(f"Final Score: {score}", YELLOW, WIDTH / 2, HEIGHT / 2, font_type=font)

        if new_high_score_achieved:
            draw_text("NEW HIGH SCORE!", (0, 255, 0), WIDTH / 2, HEIGHT / 2 + 70, font_type=small_font)
        else:
            draw_text(f"High Score: {high_score}", YELLOW, WIDTH / 2, HEIGHT / 2 + 70, font_type=small_font)

        draw_text("Press C to Play Again or Q to Quit", WHITE, WIDTH / 2, HEIGHT / 1.4, font_type=font)
        pygame.display.update()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    waiting_for_input = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        waiting_for_input = False
                    if event.key == pygame.K_c:
                        waiting_for_input = False
                        return

    pygame.quit()
    quit()


def start_screen():
    screen.fill(BLUE)
    draw_text("Play Snake game ", WHITE, WIDTH / 2, HEIGHT / 3, big_font)
    draw_text("Press SPACE to Start", YELLOW, WIDTH / 2, HEIGHT / 2, font_type=font)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    return


if __name__ == '__main__':
    start_screen()

    while True:
        SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR, SNAKE_PATTERN = skin_selection_screen()
        game_loop(SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR, SNAKE_PATTERN)