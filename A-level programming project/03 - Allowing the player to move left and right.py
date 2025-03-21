import pygame
pygame.init()

#creates the pygame window
size = width, height = 500, 800

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
    
    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

#creating the circle object
circle = Circle(250, 400, 30, (255, 0, 0))
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
        #Player Movements (LEFT and Right)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            circle.x -= circle.vel
        if keys[pygame.K_RIGHT]:
            circle.x += circle.vel
        
        redraw_game_window()

       
main_game()
pygame.quit()

