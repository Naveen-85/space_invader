from typing import List
import pygame
import math
import random
from pygame import mixer

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_Y = 480
PLAYER_SPEED = 5
SINE_ANGLE_INCREMENT = 1
ENEMY_WIDTH = 62
ENEMY_HEIGHT = 62
NUM_ENEMIES = 10
ENEMY_SPEED_X = 1
ENEMY_DESCENT = 10
ENEMY_LIFE = 1
MAX_LEVELS = 3
BOSS_LIFE = 10
BOSS_SPEED_X = 0.9
BOSS_SHOOT_INTERVAL = 2000  # Boss shoots every 2 seconds
BULLET_WIDTH = 16
BULLET_HEIGHT = 16
BULLET_SPEED = 5

class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.img.get_width()) // 2
        self.rect.y = PLAYER_Y
        self.x_change = 0
        self.angle = 0

    def move(self, dx):
        self.x_change = dx

    def update(self):
        self.rect.x += self.x_change
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - self.img.get_width():
            self.rect.x = SCREEN_WIDTH - self.img.get_width()
        self.angle = (self.angle + SINE_ANGLE_INCREMENT) % 360
        self.rect.y = PLAYER_Y + 25 * math.sin(math.radians(self.angle))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, img, life):
        super().__init__()
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed_x
        self.life = life
        self.direction = 1

    def update(self):
        self.rect.x += self.speed_x * self.direction
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.direction *= -1
            self.rect.y += ENEMY_DESCENT

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, life, img):
        super().__init__()
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed_x
        self.life = life

    def update(self):
        # Mueve el jefe horizontalmente
        self.rect.x += self.speed_x
        # Cambia de dirección si llega a los bordes de la pantalla
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - self.rect.width:
            self.speed_x = -self.speed_x



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = True

    def update(self):
        if self.active:
            self.rect.y -= BULLET_SPEED
            if self.rect.y < 0:
                self.kill()

class BossBullet(Bullet):
    def __init__(self, x, y, img):
        super().__init__(x, y, img)

    def update(self):
        if self.active:
            self.rect.y += BULLET_SPEED 
            if self.rect.y > SCREEN_HEIGHT:
                self.kill()


class CollisionHandler:
    @staticmethod
    def check_collision(sprite1, sprite2):
        return sprite1.rect.colliderect(sprite2.rect)

    @staticmethod
    def handle_bullet_enemy_collision(bullets, enemies) -> int:
        score_increase = 0
        for bullet in bullets:
            if bullet.active:
                collided_enemy = pygame.sprite.spritecollideany(bullet, enemies)
                if collided_enemy:
                    collided_enemy.life -= 1
                    bullet.kill()  # Remove the bullet from the group
                    if collided_enemy.life <= 0:
                        collided_enemy.kill()  # Remove the enemy from the group
                        score_increase += 10  # Increment score by a value
        return score_increase

    @staticmethod
    def handle_bullet_boss_collision(bullets, boss):
        score_increase = 0
        for bullet in bullets:
            if bullet.active:
                collided_boss = pygame.sprite.spritecollideany(bullet, boss)
                if collided_boss:
                    collided_boss.life -= 1
                    bullet.kill()  # Remove the bullet from the group
                    if collided_boss.life <= 0:
                        collided_boss.kill()  # Remove the boss from the group
                        score_increase += 100  # Increment score by a value
        return score_increase

    @staticmethod
    def handle_player_collision(player, enemies):
        for enemy in enemies:
            if CollisionHandler.check_collision(player, enemy):
                return True
        return False

    @staticmethod
    def handle_boss_bullet_player_collision(boss_bullets, player):
        for bullet in boss_bullets:
            if bullet.active:
                if CollisionHandler.check_collision(bullet, player):
                    return True
        return False



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.icon = pygame.image.load("alien.png")
        pygame.display.set_icon(self.icon)

        self.player_img = pygame.image.load("otaku.png")
        self.enemy_img1 = pygame.image.load("oni.png")
        self.enemy_img2 = pygame.image.load("oni2.png")
        self.boss_img = pygame.image.load("oni_boss.png")
        self.background = pygame.image.load("space_ia.jpg")
        self.bullet_image = pygame.image.load("bullet.png")
        self.boss_bullet_image = pygame.image.load("bullet.png")

        mixer.music.load("background.wav")
        mixer.music.play(-1)
        self.collision_sound = mixer.Sound("explosion.wav")
        self.level_up_sound = mixer.Sound("background.wav")

        self.level = 1
        self.score = 0
        self.enemies = pygame.sprite.Group(self.create_enemies(NUM_ENEMIES, self.level))
        self.boss = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.boss_bullets = pygame.sprite.Group()
        self.player = Player(self.player_img)
        self.bullet_state = "ready"
        self.last_boss_shoot_time = pygame.time.get_ticks()
        self.running = True
        self.game_over = False

    def create_enemies(self, num_enemies, level) -> List[Enemy]:
        enemies = []
        for _ in range(num_enemies):
            enemy_img = self.enemy_img1 if level < 2 else self.enemy_img2
            enemy = Enemy(
                random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH),
                random.randint(50, 150),
                ENEMY_SPEED_X,
                enemy_img,
                ENEMY_LIFE + level - 1
            )
            enemies.append(enemy)
        return enemies

    def create_boss(self):
        if self.level == MAX_LEVELS:
            return Boss(
                (SCREEN_WIDTH - ENEMY_WIDTH) // 2,
                50,
                BOSS_SPEED_X,
                BOSS_LIFE,
                self.boss_img
            )
        return None

    def draw_image(self, image, x, y):
        self.screen.blit(image, (x, y))

    def draw_text(self, message, font_size, color, position) -> None:
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render(message, True, color)
        self.screen.blit(text_surface, position)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-PLAYER_SPEED // 2)  
        elif keys[pygame.K_RIGHT]:
            self.player.move(PLAYER_SPEED // 2)  
        else:
            self.player.move(0)

        if keys[pygame.K_SPACE]:
            if self.bullet_state == "ready":
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                bullet_x = self.player.rect.centerx - BULLET_WIDTH // 2
                bullet_y = self.player.rect.top
                self.bullets.add(Bullet(bullet_x, bullet_y, self.bullet_image))
                self.bullet_state = "fired"
        else:
            self.bullet_state = "ready"

    def update_entities(self):
        self.player.update()
        self.enemies.update()
        self.boss.update()
        self.bullets.update()
        self.boss_bullets.update()

    def check_collisions(self):
        score_increase = CollisionHandler.handle_bullet_enemy_collision(self.bullets, self.enemies)
        if score_increase is not None:
            self.score += score_increase

        score_increase = CollisionHandler.handle_bullet_boss_collision(self.bullets, self.boss)
        if score_increase is not None:
            self.score += score_increase

        if CollisionHandler.handle_player_collision(self.player, self.enemies):
            self.running = False
            self.game_over = True

        if CollisionHandler.handle_boss_bullet_player_collision(self.boss_bullets, self.player):
            self.running = False
            self.game_over = True



    def handle_level_completion(self):
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

    def handle_level(self):
        level_message = self.handle_level_completion()
        if level_message == "next":
            self.level += 1
            if self.level < MAX_LEVELS:
                self.enemies = pygame.sprite.Group(self.create_enemies(NUM_ENEMIES, self.level))
                self.boss.empty()
            else:
                self.enemies.empty()
                boss = self.create_boss()
                if boss:
                    self.boss.add(boss)
        elif level_message == "repeat":
            if self.level < MAX_LEVELS:
                self.enemies = pygame.sprite.Group(self.create_enemies(NUM_ENEMIES, self.level))
            else:
                self.boss.empty()
                boss = self.create_boss()
                if boss:
                    self.boss.add(boss)

    def boss_shoot(self):
        for b in self.boss:
            bullet_x = b.rect.centerx - BULLET_WIDTH // 2
            bullet_y = b.rect.bottom
            self.boss_bullets.add(BossBullet(bullet_x, bullet_y, self.boss_bullet_image))

    def show_game_over(self):
        self.screen.fill((0, 0, 0))
        self.draw_text("Game Over", 64, (255, 0, 0), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        self.draw_text(f"Final Score: {self.score}", 48, (255, 255, 255), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10))
        self.draw_text("Press Q to Quit or R to Restart", 36, (255, 255, 255), (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 70))
        pygame.display.update()

    def wait_for_game_over_input(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()
                    if event.key == pygame.K_r:
                        self.__init__()  # Reinicia el juego
                        self.main()
                        waiting = False

    def main(self):
        while True:
            if self.running:
                self.screen.fill((0, 0, 0))
                self.screen.blit(self.background, (0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                self.handle_input()
                self.update_entities()
                self.check_collisions()

                if self.level < MAX_LEVELS:
                    if not self.enemies:
                        self.handle_level()
                else:
                    if pygame.time.get_ticks() - self.last_boss_shoot_time >= BOSS_SHOOT_INTERVAL:
                        self.boss_shoot()
                        self.last_boss_shoot_time = pygame.time.get_ticks()
                    if not self.boss:
                        self.running = False
                        self.game_over = True

                self.draw_image(self.player.img, self.player.rect.x, self.player.rect.y)
                for enemy in self.enemies:
                    self.draw_image(enemy.img, enemy.rect.x, enemy.rect.y)
                for bullet in self.bullets:
                    self.draw_image(bullet.img, bullet.rect.x, bullet.rect.y)
                for b in self.boss:
                    self.draw_image(b.img, b.rect.x, b.rect.y)
                for boss_bullet in self.boss_bullets:
                    self.draw_image(boss_bullet.img, boss_bullet.rect.x, boss_bullet.rect.y)

                self.draw_text(f"Score: {self.score}", 36, (255, 255, 255), (10, 10))
                pygame.display.update()
            else:
                self.show_game_over()
                self.wait_for_game_over_input()

if __name__ == "__main__":
    game = Game()
    game.main()
 
