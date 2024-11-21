import pygame
import sys
import random
import math
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1500, 800
WHITE = (255, 255, 255)

# Load images
robot_image = pygame.image.load("robot.jpeg")
target_image = pygame.image.load("target.jpg")

# Scale images for consistency
robot_image = pygame.transform.scale(robot_image, (100, 100))
target_image = pygame.transform.scale(target_image, (50, 50))

# Get rects for positioning
robot_rect = robot_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
target_rect = target_image.get_rect(center=(random.randint(50, WIDTH - 100), random.randint(50, HEIGHT - 100)))

# Initialize variables
dragging = False
mode     = "manual"  # Set mode to either "manual" or "automatic"

#########################################################################

MAX_TARGETS_BEFORE_REPAIR_MANUAL        = random.choice([i for i in range(5, 12)])
remaining_targets_before_repair_manual  = MAX_TARGETS_BEFORE_REPAIR_MANUAL
speed_manual                            = random.choice([i / 100 for i in range(1, 8)])

#########################################################################


MAX_TARGETS_BEFORE_REPAIR_AUTOMATIC = random.choice([i for i in range(5, 12)])
remaining_targets_before_repair_automatic = MAX_TARGETS_BEFORE_REPAIR_AUTOMATIC
speed_automatic    = random.choice([i / 10 for i in range(1, 8)])


#########################################################################

main_countdown_timer = 60  # Main countdown timer in seconds
repair_countdown_time = 5  # Repair countdown duration in seconds
repairing = False
repair_start_time = None
main_timer_start = time.time()  # Start time of the main countdown

# Create display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Pygame Robot Game")

# Font for displaying mode and messages
font = pygame.font.SysFont(None, 50)

# Function to display the repair message
def show_repair_message(screen, font, countdown):
    message = f"Repairing Robot, please wait... {countdown}s"
    text = font.render(message, True, (255, 0, 0))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)

# Function to calculate remaining time for the main countdown
def calculate_main_timer(main_timer_start, paused_time):
    if paused_time is not None:
        return main_countdown_timer - paused_time
    else:
        return main_countdown_timer - (time.time() - main_timer_start)

# Main game loop
paused_time = None  # Tracks paused time during repairs

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle ESC key for quitting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # Mode switching with keyboard (only if not repairing)
        if event.type == pygame.KEYDOWN and not repairing:
            if event.key == pygame.K_m:
                mode = "manual"
            elif event.key == pygame.K_a:
                mode = "automatic"

        # Manual mode: check for mouse button press over robot
        if mode == "manual" and not repairing:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if robot_rect.collidepoint(event.pos):
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

    # Countdown logic
    if repairing:
        elapsed_time = time.time() - repair_start_time
        remaining_repair_time = repair_countdown_time - int(elapsed_time)

        if remaining_repair_time <= 0:
            repairing = False
            remaining_targets_before_repair_manual      = MAX_TARGETS_BEFORE_REPAIR_MANUAL
            remaining_targets_before_repair_automatic   = MAX_TARGETS_BEFORE_REPAIR_AUTOMATIC
            main_timer_start = time.time() - (paused_time if paused_time else 0)  # Resume main timer
            paused_time = None
        else:
            show_repair_message(screen, font, remaining_repair_time)
            pygame.display.flip()
            pygame.time.Clock().tick(60)
            continue  # Skip the rest of the loop during repair

    # Main countdown timer
    remaining_main_time = calculate_main_timer(main_timer_start, paused_time)
    if remaining_main_time <= 0:
        game_over_text = font.render("Game Over! Time's up!", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # Manual mode: Move robot if dragging
    if mode == "manual" and dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx, dy = mouse_x - robot_rect.centerx, mouse_y - robot_rect.centery
        distance = math.hypot(dx, dy)

        if distance > 1:  # Only move if there's a distance
            dx, dy = dx / distance, dy / distance  # Normalize direction
            robot_rect.centerx += dx * distance * speed_manual
            robot_rect.centery += dy * distance * speed_manual

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
            robot_rect.centerx += dx * speed_automatic * 10
            robot_rect.centery += dy * speed_automatic * 10

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
        target_rect.topleft = (random.randint(50, WIDTH - 100), random.randint(50, HEIGHT - 100))
        if mode == "manual":
            remaining_targets_before_repair_manual -= 1
        else:
            remaining_targets_before_repair_automatic -= 1

        if remaining_targets_before_repair_manual <= 0 or remaining_targets_before_repair_automatic <= 0:
            repairing = True
            repair_start_time = time.time()
            paused_time = time.time() - main_timer_start  # Pause main timer
            dragging = False  # Reset dragging state

    # Draw target
    screen.blit(target_image, target_rect)

    # Display mode and main timer
    mode_text = font.render(f"Mode: {mode.capitalize()} (Press 'M' for Manual, 'A' for Automatic)", True, (0, 0, 0))
    timer_text = font.render(f"Time Left: {int(remaining_main_time)}s", True, (0, 0, 0))
    screen.blit(mode_text, (10, 10))
    screen.blit(timer_text, (10, 60))

    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

