import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

class Bird:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.gravity = 0.6
        self.lift = -15
        self.velocity = 0

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.velocity = 0

        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def flap(self):
        self.velocity += self.lift

class Pipe:
    def __init__(self):
        self.width = 50
        self.x = SCREEN_WIDTH
        self.gap = 200
        self.height = random.randint(100, SCREEN_HEIGHT - self.gap - 100)
        self.top_height = self.height
        self.bottom_height = SCREEN_HEIGHT - self.height - self.gap

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, GREEN, (self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height))

    def update(self):
        self.x -= 5

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = [Pipe()]
        self.score = 0

    def draw(self):
        screen.fill(BLUE)
        self.bird.draw()
        for pipe in self.pipes:
            pipe.draw()
        self.draw_score()

    def update(self):
        self.bird.update()
        for pipe in self.pipes:
            pipe.update()
            if pipe.x + pipe.width < 0:
                self.pipes.remove(pipe)
                self.pipes.append(Pipe())
                self.score += 1

        # Check for collisions
        if self.check_collision():
            self.game_over()

    def check_collision(self):
        for pipe in self.pipes:
            if self.bird.x + self.bird.width > pipe.x and self.bird.x < pipe.x + pipe.width:
                if self.bird.y < pipe.top_height or self.bird.y + self.bird.height > SCREEN_HEIGHT - pipe.bottom_height:
                    return True
        return False

    def draw_score(self):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    def game_over(self):
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        self.__init__()

def main():
    game = Game()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.bird.flap()

        game.update()
        game.draw()
        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
