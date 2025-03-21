import pygame
import random

pygame.init()

#creates the pygame window
size = width, height = 700, 600
window = pygame.display.set_mode(size)
pygame.display.set_caption("PLATFORM JUMP")

clock = pygame.time.Clock()

#Game variables
MAX_PLATFORMS = 7  #set the maximum number of platforms to generate
GRAVITY = 1.1
platforms = []
SCROLL_THRESHOLD = 300

#player object class
class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 5
        self.isJump = True 
        self.jumpCount = 10
        self.y_vel = 1  
    
    def move(self, keys):
        if keys[pygame.K_a] and self.x - self.vel - self.radius>= 0:
            self.x -= self.vel
        if keys[pygame.K_d] and self.x + self.vel - self.radius <= 655:
            self.x += self.vel
        
        #check for collisions with platforms
        for platform in platforms:
            if (self.y_vel >= 0 and  #check only for downward movement
                self.x + self.radius >= platform.x and
                self.x - self.radius <= platform.x + platform.width and
                self.y + self.radius >= platform.y and
                self.y - self.radius <= platform.y + platform.height and
                self.y + self.radius + self.y_vel >= platform.y):  #check only for collision with top surface
                    self.isJump = False
                    self.jumpCount = 10
                    self.y_vel = -20 
                #update y-position and y-velocity

        if not(self.isJump):
            self.isJump = True  #automatically set isJump to True if not jumping
        else:
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
        if (circle.y_vel >= 0 and  #check only for downward movement
            circle.x + circle.radius >= self.x and
            circle.x - circle.radius <= self.x + self.width and
            circle.y + circle.radius >= self.y and
            circle.y - circle.radius <= self.y + self.height):
            return True
        else:
            return False

#creating the circle and platform objects
circle = Circle(250, 470, 20, (255, 0, 0))
#create a list of platforms
platforms = [Platform(213, 470, 75, 10, (0, 255, 0)), 
             Platform(100, 450, 75, 10, (0, 255, 0)), 
             Platform(300, 350, 75, 10, (0, 255, 0))]

def random_platform(platforms):
    #generate a new platform if there are fewer than MAX_PLATFORMS
    if len(platforms) < MAX_PLATFORMS:
        x = random.randint(circle.x+100, 550)
        y = random.randint(150, 450)
        new_platform = Platform(x, y, 75, 10, (0, 255, 0))

        #check if new platform overlaps with any existing platform or the circle
        is_overlapping = False
        for platform in platforms:
            if abs(new_platform.x - platform.x) < platform.width and abs(new_platform.y - platform.y) < platform.height:
                is_overlapping = True
                break
        if abs(new_platform.x - circle.x) < circle.radius and abs(new_platform.y - circle.y) < circle.radius:
            is_overlapping = True

        #add new platform if it does not overlap with any existing platform or the circle
        if not is_overlapping:
            if new_platform.collides_with_circle(circle):
                is_overlapping = True
            platforms.append(new_platform)

    #remove platforms that are off the screen
    for platform in platforms:
        if (platform.x + platform.width) < 0:
            x = platforms.index(platform)
            platforms.pop(x)
            
        

#where all the drawing of objects is done
def redraw_game_window():

    # adjust the position of the objects on the screen if the circle's y-position exceeds the scrolling threshold
    if circle.x > SCROLL_THRESHOLD:
        dx = SCROLL_THRESHOLD - circle.x
        circle.x += dx
        for platform in platforms:
            platform.x += dx

    # draw the objects on the screen
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
        random_platform(platforms)

        redraw_game_window()
            
main_game()
pygame.quit()






