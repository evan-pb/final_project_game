import pygame
import random as r

# pygame setup
pygame.init()
WIDTH, LENGTH = 1000, 600
screen = pygame.display.set_mode((WIDTH, LENGTH))
clock = pygame.time.Clock()

smallfont = pygame.font.Font("ARCADECLASSIC.TTF", 45)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
LIGHTGRAY = (100, 100, 100)

pong_button = smallfont.render("PONG", True, WHITE)
pong_rect = pong_button.get_rect()
pong_rect.center = WIDTH // 2, LENGTH // 2
pong_button_rect = pygame.rect.Rect(
    pong_rect.x - 20, pong_rect.y - 10, pong_rect.width + 40, pong_rect.height + 20
)

running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (
                pong_button_rect.left < mouse[0] < pong_button_rect.right
                and pong_button_rect.top < mouse[1] < pong_button_rect.bottom
            ):
                # Initialize pong game
                exec(open("pong.py").read())

    mouse = pygame.mouse.get_pos()

    screen.fill(BLACK)

    # RENDER GAME HERE

    # Make button highlight when hovered over

    if (
        pong_button_rect.left < mouse[0] < pong_button_rect.right
        and pong_button_rect.top < mouse[1] < pong_button_rect.bottom
    ):
        pygame.draw.rect(screen, GRAY, pong_button_rect)

    screen.blit(pong_button, pong_rect)

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
