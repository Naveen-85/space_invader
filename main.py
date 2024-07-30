import pygame
import math
import random
from pygame import mixer

# Initialize all pygame functions
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_Y = 480
PLAYER_SPEED = 0.5
SINE_ANGLE_INCREMENT = 1
ENEMY_WIDTH = 62
ENEMY_HEIGHT = 62
NUM_ENEMIES = 10
ENEMY_SPEED_X = 0.5
ENEMY_DESCENT = 10
ENEMY_SPEED_INCREMENT = 0.001
ENEMY_LIFE = 2
MAX_LEVELS = 3

BOSS_LIFE = 10
BOSS_SPEED_X = 0.2
BOSS_SHOOT_INTERVAL = 2000  # Boss shoots every 2 seconds

# Bullet variables
bullet_width = 16
bullet_height = 16
bullet_speed = 2
bullet_state = "ready"  # "ready" or "fire"

# Bullet list
bullets = []

# Boss bullet variables
boss_bullets = []

# Score
score = 0

# Level
level = 3

# Create our screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Real title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)

# Load images
<<<<<<< Updated upstream
playerIm = pygame.image.load('otaku.png')
enemyIm1 = pygame.image.load('oni.png')
enemyIm2 = pygame.image.load('oni2.png')
bossIm = pygame.image.load('oni_boss.png')
background = pygame.image.load('space_ia.jpg')
bullet_image = pygame.image.load('bullet original.png')
boss_bullet_image = pygame.image.load('bullet original.png')
=======
playerIm = pygame.image.load("otaku.png")
enemyIm1 = pygame.image.load("oni.png")
enemyIm2 = pygame.image.load("oni2.png")
bossIm = pygame.image.load("oni_boss.png")
background = pygame.image.load("space_ia.jpg")
bullet_image = pygame.image.load("bullet.png")
boss_bullet_image = pygame.image.load("bullet.png")
>>>>>>> Stashed changes

# Adding Background music
mixer.music.load("background.wav")
mixer.music.play(-1)
collision_sound = mixer.Sound("explosion.wav")
level_up_sound = mixer.Sound("background.wav")

# Initial positions
playerX = (SCREEN_WIDTH - playerIm.get_width()) // 2
playerY = PLAYER_Y
playerX_change = 0
angle = 0


# Create a list of enemies
def create_enemies(num_enemies, level):
    enemies = []
    for _ in range(num_enemies):
        enemyX = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        enemyY = random.randint(50, 150)
        speedX = random.choice([ENEMY_SPEED_X, -ENEMY_SPEED_X])
        life = ENEMY_LIFE + level - 1  # Increment life with level
        image = (
            enemyIm1 if life < 3 else enemyIm2
        )  # Change image if life is 4 or higher
        enemies.append(
            {
                "x": enemyX,
                "y": enemyY,
                "speedX": speedX,
                "angle": random.uniform(0, 360),
                "life": life,
                "image": image,
            }
        )
    return enemies


# Create boss enemy
def create_boss():
    return [
        {
            "x": (SCREEN_WIDTH - ENEMY_WIDTH) // 2,
            "y": 50,
            "angle": random.uniform(0, 360),
            "speedX": BOSS_SPEED_X,
            "life": BOSS_LIFE,
            "image": bossIm,
        }
    ]


enemies = create_enemies(NUM_ENEMIES, level)
boss = create_boss()


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

    if keys[pygame.K_SPACE]:
        if bullet_state == "ready":
            bullet_sound = mixer.Sound("laser.wav")
            bullet_sound.play()
            bulletX = playerX + (playerIm.get_width() - bullet_width) // 2
            bulletY = playerY
            bullets.append({"x": bulletX, "y": bulletY, "active": True})
            bullet_state = "fire"


def fire_bullet():
    global bullet_state
    if bullet_state == "fire":
        for bullet in bullets:
            if bullet["active"]:
                screen.blit(bullet_image, (bullet["x"] + 16, bullet["y"] + 10))
                bullet["y"] -= bullet_speed
                if bullet["y"] < 0:
                    bullet["active"] = False
        if all(not b["active"] for b in bullets):
            bullet_state = "ready"


def update_player_position():
    global playerX, playerY
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > SCREEN_WIDTH - playerIm.get_width():
        playerX = SCREEN_WIDTH - playerIm.get_width()
    playerY = PLAYER_Y + 25 * math.sin(math.radians(angle))

<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
def update_enemy_positions():
    global ENEMY_SPEED_X, enemies
    if not enemies:
        return True  # Indicate that all enemies are defeated

    for enemy in enemies:
        enemy["x"] += enemy["speedX"]
        enemy["y"] += 0.1 * math.sin(math.radians(enemy["angle"]))
        enemy["angle"] += SINE_ANGLE_INCREMENT

        if enemy["x"] > SCREEN_WIDTH - ENEMY_WIDTH or enemy["x"] < 0:
            enemy["speedX"] = -enemy["speedX"]
            enemy["y"] += ENEMY_DESCENT
            ENEMY_SPEED_X += ENEMY_SPEED_INCREMENT
            update_enemy_speeds()

        if enemy["y"] >= PLAYER_Y - ENEMY_HEIGHT:
            return True

    return False


def update_enemy_speeds():
    for e in enemies:
        e["speedX"] = ENEMY_SPEED_X if e["speedX"] > 0 else -ENEMY_SPEED_X


def update_bullets():
    global score, enemies
    for bullet in bullets[:]:
        if bullet["active"]:
            bullet["y"] -= bullet_speed
            if bullet["y"] < 0:
                bullet["active"] = False
                continue
            check_bullet_collision(bullet)

<<<<<<< Updated upstream
def check_bullet_collision(bullet):
    global score, enemies
    for enemy in enemies[:]:
        if (enemy['x'] < bullet['x'] + bullet_width < enemy['x'] + ENEMY_WIDTH or
            enemy['x'] < bullet['x'] < enemy['x'] + ENEMY_WIDTH) and \
           (enemy['y'] < bullet['y'] + bullet_height < enemy['y'] + ENEMY_HEIGHT or
            enemy['y'] < bullet['y'] < enemy['y'] + ENEMY_HEIGHT):
            enemy['life'] -= 1
            bullet['active'] = False
            if enemy['life'] <= 0:
=======

def check_bullet_collision(bullet):
    global score, enemies
    for enemy in enemies[:]:
        if (
            enemy["x"] < bullet["x"] + bullet_width < enemy["x"] + ENEMY_WIDTH
            or enemy["x"] < bullet["x"] < enemy["x"] + ENEMY_WIDTH
        ) and (
            enemy["y"] < bullet["y"] + bullet_height < enemy["y"] + ENEMY_HEIGHT
            or enemy["y"] < bullet["y"] < enemy["y"] + ENEMY_HEIGHT
        ):
            enemy["life"] -= 1
            bullet["active"] = False
            if enemy["life"] <= 0:
>>>>>>> Stashed changes
                enemies.remove(enemy)
                collision_sound.play()
                score += 10
            break

def check_player_enemy_collision():
    for enemy in enemies:
        if (enemy['x'] < playerX + playerIm.get_width() < enemy['x'] + ENEMY_WIDTH or
            enemy['x'] < playerX < enemy['x'] + ENEMY_WIDTH) and \
           (enemy['y'] < playerY + playerIm.get_height() < enemy['y'] + ENEMY_HEIGHT or
            enemy['y'] < playerY < enemy['y'] + ENEMY_HEIGHT):
            return True
    return False

def check_player_enemy_collision():
    for enemy in enemies:
        if (
            enemy["x"] < playerX + playerIm.get_width() < enemy["x"] + ENEMY_WIDTH
            or enemy["x"] < playerX < enemy["x"] + ENEMY_WIDTH
        ) and (
            enemy["y"] < playerY + playerIm.get_height() < enemy["y"] + ENEMY_HEIGHT
            or enemy["y"] < playerY < enemy["y"] + ENEMY_HEIGHT
        ):
            return True
    return False


def draw_score():
    font = pygame.font.SysFont(None, 36)
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))


def show_level_message(level):
    level_up_sound.play()
    draw_text(
        f"Level {level} Complete!",
        48,
        (255, 255, 255),
        (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50),
    )
    draw_text(
        "Press N to go to the next level or R to repeat the level",
        36,
        (255, 255, 255),
        (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 10),
    )
    pygame.display.update()

    return wait_for_level_transition()


def wait_for_level_transition():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    return "next"
                if event.key == pygame.K_r:
                    return "repeat"


def boss_shoot():
    if boss:
        bossX = boss[0]["x"]
        bossY = boss[0]["y"]
        boss_bullets.append(
            {"x": bossX + ENEMY_WIDTH // 2, "y": bossY + ENEMY_HEIGHT, "active": True}
        )


def update_boss_position():
    if not boss:
        return
    b = boss[0]
    b["x"] += b["speedX"]
    b["y"] += 0.1 * math.sin(math.radians(b["angle"]))

<<<<<<< Updated upstream
    if b['x'] < 0 or b['x'] > SCREEN_WIDTH - ENEMY_WIDTH:
        b['speedX'] *= -1
=======
    if b["x"] < 0 or b["x"] > SCREEN_WIDTH - ENEMY_WIDTH:
        b["speedX"] *= -1

>>>>>>> Stashed changes

def update_boss_bullets():
    for bullet in boss_bullets[:]:
        if bullet["active"]:
            bullet["y"] += bullet_speed // 2
            screen.blit(boss_bullet_image, (bullet["x"], bullet["y"]))
            if bullet["y"] > SCREEN_HEIGHT:
                boss_bullets.remove(bullet)


def check_player_boss_bullet_collision():
    for bullet in boss_bullets:
        if (
            bullet["x"] < playerX + playerIm.get_width() < bullet["x"] + bullet_width
            or bullet["x"] < playerX < bullet["x"] + bullet_width
        ) and (
            bullet["y"] < playerY + playerIm.get_height() < bullet["y"] + bullet_height
            or bullet["y"] < playerY < bullet["y"] + bullet_height
        ):
            return True
    return False


def check_bullet_boss_collision():
    global score, boss
    if not boss:
        return
    b = boss[0]
    for bullet in bullets[:]:
        if bullet["active"]:
            if (
                b["x"] < bullet["x"] + bullet_width < b["x"] + ENEMY_WIDTH
                or b["x"] < bullet["x"] < b["x"] + ENEMY_WIDTH
            ) and (
                b["y"] < bullet["y"] + bullet_height < b["y"] + ENEMY_HEIGHT
                or b["y"] < bullet["y"] < b["y"] + ENEMY_HEIGHT
            ):
                b["life"] -= 1
                bullet["active"] = False
                if b["life"] <= 0:
                    boss = []
                    collision_sound.play()
                    score += 50
                    return True
    return False

<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
def main():
    global angle, running, enemies, boss, level, score, boss_shoot_timer

    running = True
    game_over_message = ""
    boss_shoot_timer = 0
    last_boss_shoot_time = pygame.time.get_ticks()

    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_input()
        update_player_position()

        if level < MAX_LEVELS:
            if update_enemy_positions():
                game_over_message = "Game Over!"
                running = False
            if check_player_enemy_collision():
                game_over_message = "Game Over!"
                running = False
            update_bullets()
            fire_bullet()
            if not enemies:
                handle_level_completion()
        else:
            update_boss_position()
            update_boss_bullets()
            if pygame.time.get_ticks() - last_boss_shoot_time >= BOSS_SHOOT_INTERVAL:
                boss_shoot()
                last_boss_shoot_time = pygame.time.get_ticks()
            if check_player_boss_bullet_collision():
                game_over_message = "Game Over!"
                running = False
            if check_bullet_boss_collision():
                handle_level_completion()
                if not boss:  # Boss defeated
                    game_over_message = "Congratulations! You won!"
                    running = False
            update_bullets()
            fire_bullet()

        angle += SINE_ANGLE_INCREMENT

        draw_image(playerIm, playerX, playerY)
        draw_game_elements()
        draw_score()

        if not running and game_over_message:
            draw_text(
                game_over_message,
                72,
                (255, 0, 0),
                (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50),
            )

        pygame.display.update()

    show_final_screen()


def handle_level_completion():
    global level, enemies, boss
    if level < MAX_LEVELS:
        level_message = show_level_message(level)
        if level_message == "next":
            level += 1
<<<<<<< Updated upstream
            #ENEMY_SPEED_X = 0.5 + 0.1 * (level - 1)
=======
            # ENEMY_SPEED_X = 0.5 + 0.1 * (level - 1)
>>>>>>> Stashed changes
            enemies = create_enemies(NUM_ENEMIES, level)
        elif level_message == "repeat":
            enemies = create_enemies(NUM_ENEMIES, level)
    else:
        level_message = show_level_message("Final Boss")
        if level_message == "next":
            boss = create_boss()
        elif level_message == "repeat":
            enemies = create_enemies(NUM_ENEMIES, MAX_LEVELS)


def draw_game_elements():
    for bullet in bullets:
        if bullet["active"]:
            draw_image(bullet_image, bullet["x"], bullet["y"])
    if level < MAX_LEVELS:
        for enemy in enemies:
            draw_image(enemy["image"], enemy["x"], enemy["y"])
    else:
        if boss:
            draw_image(boss[0]["image"], boss[0]["x"], boss[0]["y"])
        for bullet in boss_bullets:
            if bullet["active"]:
                draw_image(boss_bullet_image, bullet["x"], bullet["y"])


def show_final_screen():
    final_screen = True
    while final_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                final_screen = False
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
