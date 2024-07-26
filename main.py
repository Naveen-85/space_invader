import pygame
import math
import random

# Initialize all pygame functions
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_Y = 480
PLAYER_SPEED = 2
SINE_ANGLE_INCREMENT = 1
ENEMY_WIDTH = 62
ENEMY_HEIGHT = 62
NUM_ENEMIES = 10
ENEMY_SPEED_X = 1
ENEMY_DESCENT = 10
ENEMY_SPEED_INCREMENT = 0.003

# Bullet variables
bullet_width = 32
bullet_height = 32
bullet_speed = 10
bullet_state = "ready"  # "ready" or "fire"

# Bullet list
bullets = []

# Score
score = 0

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
bullet_image = pygame.image.load('bullet original.png')

# Initial positions
playerX = (SCREEN_WIDTH - playerIm.get_width()) // 2
playerY = PLAYER_Y
playerX_change = 0
angle = 0

# Create a list of enemies
enemies = []
for i in range(NUM_ENEMIES):
    enemyX = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
    enemyY = random.randint(50, 150)
    speedX = random.choice([ENEMY_SPEED_X, -ENEMY_SPEED_X])
    enemies.append({'x': enemyX, 'y': enemyY, 'speedX': speedX, 'angle': random.uniform(0, 360)})

def draw_image(image, x, y):
    screen.blit(image, (x, y))

def draw_text(message, font_size, color, position):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(message, True, color)
    screen.blit(text_surface, position)

def handle_input():
    global playerX_change, bullet_state, bulletX, bulletY
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        playerX_change = -PLAYER_SPEED
    elif keys[pygame.K_RIGHT]:
        playerX_change = PLAYER_SPEED
    else:
        playerX_change = 0

    # Shoot bullet when space bar is pressed
    if keys[pygame.K_SPACE]:
        if bullet_state == "ready":
            bulletX = playerX + (playerIm.get_width() - bullet_width) // 2
            bulletY = playerY
            bullets.append({'x': bulletX, 'y': bulletY, 'active': True})
            bullet_state = "fire"

def fire_bullet():
    global bullet_state
    if bullet_state == "fire":
        for bullet in bullets:
            if bullet['active']:
                # Draw the bullet
                screen.blit(bullet_image, (bullet['x'] + 16, bullet['y'] + 10))
                bullet['y'] -= bullet_speed
                if bullet['y'] < 0:
                    bullet['active'] = False
        # Set bullet state to "ready" if no bullets are active
        if all(not b['active'] for b in bullets):
            bullet_state = "ready"

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
    if not enemies:  # Check if the enemies list is empty
        return True  # Indicate that all enemies are defeated

    for enemy in enemies:
        enemy['x'] += enemy['speedX']
        enemy['y'] += 0.1 * math.sin(math.radians(enemy['angle']))
        enemy['angle'] += SINE_ANGLE_INCREMENT

        # Reverse the enemy's direction when it goes off-screen
        if enemy['x'] > SCREEN_WIDTH - ENEMY_WIDTH or enemy['x'] < 0:
            enemy['speedX'] = -enemy['speedX']
            enemy['y'] += ENEMY_DESCENT
            ENEMY_SPEED_X += ENEMY_SPEED_INCREMENT

            # Adjust the speed for each enemy to ensure they maintain the same relative speed
            for e in enemies:
                e['speedX'] = ENEMY_SPEED_X if e['speedX'] > 0 else -ENEMY_SPEED_X

        # End the game if an enemy reaches the bottom of the screen
        if enemy['y'] >= playerY - ENEMY_HEIGHT:
            return True

    return False

def update_bullets():
    global score
    for bullet in bullets[:]:
        if bullet['active']:
            bullet['y'] -= bullet_speed

            # Check if the bullet has gone off-screen
            if bullet['y'] < 0:
                bullet['active'] = False
                continue

            # Check for collisions with enemies
            for enemy in enemies[:]:
                if (enemy['x'] < bullet['x'] + bullet_width < enemy['x'] + ENEMY_WIDTH or
                    enemy['x'] < bullet['x'] < enemy['x'] + ENEMY_WIDTH) and \
                   (enemy['y'] < bullet['y'] + bullet_height < enemy['y'] + ENEMY_HEIGHT or
                    enemy['y'] < bullet['y'] < enemy['y'] + ENEMY_HEIGHT):
                    enemies.remove(enemy)
                    bullet['active'] = False
                    score += 10  # Increase score by 10
                    break

def check_player_enemy_collision():
    for enemy in enemies:
        if (enemy['x'] < playerX + playerIm.get_width() < enemy['x'] + ENEMY_WIDTH or
            enemy['x'] < playerX < enemy['x'] + ENEMY_WIDTH) and \
           (enemy['y'] < playerY + playerIm.get_height() < enemy['y'] + ENEMY_HEIGHT or
            enemy['y'] < playerY < enemy['y'] + ENEMY_HEIGHT):
            return True
    return False

def draw_score():
    font = pygame.font.SysFont(None, 36)
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

def main():
    global angle, running

    running = True
    game_over_message = ""
    
    while running:
        screen.fill((0, 0, 0))  # Clear the screen
        screen.blit(background, (0, 0))  # Display the background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_input()
        update_player_position()
        game_over = update_enemy_positions()
        if check_player_enemy_collision():
            game_over_message = "Game Over!"
            running = False
        elif not enemies:  # If there are no enemies left
            game_over_message = "You Win!"
            running = False

        update_bullets()  # Update bullets for collision and movement
        fire_bullet()  # Draw the bullet if it is in the "fire" state

        angle += SINE_ANGLE_INCREMENT

        draw_image(playerIm, playerX, playerY)
        for bullet in bullets:
            if bullet['active']:
                draw_image(bullet_image, bullet['x'], bullet['y'])
        for enemy in enemies:
            draw_image(enemyIm, enemy['x'], enemy['y'])

        draw_score()

        if not running and game_over_message:  # Display game over message
            draw_text(game_over_message, 72, (255, 0, 0), (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        
        pygame.display.update()

    # Final screen loop to keep the game over message visible until the user closes the window
    final_screen = True
    while final_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                final_screen = False
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
