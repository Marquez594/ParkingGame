import pygame

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

user = pygame.image.load("user.png")
user = pygame.transform.scale(user,(200,200))
user_x = width//2
user_y = height//2 + 100
speed = 5

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
    title = title_font.render("Parking Peral", True, (255, 255, 255))
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
                if selected_difficulty == "easy":
                    speed = 4
                elif selected_difficulty == "medium":
                    speed = 7
                elif selected_difficulty == "hard":
                    speed = 11
    clock.tick(60)
# START SCREEN END

start_time = pygame.time.get_ticks()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    #User movement
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        user_x -= speed
        direction = "left"
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
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
    
    #Makes player model flip to give that left/right feel
    if direction == "left":
        rotated_user = pygame.transform.flip(user,True,False)
    else:
        rotated_user = user
    screen.blit(rotated_user,(user_x,user_y))

    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    remaining_time = max(0,time_limit - int(elapsed_time))

    timer = font.render(f"Time: {remaining_time}s",True,(255,255,255))

    timer_rect = timer.get_rect(center=(width//2,30))
    screen.blit(timer,timer_rect)

    pygame.display.flip()
    clock.tick(60)  # limit to 60 FPS

pygame.quit()
