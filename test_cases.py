import unittest
from main import update_enemy_positions, check_bullet_collision, create_enemies, create_boss, ENEMY_WIDTH, ENEMY_HEIGHT

class TestGameFunctions(unittest.TestCase):

    def setUp(self):
        # Setup initial state for tests
        self.enemies = create_enemies(10, 1)
        self.bullets = [{'x': 100, 'y': 100, 'active': True}]
        self.boss = create_boss()

    def test_update_enemy_positions(self):
        result = update_enemy_positions(self.enemies)
        # Expect False if enemies are not defeated yet
        self.assertFalse(result)
        # Further checks on enemies' positions or speed can be added here

    def test_check_bullet_collision(self):
    # Setup an enemy and bullet in a collision path
        enemy = {'x': 90, 'y': 90, 'life': 1, 'image': None}
        bullet = {'x': 90, 'y': 90, 'active': True}
        self.bullets.append(bullet)
        self.enemies.append(enemy)

        # Call the collision check
        check_bullet_collision(bullet, self.enemies)

        # Debugging
        print(f"Bullet active state: {bullet['active']}")
        print(f"Enemy life: {enemy['life']}")

        # Verify the bullet is no longer active and enemy life is reduced
        self.assertFalse(bullet['active'])
        self.assertEqual(enemy['life'], 0)



    def test_create_enemies(self):
        enemies = create_enemies(5, 2)
        self.assertEqual(len(enemies), 5)
        for enemy in enemies:
            self.assertIn('x', enemy)
            self.assertIn('y', enemy)
            self.assertIn('speedX', enemy)
            self.assertIn('angle', enemy)
            self.assertIn('life', enemy)
            self.assertIn('image', enemy)

    def test_create_boss(self):
        boss = create_boss()
        self.assertEqual(len(boss), 1)
        self.assertIn('x', boss[0])
        self.assertIn('y', boss[0])
        self.assertIn('speedX', boss[0])
        self.assertIn('angle', boss[0])
        self.assertIn('life', boss[0])
        self.assertIn('image', boss[0])

if __name__ == "__main__":
    unittest.main()
