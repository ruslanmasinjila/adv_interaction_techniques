import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)

# Load images
robot_image = pygame.image.load("robot.jpeg")
target_image = pygame.image.load("target.jpg")

# Scale images for consistency
robot_image = pygame.transform.scale(robot_image, (50, 50))
target_image = pygame.transform.scale(target_image, (30, 30))

# Get rects for positioning
robot_rect = robot_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
target_rect = target_image.get_rect(center=(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))

# Initialize variables
dragging = False
speed = 0.1  # Speed factor for moving robot

# Create display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Robot Game")

# Main game loop
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for mouse button press over robot
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if robot_rect.collidepoint(event.pos):
                dragging = True

        # Release mouse button
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        # Adjust speed with scroll
        elif event.type == pygame.MOUSEWHEEL:
            speed = max(0.05, speed + 0.05 * event.y)  # Increase or decrease speed, with minimum limit

    # Move robot if dragging
    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx, dy = mouse_x - robot_rect.centerx, mouse_y - robot_rect.centery
        distance = math.hypot(dx, dy)

        if distance > 1:  # Only move if there's a distance
            dx, dy = dx / distance, dy / distance  # Normalize direction
            robot_rect.centerx += dx * distance * speed
            robot_rect.centery += dy * distance * speed

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

    # Draw target
    screen.blit(target_image, target_rect)

    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(60)
