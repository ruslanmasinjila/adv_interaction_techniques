import pygame
import sys
import random
import math
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)

# Load images
robot_image = pygame.image.load("robot.jpeg")
target_image = pygame.image.load("target.jpg")

# Scale images for consistency
robot_image = pygame.transform.scale(robot_image, (100, 100))
target_image = pygame.transform.scale(target_image, (50, 50))

# Get rects for positioning
robot_rect = robot_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
target_rect = target_image.get_rect(center=(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))

# Initialize variables
dragging = False
speed_manual_mode = 0.005
speed_automatic_mode = 0.1
mode = "manual"  # Set mode to either "manual" or "automatic"
manual_count = 10
automatic_count = 5
countdown_time = 5  # Countdown duration in seconds
repairing = False
repair_start_time = None

# Create display
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pygame Robot Game")

# Font for displaying mode and messages
font = pygame.font.SysFont(None, 50)

# Function to display the countdown
def show_repair_message(screen, font, countdown):
    message = f"Repairing Robot, please wait... {countdown}s"
    text = font.render(message, True, (255, 0, 0))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)

# Main game loop
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mode switching with keyboard (only if not repairing)
        elif event.type == pygame.KEYDOWN and not repairing:
            if event.key == pygame.K_m:
                mode = "manual"
            elif event.key == pygame.K_a:
                mode = "automatic"

        # Manual mode: check for mouse button press over robot
        elif mode == "manual" and not repairing:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if robot_rect.collidepoint(event.pos):
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

    # Countdown logic
    if repairing:
        elapsed_time = time.time() - repair_start_time
        remaining_time = countdown_time - int(elapsed_time)

        if remaining_time <= 0:
            repairing = False
            # Reset counters after repair
            manual_count = 10
            automatic_count = 5
        else:
            show_repair_message(screen, font, remaining_time)
            pygame.display.flip()
            pygame.time.Clock().tick(60)
            continue  # Skip the rest of the loop during repair

    # Manual mode: Move robot if dragging
    if mode == "manual" and dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx, dy = mouse_x - robot_rect.centerx, mouse_y - robot_rect.centery
        distance = math.hypot(dx, dy)

        if distance > 1:  # Only move if there's a distance
            dx, dy = dx / distance, dy / distance  # Normalize direction
            robot_rect.centerx += dx * distance * speed_manual_mode
            robot_rect.centery += dy * distance * speed_manual_mode

            # Rotate robot image in direction of movement
            angle = math.degrees(math.atan2(-dy, dx))  # Invert y-axis for correct angle
            rotated_robot = pygame.transform.rotate(robot_image, angle)
            rotated_rect = rotated_robot.get_rect(center=robot_rect.center)
            screen.blit(rotated_robot, rotated_rect.topleft)

    # Automatic mode: Robot moves on its own toward target
    elif mode == "automatic":
        dx, dy = target_rect.centerx - robot_rect.centerx, target_rect.centery - robot_rect.centery
        distance = math.hypot(dx, dy)

        if distance > 1:  # Only move if there's a distance
            dx, dy = dx / distance, dy / distance  # Normalize direction
            robot_rect.centerx += dx * speed_automatic_mode * 10
            robot_rect.centery += dy * speed_automatic_mode * 10

            # Rotate robot image in direction of movement
            angle = math.degrees(math.atan2(-dy, dx))  # Invert y-axis for correct angle
            rotated_robot = pygame.transform.rotate(robot_image, angle)
            rotated_rect = rotated_robot.get_rect(center=robot_rect.center)
            screen.blit(rotated_robot, rotated_rect.topleft)

    else:
        # If not dragging, just display the robot without movement
        screen.blit(robot_image, robot_rect)

    # Check collision with target
    if robot_rect.colliderect(target_rect):
        target_rect.topleft = (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        if mode == "manual":
            manual_count -= 1
        else:
            automatic_count -= 1

        if manual_count <= 0 or automatic_count <= 0:
            repairing = True
            repair_start_time = time.time()
            dragging = False  # Reset dragging state

    # Draw target
    screen.blit(target_image, target_rect)

    # Display mode
    mode_text = font.render(f"Mode: {mode.capitalize()} (Press 'M' for Manual, 'A' for Automatic)", True, (0, 0, 0))
    screen.blit(mode_text, (10, 10))

    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

