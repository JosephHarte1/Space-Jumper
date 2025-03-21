import pygame
import random

pygame.init()

# Creates the pygame window
size = width, height = 700, 600
window = pygame.display.set_mode(size)
pygame.display.set_caption("PLATFORM JUMP")

clock = pygame.time.Clock()

# Game variables
MAX_PLATFORMS = 5  # Set the maximum number of platforms to generate
GRAVITY = 1
platforms = []
SCROLL_THRESHOLD = 300

# Player object class
class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 6
        self.isJump = True
        self.jumpCount = 10
        self.y_vel = 1

    def move(self, keys):
        if keys[pygame.K_a] and self.x - self.vel - self.radius >= 0:
            self.x -= self.vel
        if keys[pygame.K_d] and self.x + self.vel - self.radius <= 655:
            self.x += self.vel

        # Check for collisions with platforms
        for platform in platforms:
            if (self.y_vel >= 0  # Check only for downward movement
                and self.x + self.radius >= platform.x
                and self.x - self.radius <= platform.x + platform.width
                and self.y + self.radius >= platform.y
                and self.y - self.radius <= platform.y + platform.height
                and self.y + self.radius + self.y_vel >= platform.y):  # Check only for collision with top surface
                    self.isJump = False
                    self.jumpCount = 10
                    self.y_vel = -20
                # Update y-position and y-velocity
                
        if not self.isJump:
            self.isJump = True  # Automatically set isJump to True if not jumping
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


# Platform object class
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
        if (circle.y_vel >= 0  # Check only for downward movement
            and circle.x + circle.radius >= self.x
            and circle.x - circle.radius <= self.x + self.width
            and circle.y + circle.radius >= self.y
            and circle.y - circle.radius <= self.y + self.height):
            return True
        else:
            return False
            


# Creating the circle and platform objects
circle = Circle(250, 470, 20, (255, 0, 0))
platforms = [Platform(250, 470, 75, 10, (0, 255, 0))]


def random_platform():
    # Generate a new platform if there are fewer than MAX_PLATFORMS
    if len(platforms) < MAX_PLATFORMS:
        x = platforms[-1].x + random.randint(150, 250)  # Generate platforms ahead of the last platform
        y = random.randint(250, 550)
        new_platform = Platform(x, y, 75, 10, (0, 255, 0))
        platforms.append(new_platform)

    # Remove platforms that are off the screen
    for platform in platforms:
        if platform.x + platform.width < 0:
            platforms.remove(platform)


# Where all the drawing of objects is done
def redraw_game_window():
    # Adjust the position of the objects on the screen if the circle's y-position exceeds the scrolling threshold
    if circle.x > SCROLL_THRESHOLD:
        dx = SCROLL_THRESHOLD - circle.x
        circle.x += dx
        for platform in platforms:
            platform.x += dx

    # Draw the objects on the screen
    window.fill((0, 0, 0))
    for platform in platforms:
        platform.platform_draw()
    circle.circle_draw()
    pygame.display.update()


def main_game():
    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Calls the move function
        keys = pygame.key.get_pressed()
        circle.move(keys)

        # Calls the function which will randomly generate platforms
        random_platform()

        redraw_game_window()


main_game()
pygame.quit()
