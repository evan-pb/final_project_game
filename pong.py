import pygame
import random as r

pygame.init()
pygame.display.set_caption("PONG")
WIDTH, LENGTH = 1000, 600
screen = pygame.display.set_mode((WIDTH, LENGTH))
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = "#62ff4a"
LIGHTGRAY = (100, 100, 100)
SPEED = 10
frame_count = 0
seconds = 00
minutes = 00

font = pygame.font.Font("ARCADECLASSIC.TTF", 30)

start_text = font.render("press any key to start", True, WHITE)
start_rect = start_text.get_rect()
start_rect.centerx, start_rect.centery = WIDTH // 2, LENGTH // 2

again_text_l = font.render("right  wins!", True, WHITE)
again_text_lrect = again_text_l.get_rect()
again_text_lrect.centerx, again_text_lrect.centery = WIDTH // 2, (LENGTH // 2) - 50

again_text_r = font.render("left  wins!", True, WHITE)
again_text_rrect = again_text_r.get_rect()
again_text_rrect.centerx, again_text_rrect.centery = WIDTH // 2, (LENGTH // 2) - 50

time_text = font.render("00  00", True, LIGHTGRAY)
time_rect = time_text.get_rect()
time_rect.centerx, time_rect.top = (WIDTH//2, 0)

playing = False


class Hearts(pygame.sprite.Sprite):
    def __init__(self) -> None:
        self.image = pygame.image.load("heart.png")
        self.rect = self.image.get_rect()

    def update(self):
        for i in range(left_lives):
            self.rect.topleft = (10 + 40 * i, 10)
            screen.blit(self.image, self.rect)
        for i in range(right_lives):
            self.rect.topleft = (958 - 40 * i, 10)
            screen.blit(self.image, self.rect)


class Ball:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(x, y, 10, 10)
        self.dx, self.dy = r.choice((SPEED, -SPEED)), r.choice((SPEED / 2, -SPEED / 2))
        self.left_lost, self.right_lost = False, False

    def update(self):
        if self.rect.colliderect(left_paddle.rect) or self.rect.colliderect(right_paddle.rect):
            self.dx = -self.dx
        if self.rect.top <= 0 or self.rect.bottom >= LENGTH:
            self.dy = -self.dy
        if self.rect.left <= 0:
            self.left_lost = True
        if self.rect.right >= WIDTH:
            self.right_lost = True
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def reset(self):
        global SPEED
        self.rect.x, self.rect.y = WIDTH // 2, LENGTH // 2
        self.dx, self.dy = r.choice((SPEED, -SPEED)), r.choice((SPEED / 2, -SPEED / 2))
        SPEED = 10


class Paddle:
    def __init__(self, x: int, y: int, side: bool) -> None:
        self.rect = pygame.rect.Rect(x, y, 20, 100)
        self.side = side

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.rect.top > 0 and self.side:
            self.rect.y -= SPEED
        if keys[pygame.K_s] and self.rect.bottom < LENGTH and self.side:
            self.rect.y += SPEED
        if keys[pygame.K_UP] and self.rect.top > 0 and not self.side:
            self.rect.y -= SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < LENGTH and not self.side:
            self.rect.y += SPEED

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


left_lives, right_lives = 5, 5
left_paddle = Paddle(50, 250, True)
right_paddle = Paddle(930, 250, False)
ball = Ball(WIDTH // 2, LENGTH // 2)
left_heart_group = pygame.sprite.Group()
right_heart_group = pygame.sprite.Group()
heart_left = Hearts()
heart_right = Hearts()


running = True
playing = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not playing:
            if event.key == pygame.K_ESCAPE:
                exec(open("main.py").read())

            else:
                playing = True
                time_text = font.render("00  00", True, LIGHTGRAY)
                ball.reset()
                left_paddle.rect.centery, right_paddle.rect.centery = (
                    LENGTH // 2,
                    LENGTH // 2,
                )
                left_lives, right_lives = 5, 5

    if left_lives == 0 or right_lives == 0:
        playing = False

    if ball.left_lost:
        ball.reset()
        left_lives -= 1
        heart_left.update()
        ball.left_lost = False
        # pygame.time.delay(500)

    if ball.right_lost:
        ball.reset()
        right_lives -= 1
        heart_right.update()
        ball.right_lost = False
        # pygame.time.delay(500)

    if not playing:
        screen.fill(BLACK)
        screen.blit(start_text, start_rect)
        seconds, minutes = 0, 0
        if left_lives == 0:
            screen.blit(again_text_l, again_text_lrect)
        if right_lives == 0:
            screen.blit(again_text_r, again_text_rrect)

    else:
        screen.fill(BLACK)
        for i in range(10):
            pygame.draw.rect(
                screen, WHITE, pygame.rect.Rect(WIDTH // 2 - 2, i * 62, 4, 40)
            )
        screen.blit(time_text, time_rect)
        left_paddle.draw()
        left_paddle.update()
        right_paddle.draw()
        right_paddle.update()
        ball.draw()
        ball.update()
        heart_left.update()
        heart_right.update()

    frame_count += 1
    if frame_count == 60:
        seconds += 1
        # if seconds == 30:
        #     SPEED += 2
        if seconds % 20 == 0:
            SPEED += 2
            minutes += 1
            seconds = 0
        if len(str(seconds)) == 1 and len(str(minutes)) == 1:
            time_text = font.render(f"0{minutes}  0{seconds}", True, LIGHTGRAY)
        elif len(str(seconds)) == 1 and len(str(minutes)) == 2:
            time_text = font.render(f"{minutes}  0{seconds}", True, LIGHTGRAY)
        elif len(str(seconds)) == 2 and len(str(minutes)) == 1:
            time_text = font.render(f"0{minutes}  {seconds}", True, LIGHTGRAY)
        else:
            time_text = font.render(f"{minutes}  {seconds}", True, LIGHTGRAY)
        frame_count = 0


    pygame.display.flip()
    clock.tick(60)
    



pygame.quit()
