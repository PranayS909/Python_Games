import pygame
import random
import sounddevice as sd
import numpy as np

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Game variables
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 30)

# Bird properties
bird_x = 50
bird_y = 300
bird_radius = 15
bird_velocity = 0
gravity = 0.5
flap_strength = -5

# Pipe properties
pipe_width = 60
pipe_gap = 150
pipe_velocity = 4
pipe_color = GREEN
pipes = []
spawn_pipe_event = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe_event, 1500)

# Game state
score = 0
game_over = False
volume_norm = 0  # Initialize sound level variable


def audio_callback(indata, frames, time, status):
    """Audio callback to capture sound and calculate volume."""
    global volume_norm
    if status:
        print(status)
    # Calculate volume level (RMS)
    volume_norm = np.linalg.norm(indata) * 10


# Set up sound detection stream
stream = sd.InputStream(callback=audio_callback)
stream.start()


def draw_bird(x, y):
    pygame.draw.circle(screen, RED, (x, y), bird_radius)


def draw_pipes(pipes):
    for pipe in pipes:
        pipe_top = pygame.Rect(pipe['x'], 0, pipe_width, pipe['height'])
        pipe_bottom = pygame.Rect(pipe['x'], pipe['height'] + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe['height'] - pipe_gap)
        pygame.draw.rect(screen, pipe_color, pipe_top)
        pygame.draw.rect(screen, pipe_color, pipe_bottom)


def check_collision(bird_y, pipes):
    for pipe in pipes:
        if bird_x + bird_radius > pipe['x'] and bird_x - bird_radius < pipe['x'] + pipe_width:
            if bird_y - bird_radius < pipe['height'] or bird_y + bird_radius > pipe['height'] + pipe_gap:
                return True
    if bird_y - bird_radius < 0 or bird_y + bird_radius > SCREEN_HEIGHT:
        return True
    return False


def display_text(text, x, y, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


# Game loop
running = True
while running:
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_pipe_event and not game_over:
            pipe_height = random.randint(100, 300)
            pipes.append({'x': SCREEN_WIDTH, 'height': pipe_height})
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:  # Restart game
                game_over = False
                bird_y = 300
                bird_velocity = 0
                pipes = []
                score = 0

    if not game_over:
        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity

        # Sound-based flap
        if volume_norm > 10:
            bird_velocity = flap_strength

        # Pipe movement
        for pipe in pipes:
            pipe['x'] -= pipe_velocity

        # Remove pipes that are off-screen
        pipes = [pipe for pipe in pipes if pipe['x'] + pipe_width > 0]

        # Check for collisions
        if check_collision(bird_y, pipes):
            game_over = True

        # Scoring
        for pipe in pipes:
            if pipe['x'] + pipe_width == bird_x:
                score += 1

    # Drawing
    draw_bird(bird_x, bird_y)
    draw_pipes(pipes)
    display_text(f"Score: {score}", 10, 10)

    if game_over:
        display_text("Game Over!", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 30, RED)
        display_text("Press R to Restart", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20, BLACK)

    pygame.display.flip()
    clock.tick(30)

stream.stop()
stream.close()
pygame.quit()
