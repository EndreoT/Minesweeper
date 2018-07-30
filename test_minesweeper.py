import unittest
import itertools
import random

from minesweeper import Model, get_adjacent


class TestGetAdjacent(unittest.TestCase):

    def test_get_adjacent(self):
        coordinate_1 = (5, 7)
        adj_coords_1 = get_adjacent(coordinate_1)

        self.assertEqual(len(adj_coords_1), 8)
        for c in [(4, 7), (6, 7), (4, 6), (6, 8), (6, 6), (5, 6), (4, 8), (5, 8)]:
            self.assertIn(c, adj_coords_1)


class TestModel(unittest.TestCase):
    
    def setUp(self):
        random.seed(3)
        self.height = 16
        self.width = 20
        self.num_mines = 40
        self.model = Model(self.width, self.height, self.num_mines)
        self.grid = self.model.grid
        self.grid_coords = self.model.grid_coords
           
    def test_board_dimensions(self):        
        self.assertEqual(len(self.grid), self.height)
        self.assertEqual(len(self.grid[random.randint(0, self.height)]), self.width)
    
    def test_mine_count(self):
       flattened_list = list(itertools.chain.from_iterable(self.grid))
       self.assertEqual(40, flattened_list.count(-1))

    def test_grid_coords(self):
       self.assertEqual(len(self.grid_coords), self.width * self.height)
       self.assertIn((5, 5), self.grid_coords)
       self.assertIn((15, 15), self.grid_coords)

    def test_set_adjacent_mine_count(self):

        def is_mine(coords: tuple) -> bool:
            try:
                if coords[0] >= 0 and coords[1] >= 0:
                    return self.grid[coords[1]][coords[0]] == -1
                else:
                    return False
            except IndexError:
                return False

        coordinates = []
        while len(coordinates) <= 50:
            coord = random.choice(self.model.grid_coords)
            if self.model.get_cell_value(coord) == self.model.mine_value():
                self.assertEqual(self.model.is_mine(coord), True)
                continue
            coordinates.append(coord)
        for coordinate in coordinates:
            self.assertEqual(
                        self.grid[coordinate[1]][coordinate[0]],
                        sum(map(is_mine, get_adjacent(coordinate)))
                        )


if __name__ == "__main__":
    unittest.main()