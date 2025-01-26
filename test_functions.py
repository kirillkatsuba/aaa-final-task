import unittest
from copy import deepcopy
from main import (
    get_default_state,
    generate_keyboard,
    Player,
    won,
    draw,
    FREE_SPACE,
    CROSS,
    ZERO,
)


class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        """Set up default game state."""
        self.default_state = get_default_state()

    def test_get_default_state(self):
        """Test default state generation."""
        state = get_default_state()
        self.assertEqual(len(state), 3)
        for row in state:
            self.assertEqual(len(row), 3)
            self.assertTrue(all(cell == FREE_SPACE for cell in row))

    def test_generate_keyboard(self):
        """Test keyboard generation."""
        keyboard = generate_keyboard(self.default_state)
        self.assertEqual(len(keyboard), 3)
        for row in keyboard:
            self.assertEqual(len(row), 3)
            for button in row:
                self.assertTrue(button.callback_data)

    def test_player_move(self):
        """Test computer move logic."""
        player = Player(deepcopy(self.default_state))
        updated_field = player.move()
        filled_count = sum(row.count(ZERO) for row in updated_field)
        self.assertEqual(filled_count, 1)

    def test_won(self):
        """Test winning conditions."""
        for i in range(3):
            state = deepcopy(self.default_state)
            state[i] = [CROSS, CROSS, CROSS]
            self.assertTrue(won(state))

        for i in range(3):
            state = deepcopy(self.default_state)
            for j in range(3):
                state[j][i] = CROSS
            self.assertTrue(won(state))

        state = deepcopy(self.default_state)
        for i in range(3):
            state[i][i] = CROSS
        self.assertTrue(won(state))

        state = deepcopy(self.default_state)
        for i in range(3):
            state[i][2 - i] = CROSS
        self.assertTrue(won(state))

    def test_draw(self):
        """Test draw condition."""
        state = [
            [CROSS, ZERO, CROSS],
            [ZERO, CROSS, ZERO],
            [ZERO, CROSS, ZERO]
        ]
        self.assertTrue(draw(state))

        state = deepcopy(self.default_state)
        self.assertFalse(draw(state))


if __name__ == "__main__":
    unittest.main()
