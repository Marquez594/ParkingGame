import pygame
import random
import asyncio
import sys


pygame.init()

num_spots = 6
parking_spots = []

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Parking Peril")

level = 0
clock = pygame.time.Clock()

def safe_load(path, size):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except Exception as e:
        print("FAILED TO LOAD:", path, e)
        surf = pygame.Surface(size)
        surf.fill((80, 80, 80))  
        return surf

garage_bottom = None
garage_middle = None
garage_top = None
parked_car = None
user = None
car_parc = None

async def load_assets():
    global garage_bottom, garage_middle, garage_top
    global parked_car, user, car_parc

    garage_bottom = safe_load("garage-bottom.jpg", (width, height))
    garage_middle = safe_load("garage-middle.jpg", (width, height))
    garage_top = safe_load("garage-top.png", (width, height))

    parked_car = safe_load("parkedcar.png", (200, 200))
    user = safe_load("user.png", (200, 200))
    car_parc = safe_load("titlescreen.jpg", (width, height))

    await asyncio.sleep(0)


user_x = width // 2
user_y = height // 1.5
speed = 11
probability = 0.95
direction = "right"

time_limit = 60
font = pygame.font.SysFont(None, 50)

selected_difficulty = "easy"
game_started = False

reverse = False

def draw_button(text, x, y, w, h, color, text_color=(255, 255, 255)):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)
    label = font.render(text, True, text_color)
    screen.blit(label, label.get_rect(center=(x + w // 2, y + h // 2)))
    return pygame.Rect(x, y, w, h)


async def first_frame():
    screen.fill((30, 30, 30))
    t = font.render("Loading...", True, (255, 255, 255))
    screen.blit(t, t.get_rect(center=(width // 2, height // 2)))
    pygame.display.flip()
    await asyncio.sleep(0)


async def start_screen():
    global selected_difficulty, probability, game_started

    while not game_started:
        screen.blit(car_parc, (0, 0))

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        title_font = pygame.font.SysFont(None, 90)
        title = title_font.render("Parking Peril", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(width // 2, 180)))

        diff_label = font.render("Select Difficulty:", True, (255, 255, 255))
        screen.blit(diff_label, diff_label.get_rect(center=(width // 2, 310)))

        easy_color = (0, 180, 0) if selected_difficulty == "easy" else (80, 80, 80)
        medium_color = (200, 140, 0) if selected_difficulty == "medium" else (80, 80, 80)
        hard_color = (180, 0, 0) if selected_difficulty == "hard" else (80, 80, 80)

        easy_btn = draw_button("Easy", width // 2 - 310, 360, 180, 60, easy_color)
        medium_btn = draw_button("Medium", width // 2 - 90, 360, 180, 60, medium_color)
        hard_btn = draw_button("Hard", width // 2 + 130, 360, 180, 60, hard_color)
        start_btn = draw_button("START", width // 2 - 110, 480, 220, 70, (30, 30, 200))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn.collidepoint(event.pos):
                    selected_difficulty = "easy"
                elif medium_btn.collidepoint(event.pos):
                    selected_difficulty = "medium"
                elif hard_btn.collidepoint(event.pos):
                    selected_difficulty = "hard"
                elif start_btn.collidepoint(event.pos):
                    game_started = True
                    if selected_difficulty == "medium":
                        probability = 0.97
                    elif selected_difficulty == "hard":
                        probability = 0.99

        clock.tick(60)
        await asyncio.sleep(0)


def refresh_spawns():
    global parking_spots, reverse
    reverse = not reverse
    parking_spots = [
        1 if random.random() < probability else 0
        for _ in range(num_spots)
    ]

def reset_game():
    global level, user_x, parking_spots, game_started

    level = 0
    user_x = width // 2
    parking_spots.clear()
    game_started = True


async def game_loop():
    global user_x, direction, level

    start_time = pygame.time.get_ticks()
    frozen = False
    pause_start = None

    spot_width = 120
    gap = 60
    y = 450

    start_x = (width - (num_spots * spot_width + (num_spots - 1) * gap)) // 2 - 50

    refresh_spawns()

    running = True
    game_result = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if not frozen and event.key == pygame.K_SPACE:
                    at_left = user_x < 50
                    at_right = user_x > width - 250

                    if at_left and level != 0:
                        if reverse:
                            level = min(8, level + 1)
                        else:
                            level = max(0, level - 1)
                        refresh_spawns()

                    elif at_right and level != 8:
                        if reverse:
                            level = max(0, level - 1)
                        else:
                            level = min(8, level + 1)
                        refresh_spawns()
                        
                    else:
                        for i in range(num_spots):
                                x = start_x + i * (spot_width + gap)

                                # check if player is in this spot
                                if abs(user_x - x) < 40 and abs(user_y - y ) < 50:

                                    # only allow parking if empty
                                    if parking_spots[i] == 0:
                                        parking_spots[i] = 2  # parked successfully
                                        print("Parked!")
                                        #Set pause
                                        pause_start = pygame.time.get_ticks()
                                        frozen = True
                                    else:
                                        print("Spot taken!")

        keys = pygame.key.get_pressed()

        if not frozen:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                user_x -= speed
                direction = "left"
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                user_x += speed
                direction = "right"

        user_x = max(0, min(user_x, width - 200))

        # BACKGROUND
        if level == 0:
            screen.blit(garage_bottom, (0, 0))
        elif level == 8:
            screen.blit(garage_top, (0, 0))
        else:
            screen.blit(garage_middle, (0, 0))

        # CARS
        for i in range(num_spots):
            x = start_x + i * (spot_width + gap)
            if parking_spots[i]:
                screen.blit(parked_car, (x, y))

        # PLAYER
        if direction == "left":
            rotated_user = pygame.transform.flip(user, True, False)
        else:
            rotated_user = user

        screen.blit(rotated_user, (int(user_x), int(user_y)))

        # TIMER
        if frozen:
            elapsed_time = (pause_start - start_time) / 1000
        else:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

        remaining_time = max(0, time_limit - int(elapsed_time))

        if remaining_time <= 0:
            running = False
            game_result = "lose"

        if 2 in parking_spots:
            running = False
            game_result = "win"

        timer = font.render(f"Time: {remaining_time}s", True, (255, 255, 255))
        screen.blit(timer, (width // 2 - 80, 10))
        level_text = font.render(f"Floor: {level}", True, (255, 255, 255))
        screen.blit(level_text, (20, 20))
        if reverse:
            help_text = font.render("Go to edges + press SPACE (Left=Up, Right=Down, SPACE to park", True, (255,255,255))
        else:
            help_text = font.render("Go to edges + press SPACE (Left=Down, Right=Up), SPACE to park", True, (255,255,255))
        screen.blit(help_text, (20, 680))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    return game_result


# ---------------- END SCREEN ----------------
async def end_screen(game_result):
    while True:
        screen.blit(car_parc, (0, 0))

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        title_font = pygame.font.SysFont(None, 90)

        if game_result == "win":
            msg = title_font.render("You Win!", True, (0, 255, 0))
        else:
            msg = title_font.render("Game Over!", True, (255, 60, 60))

        screen.blit(msg, msg.get_rect(center=(width // 2, 250)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        clock.tick(60)
        await asyncio.sleep(0)


async def main():
    await first_frame()
    await load_assets()
    await start_screen()
    while True:
        result = await game_loop()

        if result == "replay":
            reset_game()
            continue

        await end_screen(result)
        break


asyncio.run(main())