import pygame
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
        self.isJump = True  # set isJump to True initially
        self.jumpCount = 10

    #player movements
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - self.vel - self.radius >= 0:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x + self.vel + self.radius <= 500:
            self.x += self.vel
        #allows the player to jump
        if not(self.isJump):
            self.isJump = True  # automatically set isJump to True if not jumping
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
    
    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

#creating the circle object
circle = Circle(250, 570, 30, (255, 0, 0))

#where all the drawing of objects is done
def redraw_game_window():
    window.fill((0,0,0))
    circle.draw()
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

        redraw_game_window()
        
main_game()
pygame.quit()





