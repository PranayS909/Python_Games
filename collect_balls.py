import pygame
import random
import sys
import cv2
import mediapipe as mp

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Player properties
player_width, player_height = 100, 20
player_y = HEIGHT - 50
player_x = WIDTH // 2 - player_width // 2

# Falling object properties
object_width, object_height = 30, 30
object_x = random.randint(0, WIDTH - object_width)
object_y = -object_height
object_speed = 5

# Score and font
score = 0
font = pygame.font.Font(None, 36)

# Game over flag
game_over = False

# Mediapipe Hand Detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

def get_index_finger_x():
    """Capture hand position and return the x-coordinate of the index finger."""
    ret, frame = cap.read()
    if not ret:
        return None
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the x-coordinate of the index finger tip (landmark 8)
            index_finger_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
            screen_x = int(index_finger_tip_x * WIDTH)
            return screen_x
    return None

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()

    if not game_over:
        # Get the x-coordinate of the index finger
        finger_x = get_index_finger_x()
        if finger_x is not None:
            player_x = finger_x - player_width // 2  # Center the rectangle on the finger

        # Clamp the player within screen bounds
        player_x = max(0, min(WIDTH - player_width, player_x))

        # Update falling object's position
        object_y += object_speed

        # Check for collision
        if (
            player_x < object_x + object_width
            and player_x + player_width > object_x
            and player_y < object_y + object_height
            and player_y + player_height > object_y
        ):
            score += 1
            object_x = random.randint(0, WIDTH - object_width)
            object_y = -object_height
            object_speed += 0.5  # Increase difficulty

        # Reset object if it goes off-screen
        if object_y > HEIGHT:
            game_over = True

    # Drawing
    screen.fill(WHITE)  # Clear screen
    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    else:
        # Draw player
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

        # Draw falling object
        pygame.draw.rect(screen, RED, (object_x, object_y, object_width, object_height))

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    # Restart game logic
    keys = pygame.key.get_pressed()
    if game_over and keys[pygame.K_r]:
        game_over = False
        score = 0
        object_x = random.randint(0, WIDTH - object_width)
        object_y = -object_height
        object_speed = 5

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
