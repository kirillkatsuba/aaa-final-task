import unittest
import asyncio
from main import start, choose_game_type
from telegram import InlineKeyboardMarkup
from unittest.mock import AsyncMock, patch


class TestTelegramBot(unittest.TestCase):
    @patch('main.Update')
    @patch('main.ContextTypes.DEFAULT_TYPE')
    def test_start(self, mock_update, mock_context):
        """Test /start command."""
        mock_update.message.reply_text = AsyncMock()
        mock_context.user_data = {}

        # Call the function
        asyncio.run(start(mock_update, mock_context))

        # Check if reply_text was called with the correct message
        mock_update.message.reply_text.assert_called_once_with(
            'Choose if you want to play with computer '
            'or with the second player?',
            reply_markup=InlineKeyboardMarkup(choose_game_type()),
        )
