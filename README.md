# pytrivia
 Trivia game on the command line

## Usage
**Requires Python 3.6+**
Download both `pytrivia.py` and `db_record.py` into a directory of your choice. 
Then, in a terminal, point to where the files are located and run `python pytrivia.py`.

This will run the file and create a SQLite database in the folder. This is used to store your scores. The last 5 scores will be displayed when you finish the game.

Enter your name and get started with the quiz. Answer using `'a', 'b', 'c', or 'd'`. The game will not continue unless you put a valid input.
To quit at any time, type `quit` during a prompt. The game will automatically exit and show the score up to that point as well as log your score.
