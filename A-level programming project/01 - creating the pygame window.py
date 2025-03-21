import pygame
pygame.init()

#creates the pygame window
size = width, height = 500, 800

window = pygame.display.set_mode(size)
pygame.display.set_caption("PLATFORM JUMP")

clock = pygame.time.Clock()

def redraw_game_window():
    window.fill((0,0,0))
    pygame.display.update()

def main_game():
    run = True
    while(run):
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redraw_game_window()

main_game()
pygame.quit()
