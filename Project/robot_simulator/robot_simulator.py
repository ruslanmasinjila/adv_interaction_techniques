# ROBOT SIMULATOR FOR ADVANCED INTERACTION TECHNIQUES PROJECT

import pygame
import sys
import random
import math
import time
import numpy as np


# Initialize pygame
pygame.init()

# Constants
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
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
mode = "manual"  # Set mode to either "manual" or "automatic"
main_countdown_time = 45  # Main countdown timer in seconds

rand_low, rand_high = 3,11

#########################################################################################
# Manual mode variables

MAX_TARGETS_BEFORE_REPAIR_MANUAL = random.choice([i for i in range(rand_low, rand_high)])
remaining_targets_before_repair_manual = MAX_TARGETS_BEFORE_REPAIR_MANUAL
speed_manual = random.choice([i / 100 for i in range(rand_low, rand_high)])
repair_countdown_time_manual  = random.choice([i for i in range(rand_low, rand_high)])
cost_per_target_manual        = random.choice([i for i in range(rand_low, rand_high)])
cost_for_all_targets_manual   = 0
total_targets_acquired_manual = 0
total_repair_time_manual      = 0
live_active_time_manual       = 0
last_time_manual = None  # Tracks the last timestamp when manual mode was active

#########################################################################################

# Automatic mode variables
MAX_TARGETS_BEFORE_REPAIR_AUTOMATIC = random.choice([i for i in range(rand_low, rand_high)])
remaining_targets_before_repair_automatic = MAX_TARGETS_BEFORE_REPAIR_AUTOMATIC
speed_automatic = random.choice([i / 100 for i in range(rand_low, rand_high)])
repair_countdown_time_automatic  = random.choice([i for i in range(rand_low, rand_high)])
cost_per_target_automatic        = random.choice([i for i in range(rand_low, rand_high)])
cost_for_all_targets_automatic   = 0
total_targets_acquired_automatic = 0
total_repair_time_automatic      = 0
live_active_time_automatic       = 0
last_time_automatic = None  # Tracks the last timestamp when automatic mode was active

#######################################################################################
variance = np.var(range(3,11))



# Repair variables
repairing = False
repair_start_time = None
main_timer_start = time.time()  # Start time of the main countdown
paused_time = None  # Tracks paused time during repairs

# Create display
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pygame Robot Game")

# Font for displaying mode and messages
font = pygame.font.SysFont(None, 34)



# Function to display the repair message
def show_repair_message(screen, font, countdown):
    message = f"Repairing Robot, please wait... {countdown}s"
    text = font.render(message, True, (255, 0, 0))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)

# Function to calculate remaining time for the main countdown
def calculate_main_timer(main_timer_start, paused_time):
    if paused_time is not None:
        return main_countdown_time - paused_time
    else:
        return main_countdown_time - (time.time() - main_timer_start)

# Main game loop
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            robot_rect.center = (WIDTH // 2, HEIGHT // 2)
            target_rect.center = (random.randint(50, WIDTH - 100), random.randint(50, HEIGHT - 100))

        # Mode switching with keyboard (only if not repairing)
        if event.type == pygame.KEYDOWN and not repairing:
            if event.key == pygame.K_m:
                mode = "manual"
                last_time_automatic = None  # Stop tracking time for automatic mode
                last_time_manual = time.time()  # Start tracking time for automatic mode
            elif event.key == pygame.K_a:
                mode = "automatic"
                last_time_manual = None  # Stop tracking time for automatic mode
                last_time_automatic = time.time()  # Start tracking time for automatic mode

        # Manual mode: check for mouse button press over robot
        if mode == "manual" and not repairing:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if robot_rect.collidepoint(event.pos):
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

    # Countdown logic
    if repairing:
        last_time_manual    = None  # Stop tracking time for manual mode
        last_time_automatic = None  # Stop tracking time for automatic mode
        elapsed_time = time.time() - repair_start_time
        remaining_repair_time = (
            repair_countdown_time_manual if mode == "manual" else repair_countdown_time_automatic
        ) - int(elapsed_time)

        if remaining_repair_time <= 0:
            repairing = False
            remaining_targets_before_repair_manual = MAX_TARGETS_BEFORE_REPAIR_MANUAL
            remaining_targets_before_repair_automatic = MAX_TARGETS_BEFORE_REPAIR_AUTOMATIC
            main_timer_start = time.time() - (paused_time if paused_time else 0)
            paused_time = None
            if(mode=="manual"):
                total_repair_time_manual    +=repair_countdown_time_manual
            else:
                total_repair_time_automatic +=repair_countdown_time_automatic
                
        else:
            show_repair_message(screen, font, remaining_repair_time)
            pygame.display.flip()
            pygame.time.Clock().tick(60)
            continue

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

        if distance > 1:
            dx, dy = dx / distance, dy / distance
            robot_rect.centerx += dx * distance * speed_manual
            robot_rect.centery += dy * distance * speed_manual
            angle = math.degrees(math.atan2(-dy, dx))
            rotated_robot = pygame.transform.rotate(robot_image, angle)
            rotated_rect = rotated_robot.get_rect(center=robot_rect.center)
            screen.blit(rotated_robot, rotated_rect.topleft)

    # Automatic mode: Robot moves on its own toward target
    elif mode == "automatic":
        dx, dy = target_rect.centerx - robot_rect.centerx, target_rect.centery - robot_rect.centery
        distance = math.hypot(dx, dy)

        if distance > 1:
            dx, dy = dx / distance, dy / distance
            robot_rect.centerx += dx * distance * speed_automatic
            robot_rect.centery += dy * distance * speed_automatic
            angle = math.degrees(math.atan2(-dy, dx))
            rotated_robot = pygame.transform.rotate(robot_image, angle)
            rotated_rect = rotated_robot.get_rect(center=robot_rect.center)
            screen.blit(rotated_robot, rotated_rect.topleft)

    else:
        screen.blit(robot_image, robot_rect)

    # Check collision with target
    if robot_rect.colliderect(target_rect):
        target_rect.topleft = (random.randint(50, WIDTH - 100), random.randint(50, HEIGHT - 100))
        if mode == "manual":
            remaining_targets_before_repair_manual -= 1
            total_targets_acquired_manual += 1
            cost_for_all_targets_manual   += cost_per_target_manual
        else:
            remaining_targets_before_repair_automatic -= 1
            total_targets_acquired_automatic += 1
            cost_for_all_targets_automatic   += cost_per_target_automatic

        if remaining_targets_before_repair_manual <= 0 or remaining_targets_before_repair_automatic <= 0:
            repairing = True
            repair_start_time = time.time()
            paused_time = time.time() - main_timer_start
            dragging = False

    # Track time spent in automatic mode
    if mode == "automatic" and not repairing:
        last_time_manual = None
        if last_time_automatic is not None:
            live_active_time_automatic += time.time() - last_time_automatic
        last_time_automatic = time.time()
        

    if mode == "manual" and not repairing:
        last_time_automatic = None 
        if last_time_manual is not None:
            live_active_time_manual += time.time() - last_time_manual
        last_time_manual = time.time()

    # Draw target
    screen.blit(target_image, target_rect)

    # Display mode and main timer
    mode_text = font.render(
        f"Current Mode: {mode.capitalize()} [Press 'M' for Manual, 'A' for Automatic]. Press ESC to End simulation", True, (0, 0, 0)
    )
    timer_text = font.render(f"Time Left: {int(remaining_main_time)}s", True, (0, 0, 0))

    manual_mode_time_text       = font.render(f"Manual       Mode: | Active Time={int(live_active_time_manual)}s | Repair Time = {total_repair_time_manual} | Targets={total_targets_acquired_manual} | Cost= ${cost_for_all_targets_manual}", 
                                              True, 
                                              (0, 0, 0))
    
    automatic_mode_time_text    = font.render(f"Automatic Mode: | Active Time={int(live_active_time_automatic)}s | Repair Time = {total_repair_time_automatic} | Targets={total_targets_acquired_automatic} | Cost = ${cost_for_all_targets_automatic}", 
                                              True, 
                                              (0, 0, 0))


    screen.blit(mode_text, (10, 10))
    screen.blit(timer_text, (10, 40))
    screen.blit(automatic_mode_time_text, (10, 70))     # Below timer text
    screen.blit(manual_mode_time_text, (10, 100))       # Below automatic mode text

    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(60)
