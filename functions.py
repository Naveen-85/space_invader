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
BULLET_WIDTH = 16
BULLET_HEIGHT = 16
BULLET_SPEED = 2

class Game:
    def __init__(self):
        # Initialize game state
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.icon = pygame.image.load("alien.png")
        pygame.display.set_icon(self.icon)

        # Load images
        self.player_img = pygame.image.load("otaku.png")
        self.enemy_img1 = pygame.image.load("oni.png")
        self.enemy_img2 = pygame.image.load("oni2.png")
        self.boss_img = pygame.image.load("oni_boss.png")
        self.background = pygame.image.load("space_ia.jpg")
        self.bullet_image = pygame.image.load("bullet.png")
        self.boss_bullet_image = pygame.image.load("bullet.png")

        # Sound setup
        mixer.music.load("background.wav")
        mixer.music.play(-1)
        self.collision_sound = mixer.Sound("explosion.wav")
        self.level_up_sound = mixer.Sound("background.wav")

        # Game variables
        self.level = 1
        self.score = 0
        self.enemies = self.create_enemies(NUM_ENEMIES, self.level)
        self.boss = []
        self.bullets = []
        self.boss_bullets = []
        self.player_x = (SCREEN_WIDTH - self.player_img.get_width()) // 2
        self.player_y = PLAYER_Y
        self.player_x_change = 0
        self.angle = 0
        self.bullet_state = "ready"  # "ready" or "fire"
        self.boss_shoot_timer = 0
        self.last_boss_shoot_time = pygame.time.get_ticks()
        self.running = True

    def create_enemies(self, num_enemies, level):
        enemies = []
        for _ in range(num_enemies):
            enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
            enemy_y = random.randint(50, 150)
            speed_x = random.choice([ENEMY_SPEED_X, -ENEMY_SPEED_X])
            life = ENEMY_LIFE + level - 1
            image = self.enemy_img1 if life < 3 else self.enemy_img2
            enemies.append({
                "x": enemy_x,
                "y": enemy_y,
                "speed_x": speed_x,
                "angle": random.uniform(0, 360),
                "life": life,
                "image": image
            })
        return enemies

    def create_boss(self):
        return [{
            "x": (SCREEN_WIDTH - ENEMY_WIDTH) // 2,
            "y": 50,
            "angle": random.uniform(0, 360),
            "speed_x": BOSS_SPEED_X,
            "life": BOSS_LIFE,
            "image": self.boss_img
        }]

    def draw_image(self, image, x, y):
        self.screen.blit(image, (x, y))

    def draw_text(self, message, font_size, color, position):
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render(message, True, color)
        self.screen.blit(text_surface, position)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_x_change = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT]:
            self.player_x_change = PLAYER_SPEED
        else:
            self.player_x_change = 0

        if keys[pygame.K_SPACE]:
            if self.bullet_state == "ready":
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                bullet_x = self.player_x + (self.player_img.get_width() - BULLET_WIDTH) // 2
                bullet_y = self.player_y
                self.bullets.append({"x": bullet_x, "y": bullet_y, "active": True})
                self.bullet_state = "fire"

    def fire_bullet(self):
        if self.bullet_state == "fire":
            for bullet in self.bullets:
                if bullet["active"]:
                    self.screen.blit(self.bullet_image, (bullet["x"], bullet["y"]))
                    bullet["y"] -= BULLET_SPEED
                    if bullet["y"] < 0:
                        bullet["active"] = False
            if all(not b["active"] for b in self.bullets):
                self.bullet_state = "ready"

    def update_player_position(self):
        self.player_x += self.player_x_change
        if self.player_x < 0:
            self.player_x = 0
        elif self.player_x > SCREEN_WIDTH - self.player_img.get_width():
            self.player_x = SCREEN_WIDTH - self.player_img.get_width()
        self.player_y = PLAYER_Y + 25 * math.sin(math.radians(self.angle))

    def update_enemy_positions(self):
        if not self.enemies:
            return True

        for enemy in self.enemies:
            enemy["x"] += enemy["speed_x"]
            enemy["y"] += 0.1 * math.sin(math.radians(enemy["angle"]))
            enemy["angle"] += SINE_ANGLE_INCREMENT

            if enemy["x"] > SCREEN_WIDTH - ENEMY_WIDTH or enemy["x"] < 0:
                enemy["speed_x"] = -enemy["speed_x"]
                enemy["y"] += ENEMY_DESCENT

            if enemy["y"] >= PLAYER_Y - ENEMY_HEIGHT:
                return True

        return False

    def update_bullets(self):
        for bullet in self.bullets[:]:
            if bullet["active"]:
                bullet["y"] -= BULLET_SPEED
                if bullet["y"] < 0:
                    bullet["active"] = False
                    continue
                self.check_bullet_collision(bullet)

    def check_bullet_collision(self, bullet):
        for enemy in self.enemies[:]:
            if (enemy["x"] < bullet["x"] + BULLET_WIDTH < enemy["x"] + ENEMY_WIDTH or
                enemy["x"] < bullet["x"] < enemy["x"] + ENEMY_WIDTH) and \
               (enemy["y"] < bullet["y"] + BULLET_HEIGHT < enemy["y"] + ENEMY_HEIGHT or
                enemy["y"] < bullet["y"] < enemy["y"] + ENEMY_HEIGHT):
                enemy["life"] -= 1
                bullet["active"] = False
                if enemy["life"] <= 0:
                    self.enemies.remove(enemy)
                    self.collision_sound.play()
                    self.score += 10
                break

    def check_player_enemy_collision(self):
        for enemy in self.enemies:
            if (enemy["x"] < self.player_x + self.player_img.get_width() < enemy["x"] + ENEMY_WIDTH or
                enemy["x"] < self.player_x < enemy["x"] + ENEMY_WIDTH) and \
               (enemy["y"] < self.player_y + self.player_img.get_height() < enemy["y"] + ENEMY_HEIGHT or
                enemy["y"] < self.player_y < enemy["y"] + ENEMY_HEIGHT):
                return True
        return False

    def draw_score(self):
        font = pygame.font.SysFont(None, 36)
        score_surface = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

    def show_level_message(self):
        self.level_up_sound.play()
        self.draw_text(f"Level {self.level} Complete!", 48, (255, 255, 255), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        self.draw_text("Press N to go to the next level or R to repeat the level", 36, (255, 255, 255), (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 10))
        pygame.display.update()
        return self.wait_for_level_transition()

    def wait_for_level_transition(self):
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

    def handle_level_completion(self):
        if self.level < MAX_LEVELS:
            level_message = self.show_level_message()
            if level_message == "next":
                self.level += 1
                self.enemies = self.create_enemies(NUM_ENEMIES, self.level)
            elif level_message == "repeat":
                self.enemies = self.create_enemies(NUM_ENEMIES, self.level)
        else:
            level_message = self.show_level_message()
            if level_message == "next":
                self.boss = self.create_boss()
            elif level_message == "repeat":
                self.enemies = self.create_enemies(NUM_ENEMIES, MAX_LEVELS)

    def update_boss_position(self):
        for b in self.boss:
            b["x"] += b["speed_x"]
            if b["x"] <= 0 or b["x"] >= SCREEN_WIDTH - ENEMY_WIDTH:
                b["speed_x"] = -b["speed_x"]

    def update_boss_bullets(self):
        for bullet in self.boss_bullets[:]:
            bullet["y"] += BULLET_SPEED
            if bullet["y"] > SCREEN_HEIGHT:
                self.boss_bullets.remove(bullet)

    def check_bullet_boss_collision(self):
        for bullet in self.bullets[:]:
            for b in self.boss:
                if (b["x"] < bullet["x"] + BULLET_WIDTH < b["x"] + ENEMY_WIDTH or
                    b["x"] < bullet["x"] < b["x"] + ENEMY_WIDTH) and \
                   (b["y"] < bullet["y"] + BULLET_HEIGHT < b["y"] + ENEMY_HEIGHT or
                    b["y"] < bullet["y"] < b["y"] + ENEMY_HEIGHT):
                    b["life"] -= 1
                    bullet["active"] = False
                    if b["life"] <= 0:
                        self.boss.remove(b)
                        self.collision_sound.play()
                        self.score += 100
                    break

    def boss_shoot(self):
        for b in self.boss:
            bullet_x = b["x"] + (ENEMY_WIDTH - BULLET_WIDTH) // 2
            bullet_y = b["y"] + ENEMY_HEIGHT
            self.boss_bullets.append({"x": bullet_x, "y": bullet_y, "active": True})

    def check_player_boss_bullet_collision(self):
        for bullet in self.boss_bullets:
            if (bullet["x"] < self.player_x + self.player_img.get_width() < bullet["x"] + BULLET_WIDTH or
                bullet["x"] < self.player_x < bullet["x"] + BULLET_WIDTH) and \
               (bullet["y"] < self.player_y + self.player_img.get_height() < bullet["y"] + BULLET_HEIGHT or
                bullet["y"] < self.player_y < bullet["y"] + BULLET_HEIGHT):
                return True
        return False

    def show_final_screen(self):
        self.draw_text("Game Over!", 72, (255, 0, 0), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        self.draw_text(f"Your Final Score: {self.score}", 48, (255, 255, 255), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10))
        pygame.display.update()
        pygame.time.wait(3000)

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.handle_input()
            self.update_player_position()

            if self.level < MAX_LEVELS:
                if self.update_enemy_positions():
                    self.running = False
                if self.check_player_enemy_collision():
                    self.running = False
                self.update_bullets()
                self.fire_bullet()
                if not self.enemies:
                    self.handle_level_completion()
            else:
                self.update_boss_position()
                self.update_boss_bullets()
                if pygame.time.get_ticks() - self.last_boss_shoot_time >= BOSS_SHOOT_INTERVAL:
                    self.boss_shoot()
                    self.last_boss_shoot_time = pygame.time.get_ticks()
                if self.check_player_boss_bullet_collision():
                    self.running = False
                if len(self.boss) == 0:
                    self.handle_level_completion()
                    if not self.boss:
                        self.running = False
                self.update_bullets()
                self.fire_bullet()

            self.angle += SINE_ANGLE_INCREMENT

            self.draw_image(self.player_img, self.player_x, self.player_y)
            for enemy in self.enemies:
                self.draw_image(enemy["image"], enemy["x"], enemy["y"])
            for bullet in self.bullets:
                if bullet["active"]:
                    self.draw_image(self.bullet_image, bullet["x"], bullet["y"])
            for b in self.boss:
                self.draw_image(b["image"], b["x"], b["y"])
            for bullet in self.boss_bullets:
                if bullet["active"]:
                    self.draw_image(self.boss_bullet_image, bullet["x"], bullet["y"])

            self.draw_score()

            pygame.display.update()

        self.show_final_screen()

if __name__ == "__main__":
    game = Game()
    game.run()
