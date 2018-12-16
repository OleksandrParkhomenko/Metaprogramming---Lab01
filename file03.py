 # SNAKESGAME
 # UseARROWKEYStoplay, SPACEBAR for pausing / resuming and EscKey for exiting
 # OriginalAuthor: SanchitGangwar
 # Modifiedby: RayanDutta
 # Minorchangesmadetokeepthegameworking.

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint


curses.initscr()
win = curses.newwin(20, 60, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

key = KEY_RIGHT # Initializingvalues
score = 0

snake = [[4, 10], [4, 9], [4, 8]] # Initialsnakeco - ordinates
food = [10, 20] # Firstfoodco - ordinates

win.addch(food[0], food[1], ' * ') # Prints or showsthefood

while key!=27: # WhileEsckey is not pressed
    win.border(0)
    win.addstr(0, 2, 'Score: ' + str(score) + '') # Printing'Score' and 
    win.addstr(0, 27, 'SNAKE') # 'SNAKE'strings
    win.timeout(int(150 - (len(snake) / 5 + len(snake) / 10) % 120)) # IncreasesthespeedofSnake as itslengthincreases

    prevKey = key # Previouskeypressed
    event = win.getch()
    key = key if event == - 1 else event


    if key == ord(''): # IfSPACEBAR is pressed, wait for another
        key = - 1 # one(Pause / Resume)
        while key!=ord(''): 
            key = win.getch()
        key = prevKey
        continue 

    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]: # Ifaninvalidkey is pressed
        key = prevKey

    # Calculatesthenewcoordinatesoftheheadofthesnake.NOTE: len(snake)increases.
    # This is takencareoflaterat[1].
    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and - 1), snake[0][1] + (key == KEY_LEFT and - 1) + (key == KEY_RIGHT and 1)])

    # Ifsnakecrossestheboundaries, makeitenter from theotherside
    if snake[0][0] == 0: snake[0][0] = 18
    if snake[0][1] == 0: snake[0][1] = 58
    if snake[0][0] == 19: snake[0][0] = 1
    if snake[0][1] == 59: snake[0][1] = 1

    # Exit if snakecrossestheboundaries(Uncommenttoenable)
    # if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break 

    # Ifsnakerunsoveritself
    if snake[0] in snake[1: ]: 
        print('GameOver')
        break ;

    if snake[0] == food: # Whensnakeeatsthefood
        food = []
        score+=1
        while food == []: 
            food = [randint(1, 18), randint(1, 58)] # Calculatingnextfood'scoordinates
            if food in snake: food = []
        win.addch(food[0], food[1], ' * ')
    else : 
        last = snake.pop() # [1]Ifitdoes not eatthefood, lengthdecreases
        win.addch(last[0], last[1], '')
    win.addch(snake[0][0], snake[0][1], ' # ')

curses.endwin()
print(" \nScore - " + str(score))
