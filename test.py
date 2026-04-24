import pygame

pygame.init() 
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Parking Peral")

level = 1

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

start_time = pygame.time.get_ticks()
time_limit = 60
font = pygame.font.SysFont(None, 50)

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

pygame.quit()