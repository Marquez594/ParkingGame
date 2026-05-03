import pygame
import random 
num_spots = 6
parking_spots = []

pygame.init() 
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Parking Peril")


level = 0
clock = pygame.time.Clock()

garage_bottom = pygame.image.load("garage-bottom.jpg")
garage_bottom = pygame.transform.scale(garage_bottom,(width,height))

garage_middle = pygame.image.load("garage-middle.jpg")
garage_middle = pygame.transform.scale(garage_middle,(width,height))

garage_top = pygame.image.load("garage-top.webp")
garage_top = pygame.transform.scale(garage_top,(width,height))

level = 0

parked_car = pygame.image.load("parkedcar.png")
parked_car = pygame.transform.scale(parked_car, (200, 200))
#
user = pygame.image.load("user.webp")
user = pygame.transform.scale(user,(200,200))
user_x = width//2
user_y = height//1.5
speed = 11
probability = 0.95


direction = "right"

time_limit = 60
font = pygame.font.SysFont(None, 50)

# START SCREEN SETUP
car_parc = pygame.image.load("titlescreen.jpg")
car_parc = pygame.transform.scale(car_parc, (width, height))

selected_difficulty = "easy"
game_started = False

def draw_button(text, x, y, w, h, color, text_color=(255,255,255)):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=(x + w//2, y + h//2))
    screen.blit(label, label_rect)
    return pygame.Rect(x, y, w, h)

while not game_started:
    screen.blit(car_parc, (0, 0))
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))
    title_font = pygame.font.SysFont(None, 90)
    title = title_font.render("Parking Peril", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(width//2, 180)))
    diff_label = font.render("Select Difficulty:", True, (255, 255, 255))
    screen.blit(diff_label, diff_label.get_rect(center=(width//2, 310)))
    easy_color   = (0, 180, 0)   if selected_difficulty == "easy"   else (80, 80, 80)
    medium_color = (200, 140, 0) if selected_difficulty == "medium" else (80, 80, 80)
    hard_color   = (180, 0, 0)   if selected_difficulty == "hard"   else (80, 80, 80)
    easy_btn   = draw_button("Easy",   width//2 - 310, 360, 180, 60, easy_color)
    medium_btn = draw_button("Medium", width//2 - 90,  360, 180, 60, medium_color)
    hard_btn   = draw_button("Hard",   width//2 + 130, 360, 180, 60, hard_color)
    start_btn  = draw_button("START",  width//2 - 110, 480, 220, 70, (30, 30, 200))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if easy_btn.collidepoint(event.pos):
                selected_difficulty = "easy"
            elif medium_btn.collidepoint(event.pos):
                selected_difficulty = "medium"
            elif hard_btn.collidepoint(event.pos):
                selected_difficulty = "hard"
            elif start_btn.collidepoint(event.pos):
                game_started = True
                print(f"Difficulty: {selected_difficulty}, Time: {time_limit}")
                if selected_difficulty == "medium":
                    probability = 0.97
                elif selected_difficulty == "hard":
                    probability = 0.99

    clock.tick(60)
# START SCREEN END


start_time = pygame.time.get_ticks()

reverse = False

def refresh_spawns():
    global parking_spots, reverse
    reverse = not reverse
    parking_spots = []

    for i in range(num_spots):

        if random.random() < probability:
            parking_spots.append(1)
        else: 
            parking_spots.append(0)
    
refresh_spawns()
spot_width = 120

gap = 60
y = 450

level_swap = False

start_x = (width - (num_spots * spot_width + (num_spots -1 ) * gap )) //2 - 50
frozen = False
pause_start = None

    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not frozen:
                if event.key == pygame.K_SPACE:
                    if reverse:
                        if user_x < 50 and level != 0:
                            level = max(0,level-1)
                            refresh_spawns()
                            direction = "left"
                            
                        elif user_x > width - 250 and level != 8:
                            level = min(8,level+1)
                            refresh_spawns()
                            direction = "right"
                            
                        else:
                            for i in range(num_spots):
                                x = start_x + i * (spot_width + gap)

                                # check if player is in this spot
                                if abs(user_x - x) < 40 and abs(user_y - y ) < 50:

                                    # only allow parking if empty
                                    if parking_spots[i] == 0:
                                        parking_spots[i] = 2  # parked successfully
                                        print("Parked!")
                                        #Set Pause 
                                        pause_start = pygame.time.get_ticks()
                                        frozen = True
                                    else:
                                        print("Spot taken!")
                    else:
                        if user_x < 50 and level != 0:
                            level = max(0,level+1)
                            refresh_spawns()
                            direction = "left"
                            
                        elif user_x > width - 250 and level != 8:
                            level = min(8,level-1)
                            refresh_spawns()
                            direction = "right"
                            
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

    #User movement
    #if frozen is true then user cannot move
    #else they can move
    if not frozen:
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            user_x -= speed
            direction = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            user_x += speed
            direction = "right"
    
    
  

    #makes sure player does not go past the game border
    user_x = max(0,min(user_x,width-200))


    #Handle different background when player goes up/down levels
    if (level == 0):
        screen.blit(garage_bottom,(0,0)) 
    elif (level == 8):
        screen.blit(garage_top,(0,0))
    else:
        screen.blit(garage_middle,(0,0))

    for i in range(num_spots):
        x = start_x + i * (spot_width + gap)

        if parking_spots[i]:
            screen.blit(parked_car,(x,y))


    

    
    #Makes player model flip to give that left/right feel
    if direction == "left":
        rotated_user = pygame.transform.flip(user,True,False)
    else:
        rotated_user = user
    screen.blit(rotated_user, (int(user_x), int(user_y)))

    #Pause timer if frozen true
    if frozen:
        elapsed_time = (pause_start - start_time) / 1000
    else:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    remaining_time = max(0,time_limit - int(elapsed_time))

    #set frozen true and pause if player has reached time limit
    if remaining_time <= 0:
        pause_start = pygame.time.get_ticks()
        frozen = True
        running = False
        game_result = "lose"
    
    # check if player parked successfully
    if 2 in parking_spots and frozen:
        running = False
        game_result = "win"

    timer = font.render(f"Time: {remaining_time}s",True,(255,255,255))

    timer_rect = timer.get_rect(center=(width//2,30))
    screen.blit(timer, (width//2 - 80, 10))
    level_text = font.render(f"Floor: {level}", True, (255, 255, 255))
    screen.blit(level_text, (20, 20))
    if reverse:
        help_text = font.render("Go to edges + press SPACE (Left=Down, Right=Up)", True, (255,255,255))
    else:
        help_text = font.render("Go to edges + press SPACE (Left=Up, Right=Down)", True, (255,255,255))
    screen.blit(help_text, (20, 680))
    pygame.display.flip()
    clock.tick(60)  # limit to 60 FPS

# END SCREEN
while True:
    screen.blit(car_parc, (0, 0))
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))
    title_font = pygame.font.SysFont(None, 90)
    
    if game_result == "win":
        msg = title_font.render("You Win!", True, (0, 255, 0))
        sub = font.render("You found a parking spot!", True, (255, 255, 255))
    else:
        msg = title_font.render("Game Over!", True, (255, 60, 60))
        sub = font.render("You ran out of time!", True, (255, 255, 255))

    screen.blit(msg, msg.get_rect(center=(width//2, 250)))
    screen.blit(sub, sub.get_rect(center=(width//2, 350)))
   quit_btn   = draw_button("QUIT",   width//2 + 20,  450, 200, 70, (80, 80, 80))
   replay_btn = draw_button("REPLAY", width//2 - 230, 450, 200, 70, (30, 30, 200))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_btn.collidepoint(event.pos):
                pygame.quit()
                exit()
            elif replay_btn.collidepoint(event.pos):
                pygame.quit()
                import subprocess
                import sys
                subprocess.Popen([sys.executable, __file__])
                exit()
    clock.tick(60)
