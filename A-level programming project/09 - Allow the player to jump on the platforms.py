import pygame
import random

pygame.init()

#creates the pygame window
size = width, height = 500, 600

window = pygame.display.set_mode(size)
pygame.display.set_caption("PLATFORM JUMP")

clock = pygame.time.Clock()

#player object class
class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 10
        self.isJump = True  
        self.jumpCount = 10

    #player movements
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - self.vel - self.radius>= 0:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x + self.vel - self.radius <= 445:
            self.x += self.vel
        #allows the player to jump
        if not(self.isJump):
            self.isJump = True  #automatically set isJump to True if not jumping
        else:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
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

#creating the circle and platform objects
circle = Circle(250, 570, 25, (255, 0, 0))
#create a list of platforms
platforms = [Platform(213, 570, 75, 10, (0, 255, 0)), 
             Platform(100, 450, 75, 10, (0, 255, 0)), 
             Platform(300, 350, 75, 10, (0, 255, 0))]

MAX_PLATFORMS = 10  #set the maximum number of platforms to generate

def random_platform():
            #generate a new platform if there are fewer than MAX_PLATFORMS
        if len(platforms) < MAX_PLATFORMS:
            x = random.randint(0, 445)
            y = random.randint(100, 400)
            new_platform = Platform(x, y, 75, 10, (0, 255, 0))
    
            #check if new platform overlaps with any existing platform
            is_overlapping = False
            for platform in platforms:
                if abs(new_platform.x - platform.x) < platform.width and abs(new_platform.y - platform.y) < platform.height:
                    is_overlapping = True
                    break
            
            #add new platform if it does not overlap with any existing platform
            if not is_overlapping:
                platforms.append(new_platform)

        #remove platforms that are off the screen
        for platform in platforms:
            if platform.y > 600:
                platforms.remove(platform)

#where all the drawing of objects is done
def redraw_game_window():   
    window.fill((0,0,0))
    for platform in platforms:
        platform.platform_draw()
    circle.circle_draw()
    pygame.display.update()

def main_game():
    run = True
    while(run):
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #calls the move function
        keys = pygame.key.get_pressed()
        circle.move(keys)

        #calls the function which will randomly generate platforms
        random_platform()

        redraw_game_window()
            
main_game()
pygame.quit()






