# Final task (tg-bot)
To run the tic-tac-toe game you should define your own tg token `` TOKEN`` in the
`` main.py``.

After that run ``python3 main.py`` in the terminal and open the chat bot in telegram.

And enjoy the game!

# Check

To check code you can run 
```
flake8 .
mypy .
```
And you receive
```
kirill@MacBook-Pro-Kirill-3 aaa-final-task % flake8 .                        
kirill@MacBook-Pro-Kirill-3 aaa-final-task % mypy .  
main.py:7: error: Skipping analyzing "telegram": module is installed, but missing library stubs or py.typed marker  [import-untyped]
main.py:9: error: Skipping analyzing "telegram.ext": module is installed, but missing library stubs or py.typed marker  [import-untyped]
main.py:9: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
Found 2 errors in 1 file (checked 1 source file)
kirill@MacBook-Pro-Kirill-3 aaa-final-task % 
```

To run the test for checking correct functions operations and command ```/start```
you should run
```
python3 -m unittest -v test_functions
python3 -m unittest -v test_game
```
And you receive
```
kirill@MacBook-Pro-Kirill-3 aaa-final-task % python3 -m unittest -v functions_test
python3 -m unittest -v game_test
test_draw (functions_test.TestTicTacToe.test_draw)
Test draw condition. ... ok
test_generate_keyboard (functions_test.TestTicTacToe.test_generate_keyboard)
Test keyboard generation. ... ok
test_get_default_state (functions_test.TestTicTacToe.test_get_default_state)
Test default state generation. ... ok
test_player_move (functions_test.TestTicTacToe.test_player_move)
Test computer move logic. ... ok
test_won (functions_test.TestTicTacToe.test_won)
Test winning conditions. ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
test_start (game_test.TestTelegramBot.test_start)
Test /start command. ... ok

----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
kirill@MacBook-Pro-Kirill-3 aaa-final-task % 
```

We can see that there are problem only with telegram libraries, it is not depend on us.
Therefore, the task passed all checks.

