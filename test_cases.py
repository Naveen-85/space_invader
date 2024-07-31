import pygame
import unittest
from main import BOSS_LIFE, MAX_LEVELS, Game, Player, Enemy, Boss, Bullet, BossBullet, CollisionHandler

class TestGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = Game()
        self.player_img = pygame.image.load("otaku.png")
        self.enemy_img = pygame.image.load("oni.png")
        self.bullet_img = pygame.image.load("bullet.png")
        self.boss_img = pygame.image.load("oni_boss.png")

    def tearDown(self):
        pygame.quit()

    def test_player_movement(self):
        player = Player(self.player_img)
        initial_x = player.rect.x
        player.move(5)
        player.update()
        self.assertNotEqual(player.rect.x, initial_x)
        player.move(-5)
        player.update()
        self.assertEqual(player.rect.x, initial_x)

    def test_enemy_movement(self):
        enemy = Enemy(100, 100, 5, self.enemy_img, 1)
        initial_x = enemy.rect.x
        enemy.update()
        self.assertNotEqual(enemy.rect.x, initial_x)
        enemy.rect.x = 0
        enemy.update()
        self.assertEqual(enemy.direction, 1)

    def test_bullet_movement(self):
        bullet = Bullet(100, 100, self.bullet_img)
        initial_y = bullet.rect.y
        bullet.update()
        self.assertLess(bullet.rect.y, initial_y)

    def test_boss_bullet_movement(self):
        boss_bullet = BossBullet(100, 100, self.bullet_img)
        initial_y = boss_bullet.rect.y
        boss_bullet.update()
        self.assertGreater(boss_bullet.rect.y, initial_y)

    def test_player_enemy_collision(self):
        player = Player(self.player_img)
        enemy = Enemy(player.rect.x, player.rect.y, 5, self.enemy_img, 1)
        self.assertTrue(CollisionHandler.check_collision(player, enemy))

    def test_bullet_enemy_collision(self):
        bullet = Bullet(100, 100, self.bullet_img)
        enemy = Enemy(100, 100, 5, self.enemy_img, 1)
        bullets = pygame.sprite.Group(bullet)
        enemies = pygame.sprite.Group(enemy)
        score_increase = CollisionHandler.handle_bullet_enemy_collision(bullets, enemies)
        self.assertEqual(score_increase, 10)
        self.assertFalse(bullet.alive())
        self.assertFalse(enemy.alive())

    def test_bullet_boss_collision(self):
        bullet = Bullet(100, 100, self.bullet_img)
        boss = Boss(100, 100, 5, 1, self.boss_img)
        bullets = pygame.sprite.Group(bullet)
        bosses = pygame.sprite.Group(boss)
        score_increase = CollisionHandler.handle_bullet_boss_collision(bullets, bosses)
        self.assertEqual(score_increase, 100)
        self.assertFalse(bullet.alive())
        self.assertFalse(boss.alive())

    def test_boss_creation(self):
        self.assertIsNone(self.game.create_boss())
        self.game.level = MAX_LEVELS
        boss = self.game.create_boss()
        self.assertIsNotNone(boss)
        self.assertEqual(boss.life, BOSS_LIFE)

if __name__ == "__main__":
    unittest.main()
