import random
import unittest

from snake import Game


class SnakeTests(unittest.TestCase):
    def game(self):
        return Game(width=10, height=10, rng=random.Random(1))

    def test_moves_forward(self):
        g = self.game()
        head = g.snake[0]
        g.food = (0, 0)
        g.step()
        self.assertEqual(g.snake[0], (head[0] + 1, head[1]))
        self.assertEqual(len(g.snake), 3)

    def test_cannot_reverse(self):
        g = self.game()
        g.turn("left")
        self.assertEqual(g.direction, "right")

    def test_eating_grows_and_scores(self):
        g = self.game()
        hx, hy = g.snake[0]
        g.food = (hx + 1, hy)
        g.step()
        self.assertEqual(g.score, 1)
        self.assertEqual(len(g.snake), 4)
        self.assertNotIn(g.food, g.snake)

    def test_wall_kills(self):
        g = self.game()
        g.food = (0, 9)
        for _ in range(20):
            g.step()
        self.assertFalse(g.alive)

    def test_self_collision_kills(self):
        g = self.game()
        g.snake = [(5, 5), (5, 6), (4, 6), (4, 5), (4, 4), (5, 4)]
        g.direction = "up"
        g.turn("left")
        g.food = (0, 0)
        g.step()  # moves into (4,5), which is body
        self.assertFalse(g.alive)

    def test_food_never_on_snake(self):
        g = self.game()
        for _ in range(200):
            self.assertNotIn(g._place_food(), g.snake)


if __name__ == "__main__":
    unittest.main()
