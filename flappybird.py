import pygame
import random
import sys

pygame.init()


WIDTH = 400
HEIGHT = 600


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)  
PURPLE = (128, 0, 128)  
RED = (255, 0, 0)


FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -8
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  


BIRD_SIZE = 30


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird with Random Controls")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

CONTROL_KEYS = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
CONTROL_KEY_NAMES = {
    pygame.K_UP: "UP",
    pygame.K_DOWN: "DOWN",
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT"
}


class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.vel_y = 0
        self.rect = pygame.Rect(self.x, self.y, BIRD_SIZE, BIRD_SIZE)

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y
        self.rect.y = self.y

    def jump(self):
        self.vel_y = JUMP_STRENGTH

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.top_rect = pygame.Rect(self.x, 0, 50, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, 50, HEIGHT - self.height - PIPE_GAP)

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen,PURPLE , self.top_rect)
        pygame.draw.rect(screen,PURPLE , self.bottom_rect)

    def off_screen(self):
        return self.x < -50


def start_screen(control_key):
    """Show start screen until first correct key is pressed"""
    waiting = True
    while waiting:
        screen.fill(BLACK)
        title_text = font.render("Flappy Bird Random Keys", True, WHITE)
        info_text = font.render(f"Press {CONTROL_KEY_NAMES[control_key]} to Start", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == control_key:
                    waiting = False


def main():
    bird = Bird()
    pipes = []
    score = 0
    last_pipe_time = pygame.time.get_ticks()

    current_control_key = random.choice(CONTROL_KEYS)
    key_change_time = pygame.time.get_ticks()

    
    start_screen(current_control_key)

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == current_control_key:
                    bird.jump()

        if pygame.time.get_ticks() - key_change_time > random.randint(3000, 5000):
            current_control_key = random.choice(CONTROL_KEYS)
            key_change_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - last_pipe_time > PIPE_FREQUENCY:
            pipes.append(Pipe(WIDTH))
            last_pipe_time = pygame.time.get_ticks()

        bird.update()

        for pipe in pipes:
            pipe.update()
            if pipe.off_screen():
                pipes.remove(pipe)
                score += 1

        for pipe in pipes:
            if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                running = False
        if bird.y > HEIGHT or bird.y < 0:
            running = False

        for pipe in pipes:
            pipe.draw()

        bird.draw()

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        control_text = font.render(f"Press: {CONTROL_KEY_NAMES[current_control_key]}", True, WHITE)
        screen.blit(control_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)

    game_over(score)


def game_over(score):
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 40))
    screen.blit(score_text, (WIDTH // 2 - 50, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    main()


if __name__ == "__main__":
    main()
