import pygame

import random

import time

 

pygame.init()

 

# Creates the pygame window

size = width, height = 700, 600

window = pygame.display.set_mode(size)

pygame.display.set_caption("PLATFORM JUMP")

 

clock = pygame.time.Clock()

 

# Game variables

MAX_PLATFORMS = 10 # Set the maximum number of platforms to generate

GRAVITY = 1.2

platforms = []

SCROLL_THRESHOLD = 300

MAX_ENEMY1 = 2
LIVES = 3
collidelay = True

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

        self.jumpHeight = 17

        self.y_vel = 0

        self.jump_cooldown = 1

        self.last_jump_time = 0

        self.timer = 0

    def move(self, keys):

        if keys[pygame.K_a] or keys[pygame.K_LEFT] and self.x - self.vel - self.radius >= 0:

            self.x -= self.vel

        if keys[pygame.K_d] or keys[pygame.K_RIGHT] and self.x + self.vel - self.radius <= 655:

            self.x += self.vel


        current_time = time.time()       
        if keys[pygame.K_UP]and not self.isJump:

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

 

        # Check for collisions with platforms

        for platform in platforms:

            if (

                self.y_vel >= 0  # Check only for downward movement

                and self.x + self.radius >= platform.x

                and self.x - self.radius <= platform.x + platform.width

                and self.y + self.radius >= platform.y

                and self.y - self.radius <= platform.y + platform.height

               and self.y + self.radius + self.y_vel >= platform.y

            ):  #check only for collision with top surface

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

 

    def collides_with_circle(self, circle):

        if (

            circle.y_vel >= 0  # Check only for downward movement

            and circle.x + circle.radius >= self.x

            and circle.x - circle.radius <= self.x + self.width

            and circle.y + circle.radius >= self.y

            and circle.y - circle.radius <= self.y + self.height

        ):

           return True

        else:

            return False

 

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

        self.x -= self.vel

 

#creating the circle and platform objects

circle = Circle(250, 470, 20, (255, 0, 0))

platforms = [

    Platform(250, 470, 75, 10, (0, 255, 0)),

    Platform(250, 470, 75, 10, (0, 255, 0)),

    Platform(250, 470, 75, 10, (0, 255, 0)),

]

enemy1s = []

 

def enemy1_generation():   

    #generate a new enemy1 if there are fewer than MAX_ENEMY1

    if len(enemy1s) < MAX_ENEMY1:

        y = random.randint(50, 500)

        vel = random.randint(8, 13)

        new_enemy1 = Enemy1(690, y, 45, 30, (0, 0, 255), vel)

        enemy1s.append(new_enemy1)

 

   #remove enemy1 that goes off screen

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

 
def live_system():
    global collidelay
    collidelay = True

def pause(keys):
    if keys[pygame.K_x]:
        time.sleep(1000)

#where all the drawing of objects is done

def redraw_game_window():

    #adjust the position of the objects on the screen if the circle's y-position exceeds the scrolling threshold

    if circle.x > SCROLL_THRESHOLD:

        dx = SCROLL_THRESHOLD - circle.x

        circle.x += dx

        for platform in platforms:

            platform.x += dx

 

    #draw the objects on the screen

    window.fill((0, 0, 0))

    for platform in platforms:

        platform.platform_draw()

    circle.circle_draw()

    for enemy1 in enemy1s:

        enemy1.enemy1_draw()

 

    #display the remaining jump cooldown time

    current_time = time.time()

    remaining_cooldown = circle.jump_cooldown - (current_time - circle.last_jump_time)

    remaining_cooldown = max(remaining_cooldown, 0)  # Prevent cooldown from going below zero

    remaining_cooldown_text = "Double Jump Cooldown: {:.1f}s".format(remaining_cooldown)

    font = pygame.font.Font(None, 36)

    text = font.render(remaining_cooldown_text, True, (255, 255, 255))

    window.blit(text, (10, 10))

    #display the ramaing dash cooldown
    

 

    # Display the timer

    timer_text = "Time: {:.1f}s".format(circle.timer)

    timer = font.render(timer_text, True, (255, 255, 255))

    window.blit(timer, (10, 50))

 

    pygame.display.update()

 
menu = False
options = False
game_over = False

def options_menu():
    global window, menu, game_over
    window = pygame.display.set_mode((width, height))
    options = True
    pygame.display.set_caption("Main Menu!")

    font = pygame.font.Font('freesansbold.ttf', 60)
    text = font.render('OPTIONS MENU', True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.center = (width // 2, 40)

    font = pygame.font.Font('freesansbold.ttf', 20)
    text2 = font.render('GAME INSTRUCTIONS', True, (255, 255, 255))
    textRect2 = text.get_rect()
    textRect2.center = (width // 2, 200)

    window.fill((0, 0, 0))
    window.blit(text, textRect)
    window.blit(text2, textRect2)
    pygame.display.update()

    while options == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_m:
                    options = False
                    main_menu()

def main_menu():
    global window, menu, game_over
    window = pygame.display.set_mode((width, height))
    menu = True
    pygame.display.set_caption("Main Menu!")

    font = pygame.font.Font('freesansbold.ttf', 60)
    text = font.render('MAIN MENU', True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.center = (width // 2, 40)

    font = pygame.font.Font('freesansbold.ttf', 20)
    text2 = font.render('Press O to go to the options menu', True, (255, 255, 255))
    textRect2 = text.get_rect()
    textRect2.center = (width // 2, 200)

    font = pygame.font.Font('freesansbold.ttf', 20)
    text3 = font.render('Press P to start the game', True, (255, 255, 255))
    textRect3 = text.get_rect()
    textRect3.center = (width // 2, 250)

    window.fill((0, 0, 0))
    window.blit(text, textRect)
    window.blit(text2, textRect2)
    window.blit(text3, textRect3)
    pygame.display.update()

    while menu == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_o:
                    menu = False
                    options_menu()
                if event.key == pygame.K_p:
                    menu = False
                    main_game()
      

def main_game():
    global LIVES
    global collidelay
    run = True

    start_time = time.time() # Captures the time at the beginning of the game

    while run:

        clock.tick(60)

 

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                run = False

    

        #calls the move function

        keys = pygame.key.get_pressed()

        circle.move(keys)
        

        #calls the function which will randomly generate platforms

        random_platform()

 

        #update the timer

        current_time = time.time()

        circle.timer = current_time - start_time

 

        #quits the game if circle touches floor

        if circle.y == 580:

            pygame.quit()

 

         #calls functions for enemy1

        for enemy1 in enemy1s:

            enemy1.enemy1_move()

 

                    # Check for collisions with the circle

            if (

                circle.x + circle.radius >= enemy1.x

                and circle.x - circle.radius <= enemy1.x + enemy1.width

                and circle.y + circle.radius >= enemy1.y

                and circle.y - circle.radius <= enemy1.y + enemy1.height

            ):
                LIVES = LIVES -1
                time.sleep(0.001)
        print("lives: " + str(LIVES))
        
        print("timer: " + str(int(circle.timer)))
       

        if random.randint(1, 100) == 1:

            enemy1_generation()

        keys = pygame.key.get_pressed()
        pause(keys)
            

        redraw_game_window()

 

main_menu()

pygame.quit()
