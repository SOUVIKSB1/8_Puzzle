from django.test import TestCase, Client
from django.urls import reverse
from .views import count_inversions, is_solvable, solve_a_star, GOAL_STATE

class PuzzleTestCase(TestCase):
    def test_inversions(self):
        self.assertEqual(count_inversions(GOAL_STATE), 0)
        self.assertEqual(count_inversions([1, 2, 3, 4, 5, 6, 8, 7, 0]), 1)

    def test_solvability(self):
        self.assertTrue(is_solvable(GOAL_STATE))
        self.assertFalse(is_solvable([1, 2, 3, 4, 5, 6, 8, 7, 0]))

    def test_a_star_solver(self):
        path, nodes = solve_a_star(GOAL_STATE)
        self.assertEqual(path, [])
        self.assertEqual(nodes, 0)
        
        one_move_board = [1, 2, 3, 4, 5, 6, 7, 0, 8]
        path, nodes = solve_a_star(one_move_board)
        self.assertEqual(path, [8])

    def test_views(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
        response = client.get(reverse('api_reset'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('board', data)
        self.assertFalse(data['game_won'])
