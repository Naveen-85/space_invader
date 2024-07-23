import pygame
import math
import random

# Initialize all pygame functions
pygame.init()

# Constants
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 600
PLAYER_Y = 500
PLAYER_SPEED = 0.5
SINE_ANGLE_INCREMENT = 1
ENEMY_WIDTH = 62  # Assuming enemy image width is 62 pixels
ENEMY_HEIGHT = 62  # Assuming enemy image height is 62 pixels
NUM_ENEMIES = 10
ENEMY_SPEED_X = 0.1
ENEMY_DESCENT = 10
ENEMY_Y_BASE = 50
ENEMY_SPEED_INCREMENT = 0.003

# Create our screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Real title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# Load images
playerIm = pygame.image.load('otaku.png')
enemyIm = pygame.image.load('oni.png')
background = pygame.image.load('space_ia.jpg')

# Initial positions
playerX = 350
playerY = PLAYER_Y
playerX_change = 0
angle = 0

# Create a list of enemies
enemies = []
for i in range(NUM_ENEMIES):
    enemyX = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
    enemyY = random.randint(25, 75)
    speedX = random.choice([ENEMY_SPEED_X, -ENEMY_SPEED_X])
    enemies.append({'x': enemyX, 'y': enemyY, 'speedX': speedX, 'angle': random.uniform(0, 360)})

def draw_image(image, x, y):
    screen.blit(image, (x, y))

def handle_input():
    global playerX_change
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        playerX_change = -PLAYER_SPEED
    elif keys[pygame.K_RIGHT]:
        playerX_change = PLAYER_SPEED
    else:
        playerX_change = 0

def update_player_position():
    global playerX, playerY
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > SCREEN_WIDTH - playerIm.get_width():
        playerX = SCREEN_WIDTH - playerIm.get_width()
    playerY = PLAYER_Y + 25 * math.sin(math.radians(angle))

def update_enemy_positions():
    global ENEMY_SPEED_X
    for enemy in enemies:
        enemy['x'] += enemy['speedX']
        enemy['y'] += 0.1 * math.sin(math.radians(enemy['angle']))
        enemy['angle'] += SINE_ANGLE_INCREMENT

        # Reverse the enemy's direction when it goes off-screen
        if enemy['x'] > SCREEN_WIDTH - ENEMY_WIDTH or enemy['x'] < 0:
            enemy['speedX'] = -enemy['speedX']
            enemy['y'] += ENEMY_DESCENT  # Descend when hitting a wall
            ENEMY_SPEED_X += ENEMY_SPEED_INCREMENT  # Increase the speed

            # Adjust the speed for each enemy to ensure they maintain the same relative speed
            for e in enemies:
                e['speedX'] = ENEMY_SPEED_X if e['speedX'] > 0 else -ENEMY_SPEED_X

        # End the game if an enemy reaches the bottom of the screen
        if enemy['y'] >= playerY - ENEMY_HEIGHT:
            return True
    return False

def main():
    global angle, running

    running = True
    while running:
        screen.fill((100, 200, 0))
        # Background image
        #screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_input()
        update_player_position()
        game_over = update_enemy_positions()
        angle += SINE_ANGLE_INCREMENT

        draw_image(playerIm, playerX, playerY)
        for enemy in enemies:
            draw_image(enemyIm, enemy['x'], enemy['y'])

        pygame.display.update()

        if game_over:
            print("Game Over!")
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
