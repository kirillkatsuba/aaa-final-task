"""
Bot for playing tic tac toe game with multiple CallbackQueryHandlers.
"""
from copy import deepcopy
import logging
import random
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardRemove, Update)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# set higher logging level for httpx
# to avoid all GET and POST requests being logged
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# get token using BotFather
TOKEN = 'YOUR TG TOKEN'

CONTINUE_GAME, FINISH_GAME = range(2)
GAME_STATE = None

FREE_SPACE = '.'
CROSS = 'X'
ZERO = 'O'


DEFAULT_STATE = [[FREE_SPACE for _ in range(3)] for _ in range(3)]


class Player:
    def __init__(self, field):
        self.field = field

    def move(self, position: tuple = (None, None)):
        valid_ind = []
        for x in range(3):
            for y in range(3):
                if self.field[x][y] == FREE_SPACE:
                    valid_ind.append((x, y))
        if len(valid_ind) == 0:
            return self.field
        position = random.choice(valid_ind)
        self.field[position[0]][position[-1]] = ZERO

        return self.field


def get_default_state():
    """Helper function to get default state of the game"""
    return deepcopy(DEFAULT_STATE)


def generate_keyboard(
        state: list[list[str]]
) -> list[list[InlineKeyboardButton]]:
    """Generate tic tac toe keyboard 3x3 (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


def choose_game_type() -> list[list[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton('Multiplayer game',
                                 callback_data='Multiplayer game')
        ],
        [
            InlineKeyboardButton('Game with computer',
                                 callback_data='Game with computer')
        ]
    ]


def won(fields: list[str]) -> bool:
    """Check if crosses or zeros have won the game"""
    diagonal = []
    other_diagonal = []
    for i in range(3):
        if (len(set([fields[i][j] for j in range(3)])) == 1
                and fields[i][-1] != FREE_SPACE):
            return True
        elif (len(set([fields[j][i] for j in range(3)])) == 1
              and fields[-1][i] != FREE_SPACE):
            return True
        diagonal.append(fields[i][i])
        other_diagonal.append(fields[i][2 - i])
    if len(set(diagonal)) == 1 and diagonal[-1][-1] != FREE_SPACE:
        return True
    elif (len(set(other_diagonal)) == 1 and
          other_diagonal[-1][-1] != FREE_SPACE):
        return True
    return False


def draw(fields: list[str]):
    """Check if it is draw between players"""
    full_field = True
    for x in range(3):
        for y in range(3):
            if fields[x][y] == FREE_SPACE:
                full_field = False
    return full_field


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send message on `/start`."""
    context.user_data['keyboard_state'] = get_default_state()
    context.user_data['game_state'] = None

    reply_markup = InlineKeyboardMarkup(choose_game_type())
    text = ('Choose if you want to play with computer or with '
            'the second player?')
    await update.message.reply_text(text,
                                    reply_markup=reply_markup)
    return CONTINUE_GAME


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main processing of the game"""
    query = update.callback_query
    await query.answer()

    if context.user_data['game_state'] is None:
        context.user_data['game_state'] = query.data
        context.user_data['current_player'] = CROSS
        keyboard = generate_keyboard(context.user_data['keyboard_state'])
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = f'{context.user_data['game_state']} started!'
        await query.message.reply_text(text, reply_markup=reply_markup)
        return CONTINUE_GAME

    pos_player1 = [int(num) for num in query.data]
    if (context.user_data['keyboard_state'][pos_player1[0]][pos_player1[1]]
            != FREE_SPACE):
        keyboard = generate_keyboard(context.user_data['keyboard_state'])
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = 'Position already taken! Choose a free spot.'
        await query.message.reply_text(text, reply_markup=reply_markup)
        return CONTINUE_GAME

    current_player = context.user_data['current_player']
    if context.user_data['game_state'] == 'Multiplayer game':
        context.user_data['keyboard_state'][pos_player1[0]][pos_player1[1]] \
            = current_player
        context.user_data['current_player'] = ZERO \
            if current_player == CROSS else CROSS
    else:
        context.user_data['keyboard_state'][pos_player1[0]][pos_player1[1]] \
            = CROSS
        keyboard = generate_keyboard(context.user_data['keyboard_state'])
        reply_markup = InlineKeyboardMarkup(keyboard)
        if won(context.user_data['keyboard_state']):
            await query.message.reply_text(f'Player with {CROSS} wins!',
                                           reply_markup=reply_markup)
            return FINISH_GAME
        computer = Player(context.user_data['keyboard_state'])
        context.user_data['keyboard_state'] = computer.move()
        keyboard = generate_keyboard(context.user_data['keyboard_state'])
        reply_markup = InlineKeyboardMarkup(keyboard)
        if won(context.user_data['keyboard_state']):
            await query.message.reply_text(f'Player with {ZERO} wins!',
                                           reply_markup=reply_markup)
            return FINISH_GAME

    context.user_data['current_player'] = ZERO \
        if current_player == CROSS else CROSS

    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    if won(context.user_data['keyboard_state']):
        text = f'Player with {current_player} wins!'
        await query.message.reply_text(text,
                                       reply_markup=reply_markup)
        return FINISH_GAME
    elif draw(context.user_data['keyboard_state']):
        await query.message.reply_text('It is a draw!')
        return FINISH_GAME

    await query.message.reply_text('Next move',
                                   reply_markup=reply_markup)
    return CONTINUE_GAME


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    context.user_data['keyboard_state'] = get_default_state()
    await (update.callback_query.
           message.reply_text('Start new game!',
                              reply_markup=ReplyKeyboardRemove()))
    return ConversationHandler.END


def main():
    """Run the bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Setup conversation handler with the states CONTINUE_GAME and FINISH_GAME
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONTINUE_GAME: [CallbackQueryHandler(game)],
            FINISH_GAME: [CallbackQueryHandler(end)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
