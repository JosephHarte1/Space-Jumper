import pygame
import random
import time
import os

pygame.init()

# Creates the pygame window
size = width, height = 700, 600
window = pygame.display.set_mode(size)
pygame.display.set_caption("PLATFORM JUMP")

clock = pygame.time.Clock()

# Game variables
MAX_PLATFORMS = 10 # Set the maximum number of platforms to generate
GRAVITY = 1.2
SCROLL_THRESHOLD = 300
MAX_ENEMY1 = 0
SPAWN_CHANCE = 110
LIVES = 3
difinc = False
invincible = False
MAX_POWERUPS = 1
POWERUP_SPAWNCHANCE = 100

#timer variable
paused_total = 0

#sprites
space_background = pygame.image.load("space_background.png")
space_background = pygame.transform.scale(space_background, (width, height))

space2_background = pygame.image.load("space2_background.png")
space2_background = pygame.transform.scale(space2_background, (width, height))

# Player object class
class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 7
        self.isJump = False
        self.jumpCount = 10
        self.jumpHeight = 20
        self.y_vel = 0
        self.jump_cooldown = 2
        self.last_jump_time = 0
        self.timer = 0

    def move(self, keys):
        if keys[pygame.K_a] or keys[pygame.K_LEFT] and self.x - self.vel - self.radius >= 0:
            self.x -= self.vel
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] and self.x + self.vel - self.radius <= 655:
            self.x += self.vel

        current_time = time.time()
        remaining_cooldown = self.jump_cooldown - (current_time - self.last_jump_time)
        if remaining_cooldown <= 0 and (keys[pygame.K_SPACE] or keys[pygame.K_UP])and not self.isJump:
            self.isJump = True
            self.y_vel = -self.jumpHeight  # Set the y-velocity based on the jump height
            self.last_jump_time = current_time

        if self.isJump:
            self.y_vel += GRAVITY
            self.y += self.y_vel
            self.jumpCount -= 1
            if self.jumpCount == 0:
                self.isJump = False
                self.jumpCount = 10

        #check for collisions with platforms
        for platform in platforms:
            if (self.y_vel >= 0  #check only for downward movement
                and self.x + self.radius >= platform.x
                and self.x - self.radius <= platform.x + platform.width
                and self.y + self.radius >= platform.y
                and self.y - self.radius <= platform.y + platform.height
                and self.y + self.radius + self.y_vel >= platform.y):  #check only for collision with top surface
                self.isJump = False
                self.jumpCount = 10
                self.y_vel = -20
                # Update y-position and y-velocity
                platforms.remove(platform)
                # Removes the platform that the player just jumped onto

        if not self.isJump:
            self.y_vel += GRAVITY
            self.y += self.y_vel
            if self.y + self.radius >= height:
                self.y = height - self.radius
                self.y_vel = 0
                self.isJump = False
                self.jumpCount = 10

    def circle_draw(self):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)


#platform object class
class Platform:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def platform_draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

class Enemy1:
    def __init__(self, x, y, width, height, color, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = vel

    def enemy1_draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
   
    def enemy1_move(self):
        self.x -= self.vel #enemy1 will move to the left

class PowerUp:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        
    def powerUp_draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

#creating the objects
circle = Circle(250, 470, 20, (255, 0, 0))
                 
platforms = [
    Platform(250, 470, 75, 10, (0, 255, 0)),  
    Platform(250, 470, 75, 10, (0, 255, 0)),
    Platform(250, 470, 75, 10, (0, 255, 0))]

enemy1s = []

powerUps = []

def powerUp_generation():
    if len(powerUps) < MAX_POWERUPS:#generate new power up if there is less than MAX_POWERUPS
        y = random.randint(100, 500) 
        new_powerUp = PowerUp(690, y, 20, 20, (255, 255, 0))
        powerUps.append(new_powerUp)
    
    #remove power ups that go off screen                    
    for powerUp in powerUps:
        if powerUp.x + powerUp.width < 0:
            powerUps.remove(powerUp)
            
def enemy1_generation():
    if len(enemy1s) < MAX_ENEMY1: # Generate a new enemy1 if there are less than MAX_ENEMY1
        y = random.randint(100, 500)
        vel = random.randint(5, 7)
        new_enemy1 = Enemy1(690, y, 45, 30, (0, 0, 255), vel)
        enemy1s.append(new_enemy1)
    #remove enemies that go off screen
    for enemy1 in enemy1s:
        if enemy1.x + enemy1.width < 0:
            enemy1s.remove(enemy1)


def random_platform():
    #generate a new platform if there are fewer than MAX_PLATFORMS
    if len(platforms) < MAX_PLATFORMS:
        x = platforms[-1].x + random.randint(10, 250)  # Generate platforms ahead of the last platform
        y = random.randint(250, 550)
        new_platform = Platform(x, y, 75, 10, (0, 255, 0))
        platforms.append(new_platform)

    #remove platforms that are off the screen
    for platform in platforms:
        if platform.x + platform.width < 0:
            platforms.remove(platform)
   

def timer():
    global start_time
    current_time = time.time()
    circle.timer = current_time - start_time - paused_total      

def difficulty_increase():
    global difinc
    global SPAWN_CHANCE
    global MAX_ENEMY1
    global MAX_PLATFORMS
    global POWERUP_SPAWNCHANCE
    #only changes the difficulty at time intervals of 5 and stops when MAX_PLATFORMS is less than 3
    if int(circle.timer) %5 == 0 and difinc == False and MAX_PLATFORMS > 4:
            difinc = True
            SPAWN_CHANCE = SPAWN_CHANCE - 10
            MAX_ENEMY1 = MAX_ENEMY1 + 1
            MAX_PLATFORMS = MAX_PLATFORMS - 1
            POWERUP_SPAWNCHANCE = POWERUP_SPAWNCHANCE + 10
           
def lives():
    global LIVES
    global run
    if LIVES <= 0:
        end_screen()
       
def invincibility():
    #Check if invincibility duration has elapsed, then reset the flag
    global invincible
    global invincibility_start_time
    invincibility_duration = 1  #1 seconds
    if invincible:
        current_time = time.time()
        if current_time - invincibility_start_time >= invincibility_duration:
            invincible = False

def high_score():
    #checks if file exists
    if os.path.exists('high_scores.txt') == False:
        #make a file if it doesn't exist
        file = open('high_scores.txt','w+')
        #sets high score to 0 if no file exists
        file.write('0')
        file.close
    file = open('high_scores.txt','r')
    #giving current high score a variable
    contents = file.read()
    file.close
    #checks if current score is higher than high score
    if float(contents) > circle.timer:
        return float(contents)
    else:
        file = open('high_scores.txt','w')
        score = str(circle.timer)
        file.write(score)
        file.close
        return circle.timer
        
#where all the drawing of objects is done
def redraw_game_window():
    global LIVES
    #adjust the position of the objects on the screen if the circle's y-position exceeds the scrolling threshold
    if circle.x > SCROLL_THRESHOLD:
        dx = SCROLL_THRESHOLD - circle.x
        circle.x += dx
        for platform in platforms:
            platform.x += dx
        for enemy1 in enemy1s:
            enemy1.x += dx
        for powerUp in powerUps:
            powerUp.x += dx
    
    window.blit(space2_background, (0, 0))
    
    for platform in platforms:
        platform.platform_draw()
    circle.circle_draw()
    for enemy1 in enemy1s:
        enemy1.enemy1_draw()
    for powerUp in powerUps:
        powerUp.powerUp_draw()

    

    # Display the remaining cooldown time
    current_time = time.time()
    remaining_cooldown = circle.jump_cooldown - (current_time - circle.last_jump_time)
    remaining_cooldown = max(remaining_cooldown, 0)  # Prevent cooldown from going below zero
    remaining_cooldown_text = "Double Jump Cooldown: {:.1f}s".format(remaining_cooldown)
    font = pygame.font.Font(None, 36)
    text = font.render(remaining_cooldown_text, True, (255, 255, 255))
    window.blit(text, (10, 10))

    # Display the timer

    timer_text = "Time: {:.1f}s".format(circle.timer)
    timer = font.render(timer_text, True, (255, 255, 255))
    window.blit(timer, (10, 50))
    pygame.display.update()
    #Display lives
    live_text = "Remaining lives: {:.1f}".format(int(LIVES))
    live = font.render(live_text, True, (255, 255, 255))
    window.blit(live, (10, 90))
    pygame.display.update()
       
def MainMenu():
    menu = True
    while menu == True:
        global window
        window.blit(space_background, (0, 0))

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render('PRESS SPACE TO START', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (width // 2 , 200)

        font = pygame.font.Font('freesansbold.ttf', 20)
        text2 = font.render('press the arrow keys to move across the screen and press space to jump', True, (255, 255, 255))
        textRect2 = text2.get_rect()
        textRect2.center = (width // 2 , 400)

        font = pygame.font.Font('freesansbold.ttf', 20)
        text3 = font.render('CAN YOU GET THE HIGHEST SCORE', True, (0, 255, 0))
        textRect3 = text3.get_rect()
        textRect3.center = (width // 2 , 450)

        highscore_font = pygame.font.Font('freesansbold.ttf', 25)
        highscore_text = highscore_font.render('High Score: {:.1f}s'.format(high_score()), True, (255, 255, 255))
        highscore_rect = highscore_text.get_rect()
        highscore_rect.center = (width // 2, 300)

        window.blit(text, textRect)
        window.blit(text2, textRect2)
        window.blit(text3, textRect3)
        window.blit(highscore_text, highscore_rect)
        pygame.display.update()
       

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
               
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                menu = False
    main_game()

def pause_screen():
    pause = True
    while pause == True:
        global window
        window.blit(space_background, (0, 0))

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render('PAUSE SCREEN ENABLED', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (width // 2 , 200)

        font = pygame.font.Font('freesansbold.ttf', 30)
        text2 = font.render('R - RESTART GAME', True, (255, 255, 255))
        textRect2 = text2.get_rect()
        textRect2.center = (width // 2 , 250)

        font = pygame.font.Font('freesansbold.ttf', 30)
        text3 = font.render('Q - QUIT GAME', True, (255, 255, 255))
        textRect3 = text3.get_rect()
        textRect3.center = (width // 2 , 300)

        window.blit(text, textRect)
        window.blit(text2, textRect2)
        window.blit(text3, textRect3)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
               
            keys = pygame.key.get_pressed()

            if keys[pygame.K_p]:
                pause = False

            if keys[pygame.K_r]:
                reset_game()
                MainMenu()
            if keys[pygame.K_q]:
                pygame.quit()
           
def reset_game():
    global platforms, enemy1s, circle, LIVES, difinc, invincible, start_time, paused_total, MAX_PLATFORMS, SPAWN_CHANCE, MAX_ENEMY1, powerUps
    # Reset all game variables to their initial state
    platforms = [
        Platform(250, 470, 75, 10, (0, 255, 0)),
        Platform(250, 470, 75, 10, (0, 255, 0)),
        Platform(250, 470, 75, 10, (0, 255, 0))]
    enemy1s = []
    powerUps = []
    circle = Circle(250, 470, 20, (255, 0, 0))
    LIVES = 3
    difinc = False
    invincible = False
    start_time = time.time()
    paused_total = 0
    MAX_ENEMY1 = 0
    SPAWN_CHANCE = 110
    MAX_PLATFORMS = 10
    circle.timer = 0
   
def end_screen():
    game_over = True
    while game_over == True:
        global window
        window.blit(space_background, (0, 0))

        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render('GAME OVER', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (width // 2 , 200)

        font = pygame.font.Font('freesansbold.ttf', 30)
        text2 = font.render('R - RESTART GAME', True, (255, 255, 255))
        textRect2 = text2.get_rect()
        textRect2.center = (width // 2 , 250)

        font = pygame.font.Font('freesansbold.ttf', 30)
        text3 = font.render('Q - QUIT GAME', True, (255, 255, 255))
        textRect3 = text3.get_rect()
        textRect3.center = (width // 2 , 300)

        score_font = pygame.font.Font('freesansbold.ttf', 30)
        score_text = score_font.render('Your Score: {:.1f}s'.format(circle.timer), True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.center = (width // 2, 350)

        highscore_font = pygame.font.Font('freesansbold.ttf', 30)
        highscore_text = highscore_font.render('High Score: {:.1f}s'.format(high_score()), True, (255, 255, 255))
        highscore_rect = highscore_text.get_rect()
        highscore_rect.center = (width // 2, 400)


        window.blit(text, textRect)
        window.blit(text2, textRect2)
        window.blit(text3, textRect3)
        window.blit(highscore_text, highscore_rect)
        window.blit(score_text, score_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            reset_game()
            MainMenu()
        if keys[pygame.K_q]:
            pygame.quit()
   
def main_game():
    global difinc
    global LIVES
    global run
    global invincible
    global invincibility_start_time
    global start_time
    global paused_total
    global POWERUP_SPAWNCHANCE

    start_time = time.time()

    run = True
    while run:  
        clock.tick(60)
   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #call pause_screen() function when 'P' key is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                #PAUSED TIME PROCESS
                pause_time = time.time()
                pause_screen()
                resume_time = time.time()

                paused_for = resume_time - pause_time
                paused_total = paused_total + paused_for
               
        #calls the move function
        keys = pygame.key.get_pressed()
        circle.move(keys)

        #calls the function which will randomly generate platforms
        random_platform()

        #calls the function which increase the difficulty of the game
        difficulty_increase()

        if int(circle.timer) % 5 != 0:
            difinc = False
           
        #calls the timer MainMenu()function
        timer()

       
        #calls the functions for enemy 1
        if random.randint(1, SPAWN_CHANCE) == 1:
            enemy1_generation()

        for enemy1 in enemy1s:
            enemy1.enemy1_move()
            if not invincible and (circle.x + circle.radius >= enemy1.x
                    and circle.x - circle.radius <= enemy1.x + enemy1.width
                    and circle.y + circle.radius >= enemy1.y
                    and circle.y - circle.radius <= enemy1.y + enemy1.height):
                LIVES = LIVES - 1
                invincible = True  #set invincibility flag
                invincibility_start_time = time.time()  #start the invincibility timer

        if random.randint(1, POWERUP_SPAWNCHANCE) == 1:
            powerUp_generation()

        for powerUp in powerUps:
            if (circle.x + circle.radius >= powerUp.x
                and circle.x - circle.radius <= powerUp.x + powerUp.width
                and circle.y + circle.radius >= powerUp.y
                and circle.y - circle.radius <= powerUp.y + powerUp.height): #checks for collisions between circle and power up
                    powerUps.remove(powerUp)
                    LIVES = LIVES +1
        
            
        #calls function which changes invincibility
        invincibility()
        #calls the function which quits the game when lives are 0
        lives()
        #calls the function which sets the player's new high score
        high_score()
        #quits the game if circle touches floor
        if circle.y == 580:
            end_screen()
        
        redraw_game_window()
       
MainMenu()      
main_game()
   
pygame.quit()
