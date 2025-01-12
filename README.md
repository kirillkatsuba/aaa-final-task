# Final task (tg-bot)
To run the tic-tac-toe game you should define your own tg token `` TOKEN`` in the
`` main.py``.

After that run ``python3 main.py`` in the terminal and open the chat bot in telegram.

And enjoy the game!

# Check

To check code ypu can run 
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

We can see that there are problem only with telegram libraries, it is not depend on us.
Therefore, the task passed all checks.

