'''
    CS 5001
    Fall 2022
    Project: Sliding Puzzle game
    Ngoc (Jessie) Nguyen
'''
# import modules
import turtle  # the main graphic module
import os  # for working with files
import math  # for working with rows and columns
import itertools  # for working with dictionaries
import random  # for scrambling tiles
import datetime  # for error logging time stamp

# import subclasses
from messages_settings import Messages

# import classes
from Leaderboard import ScoreKeeper


def splash_screen(screen):
    '''
        initialize splash screen
    '''
    # load splash screen
    screen.bgpic("Resources/splash_screen.gif")

    # on screen timer so the splash screen lingers for 3 seconds
    screen.ontimer(turtle.clearscreen, t=3000)


def user_name():
    '''
        Get player name for the leaderboard
        Return username
    '''
    username = turtle.textinput("CS 5001 Sliding Puzzle",
                                "Enter your name: ")
    return username


def num_moves():
    '''
        Get number of moves from player
        Return moves
    '''
    moves = turtle.numinput("CS 5001 Sliding Puzzle: Moves",
                            "Enter the number of moves (5-200)",
                            50, minval=5, maxval=200)
    return moves


def check_puzzle(puzzle, puz_choice, puz_list):
    '''
        Function to check if puzzle exists, and has the correct number of
        tiles, and all the images for the tiles exists.
        The purpose is to prevent the system from crashing if the input
        is erroneous
        Returns True iff the puzzle satisfies all the criteria above, else,
            returns False
    '''
    if puzzle is False:
        return False

    if puz_choice + ".puz" in puz_list:
        if puzzle["number"] in [4, 9, 16]:
            # create a list of tiles that's going to be on the board
            keys = list(range(1, puzzle["number"] + 1))
            tiles_list = {k: puzzle[k] for k in keys}

            # check whether all the image exists
            exists = []
            image_list = tiles_list.values()
            for each_image in image_list:
                exists.append(os.path.exists(each_image))
                if False not in image_list:
                    return True
                else:
                    return False
        else:
            return False
    else:
        return False


def puzzle_choice(puz_data):
    '''
        Function to grab and record user choice of puzzle
        Returns the name of the puzzle that user selected
    '''
    # make a list of all file with extension ".puz"
    puz_list = []
    for file in os.listdir():
        if file.endswith(".puz"):
            puz_list.append(file)
    nl = "\n"

    # display a warning if there are more than 10 puzzle files
    if len(puz_list) > 10:
        Messages("Resources/file_warning.gif", 0, (0, 150), 3000)

    # display puzzle choice and get user input
    puz_choice = turtle.textinput("Load puzzle",
                                  f"Enter the name of the puzzle you "
                                  f"wish to load (without the .puz "
                                  f"extension), choices are: \n"
                                  f"{nl.join(puz_list[:10])}")

    # grab the puzzle from the list of available puzzle, if is not valid,
    # then False will be returned
    puzzle = next((item for item in puz_data if item["name"] == puz_choice),
                  False)
    try:
        # check if puzzle exists, isn't malformed, and isn't missing any files
        is_valid_puzzle = check_puzzle(puzzle, puz_choice, puz_list)

        if is_valid_puzzle is True:
            return puz_choice
        else:
            # initialize while loop until user enters a valid puzzle
            while is_valid_puzzle is False:
                # call error_log to record error
                error = "file " + puz_choice + ".puz does not exists or " \
                                               "is malformed"
                # get function name
                function_name = puzzle_choice.__name__
                # log error
                error_log(error, function_name)

                Messages("Resources/file_error.gif", 0, (0, 150), 3000)

                # ask again
                puz_choice = turtle.textinput("Load puzzle",
                                              f"Enter the name of the puzzle "
                                              f"you wish to load  "
                                              f"(without the .puz extension)"
                                              f", choices are: \n"
                                              f"{nl.join(puz_list)}")
                # grab the puzzle from dictionary list
                puzzle = next(
                    (item for item in puz_data if item["name"] == puz_choice),
                    False)
                # check if puzzle is valid
                is_valid_puzzle = check_puzzle(puzzle, puz_choice, puz_list)

            return puz_choice
    except StopIteration:
        error_log("user cancelled dialogue box", "puzzle_choice()")


def draw_board():
    '''
        Function to draw the game board for display
    '''
    # initialize turtle
    t = turtle.Turtle()

    # pensize
    t.pensize(5)
    # max-speed
    t.speed(0)
    # no visibility
    t.hideturtle()

    # main game board
    # reposition turtle
    t.penup()
    t.forward(100)
    # begin drawing
    t.pendown()
    t.begin_fill()
    t.left(90)
    t.forward(300)
    for i in range(3):
        t.left(90)
        t.forward(450)
    t.left(90)
    t.forward(150)
    t.end_fill()
    t.penup()

    # leader board
    # reposition turtle
    t.forward(300)
    t.right(90)
    t.forward(50)
    # begin drawing
    t.pencolor("blue")
    t.pendown()
    t.forward(200)
    t.right(90)
    t.forward(450)
    t.right(90)
    t.forward(200)
    t.right(90)
    t.forward(450)
    t.penup()

    # bottom menu
    # reposition turtle
    t.left(90)
    t.forward(50)
    t.left(90)
    t.forward(450)
    t.right(90)
    t.forward(450)
    t.left(90)
    t.forward(50)
    # begin drawing
    t.pencolor("green")
    t.pendown()
    for i in range(2):
        t.forward(100)
        t.left(90)
        t.forward(700)
        t.left(90)
    t.penup()

    # write leaderboard
    t.pencolor("blue")
    t.goto(200, 150)
    t.write("Leaderboard", font=("Arial", 15, "bold"))


def add_button():
    '''
        Function to add button icons to turtle
    '''
    # get all the file names from resource folder
    resources = os.listdir("Resources")

    # get button directories
    buttons = []
    for each in resources:
        buttons.append("Resources/" + each)

    # add shape collections to turtle library
    for each in buttons:
        turtle.addshape(each)


def load_button(score, screen, puz_data, moves, username):
    '''
        Function to make the "load" button
    '''
    load = turtle.Turtle()

    # button attributes
    load.penup()
    load.speed(0)
    load.goto(150, -250)
    load.shape("Resources/loadbutton.gif")

    def load_choice(*args):
        # get user choice of puzzle
        puz_choice = puzzle_choice(puz_data)

        # clear all turtles and redraw screen
        screen.clearscreen()

        # redraw board background
        draw_board()

        # read leaderboard
        leaderboard = read_leaderboard()

        # display leaderboard
        display_leaderboard(leaderboard)

        # add quit, load, and reset buttons
        add_button()
        quit_button()
        load_button(score, screen, puz_data, moves, username)

        # reset score to 0
        score.reset_score()

        # load puzzle to the desired one from user
        board, num_cols, num_rows, puzzle = load_puzzle(score, screen,
                                                        puz_data, puz_choice)

        # get new winning tiles positions
        win_con = get_winning_array(board, num_cols, num_rows)

        # load reset button based on new winning tiles position
        reset_button(board, win_con, num_cols, num_rows)

        # scramble tiles
        scramble_tiles(board, num_cols, num_rows, puzzle)

        # get current tiles positions
        get_tile_pos(puzzle, score, username, win_con, board, screen, moves)

    load.onclick(load_choice)


def quit_button():
    '''
        Function to make the "quit" button
        When player press on the button, it will display a farewell message
        and automatically exits the program
    '''
    quit_game = turtle.Turtle()

    # button attributes
    quit_game.penup()
    quit_game.speed(0)
    quit_game.goto(250, -250)
    quit_game.shape("Resources/quitbutton.gif")

    def exit_game(x, y):
        quit_message = turtle.Turtle()
        quit_message.shape("Resources/quitmsg.gif")
        turtle.ontimer(turtle.bye, t=2000)

    quit_game.onclick(exit_game)


def reset_button(board, win_con, num_cols, num_rows):
    '''
        Function to make the "reset" button
    '''
    reset = turtle.Turtle()

    # button attributes
    reset.penup()
    reset.speed(0)
    reset.goto(50, -250)
    reset.shape("Resources/resetbutton.gif")

    def unscramble(*args):
        reset_board(board, win_con, num_cols, num_rows)

    reset.onclick(unscramble)


def load_metadata():
    '''
        Function to load metadata of the puzzles by gathering all files
            with the ".puz" extension
        Returns a list of dictionary containing metadata for each puzzle
    '''
    # create a list with the name of all puzzles
    puz_list = []
    for file in os.listdir():
        if file.endswith(".puz"):
            puz_list.append(file)

    # read metadata of all puzzle files into a nested list where each
    # element is a puzzle
    puz_data = []

    for each in puz_list:
        with open(each, mode="r", encoding="utf-8") as in_file:
            puz_data.append(in_file.readlines())

    # clean up data
    for i in range(len(puz_data)):
        for j in range(len(puz_data[i])):
            puz_data[i][j] = puz_data[i][j].strip("\n")  # strip "\n"
            puz_data[i][j] = puz_data[i][j].replace(" ", "")
            puz_data[i][j] = puz_data[i][j].split(":")
            # turn all numbers to int
            for k in range(len(puz_data[i][j])):
                if puz_data[i][j][k].isnumeric() is True:
                    puz_data[i][j][k] = int(puz_data[i][j][k])

    # turn puz_data into dictionary
    for i in range(len(puz_data)):
        puz_data[i] = {x[0]: x[1] for x in puz_data[i]}

    return puz_data


def add_tiles_images(puz_data):
    '''
        Function to add all images of tiles to turtle from metadata
    '''
    images_path_list = []
    # get a list of images from the dictionary created from puz metadata
    for each_dict in puz_data:
        images_path_list.append(list(each_dict.values()))

    # get only the path for all tiles (excluding metadata)
    images_path_list = [sublist[3:] for sublist in images_path_list]

    # unnest the list
    images_path_list = sum(images_path_list, [])

    # remove files that don't exist
    images_path_list_valid = []
    for each in images_path_list:
        if os.path.exists(each) is True:
            images_path_list_valid.append(each)

    # use a dictionary to remove duplicate files
    images_path_list_valid = list(dict.fromkeys(images_path_list_valid))

    # add tiles collection to the turtle library
    for each in images_path_list_valid:
        turtle.addshape(each)


def load_puzzle(score, screen, puz_data, puz_choice="mario"):
    '''
    Function to load the puzzle based on user choice
    Input:
        choice: a string representing the name of the puzzle, default is
        "mario"
    Output:
        the puzzle
    Citation:
        The framework for creating board, draw tiles, a
        nd distribute board comes from
        Line 118 - 125 and 101 - 110 in source:
            Website name: Github
            URL: https://github.com/Robin-Andrews/15-Puzzle-Python-Turtle
                /blob/master15_puzzle_turtle.py
            Title: "15-Puzzle-Python-Turtle"
            Date of retrieval: 11/21/2022
    '''
    # grab puzzle from metadata of puzzle in dictionary format
    puzzle = next(item for item in puz_data if item["name"] == puz_choice)

    # get puzzle size for tile swapping logic
    tile_size = puzzle['size']

    # set score board
    scoreboard = turtle.Turtle()
    scoreboard.hideturtle()
    scoreboard.speed(0)
    scoreboard.penup()
    scoreboard.goto(-300, -250)

    # make thumbnail for the puzzle
    thumbnail = turtle.Turtle()
    thumbnail.shape(puzzle["thumbnail"])
    thumbnail.speed(0)
    thumbnail.penup()
    thumbnail.goto(300, 250)

    # create a 2d array of the board based on number of tiles
    num_cols = int(math.sqrt(puzzle["number"]))
    num_rows = int(math.sqrt(puzzle["number"]))

    board = [["Turtle" for _ in range(num_cols)] for _ in range(num_rows)]

    # create a list of tiles that's going to be on the board
    keys = list(range(1, puzzle["number"] + 1))
    tiles_list = {k: puzzle[k] for k in keys}

    # distribute tiles to board
    screen.tracer(0)  # stop animation so the screen doesn't flicker

    # make turtle objects to act as tile on the board. Each turtle is
    # assigned a tile image like the buttons. The number of iterations
    # are based on the number of rows and columns calculated from total
    # number of tiles
    tile_num = 1
    for i in range(num_rows):
        for j in range(num_cols):
            tile = turtle.Turtle()
            tile.shape(tiles_list[tile_num])
            tile.penup()
            board[i][j] = tile
            tile.hideturtle()
            tile_num += 1

            def swap_tile(x, y, tile=tile):
                is_adjacent(score, board, tile, tile_size)

                scoreboard.clear()
                scoreboard.write(f"Player Moves: {score.__str__()}",
                                 font=("Arial", 20, "bold"))

            tile.onclick(swap_tile)

    screen.tracer(1)  # re-enable animation

    # distribute the tiles in the winning configuration
    draw_tiles(board, num_cols, num_rows, puzzle)

    return board, num_cols, num_rows, puzzle


def draw_tiles(board, num_cols, num_rows, puzzle):
    '''
        Function to draw tiles on board
        Citation:
        The framework for tiles distribution comes from
        Line 118 - 125 and 101 - 110 in source:
            Website name: Github
            URL: https://github.com/Robin-Andrews/15-Puzzle-Python-Turtle
                /blob/master15_puzzle_turtle.py
            Title: "15-Puzzle-Python-Turtle"
            Date of retrieval: 11/21/2022
    '''
    # distribute the tiles onto board based on its position on the
    # 2d array of the board
    for i in range(num_rows):
        for j in range(num_cols):
            tile = board[i][j]
            tile.speed(0)
            tile.goto(-275 + j * (puzzle["size"] + 2),
                      230 - i * (puzzle["size"] + 2))
            tile.showturtle()


def get_winning_array(board, num_cols, num_rows):
    '''
        Function to get the winning configuration of tiles
        Returns a dictionary containing each tile object, and where
            they are supposed to be to form the winning configuration
    '''
    # get winning configuration
    # create 2D array for the winning tile coordinates
    win_pos = [["pos" for _ in range(num_cols)] for _ in range(num_rows)]
    for i in range(len(board)):
        for j in range(len(board[i])):
            win_pos[i][j] = board[i][j].pos()

    # zip turtle objects on the board with the corresponding coordinates
    # from win_pos
    win_con = list(map(list, zip(itertools.chain(*board),
                                 itertools.chain(*win_pos))))

    # turn it into dictionary, so we can direct turtles to go to their
    # corresponding position
    win_con = dict(win_con)

    return win_con


def scramble_tiles(board, num_cols, num_rows, puzzle):
    '''
    Function to scramble board
    Returns a board with scrambled tiles
    '''
    # shuffle tiles
    for i in range(len(board)):
        random.shuffle(board[i])
    random.shuffle(board)

    # distribute the tiles (turtles) onto the board in the scrambled
    # configuration
    draw_tiles(board, num_cols, num_rows, puzzle)

    return board


def reset_board(board, win_con, num_cols, num_rows):
    '''
        Function to reset board to winning configuration based on
        coordinates taken from function get_winning_array()
    '''
    for i in range(num_rows):
        for j in range(num_cols):
            tile = board[i][j]
            tile.speed(0)
            tile.goto(win_con[tile])


def find_blank_square(board):
    '''
        Function to return position of blank tile and the blank tile itself
        Returns a 2Dvector (x, y) for the position of the blank tile, and
        a turtle object id for the tile
    '''
    for each_row in board:
        for each_tile in each_row:
            if "blank" in each_tile.shape():
                blank_pos = each_tile.pos()
                blank_tile = each_tile

                return blank_tile, blank_pos


def is_adjacent(score, board, tile, tile_size):
    '''
        Function to check if a clicked tile is adjacent to blank tile
        If adjacent is True:
            Swap position of clicked tile with blank tile
        If adjacent is False:
            Do nothing
    '''
    # get blank tile and its coordinates
    blank_tile, blank_pos = find_blank_square(board)

    # set tile size as the distance boundaries
    tile_size = tile_size + 2

    # get tile coordinates
    tile_pos = tile.pos()

    # compare distance and swap if tile is next to blank tiles
    if tile.distance(blank_tile) <= tile_size:
        tile.goto(blank_pos)
        blank_tile.goto(tile_pos)
        # prevent score from being added if user accidentally click on
        # blank tile
        if tile.pos() != tile_pos:
            score.add_score()


def get_tile_pos(puzzle, score, username, win_con, board, screen, moves):
    '''
        Function to get the current position of the tiles. If the current
        tiles position matches with the winning configuration, then
        user wins
    '''

    position = []
    # get all positions of tiles on the board each time the board is clicked
    for each_row in board:
        for each_turtle in each_row:
            position.append(each_turtle)
            position.append(each_turtle.pos())

    # convert positional list to a dictionary
    position_dict = {position[i]: position[i + 1]
                     for i in range(0, len(position), 2)}

    # detect winning position
    if win_con == position_dict:
        Messages("Resources/winner.gif", 0, (0, 0), 3000)
        save_leader_board(score, username)
        turtle.ontimer(turtle.bye, t=4000)
    # detect losing position if exceed number of moves
    elif int(score.__str__()) > moves:
        Messages("Resources/Lose.gif", 0, (0, 0), 3000)
        turtle.ontimer(turtle.bye, t=1000)

    def check_winning(x, y):
        # get size of puzzle from puzzle metadata
        tile_size = puzzle['size']

        # define click area around the blank tile
        click_parameter = tile_size * 1.5

        # find blank tile
        blank_pos = find_blank_square(board)

        # only check position if it's within tile size parameter from blank
        if (blank_pos[0].distance(x, y) <= click_parameter) and (y >= -149) \
                and (x <= 98):
            get_tile_pos(puzzle, score, username, win_con, board,
                         screen, moves)

    screen.onscreenclick(check_winning)

    return position


def error_log(error, function_name):
    '''
        Function to log errors into a file names "5001_puzzle.err"
    '''
    # get system time in raw format
    raw_system_time = datetime.datetime.now()

    # convert to local version of date and time
    local_timestamp = raw_system_time.strftime("%c")
    error_msg = (local_timestamp + " :Error: " + error + ". LOCATION: " +
                 function_name + "()\n")

    # write error message to file
    with open("5001_puzzle.err", mode="a", encoding="utf-8") as error_file:
        error_file.write(error_msg)


def read_leaderboard():
    '''
        Function to read the leaderboard and return the leaderboard as
        a list where each element is a player and their score.
        The function will sort the leaderboard and only displays the top
        10 players.
    '''
    leaderboard = []
    try:
        with open("leaderboard.txt", mode="r", encoding="utf-8") as in_file:
            for each in in_file:
                leaderboard.append(each)

        # clean up leaderboard list
        for i in range(len(leaderboard)):
            leaderboard[i] = leaderboard[i].strip()
            leaderboard[i] = leaderboard[i].split(":")
            leaderboard[i][1] = int(leaderboard[i][1])

        # sort leaderboard score
        leaderboard.sort(key=lambda x: x[1])

        # repackage leaderboard list
        for i in range(len(leaderboard)):
            leaderboard[i][1] = str(leaderboard[i][1])
            leaderboard[i] = ": ".join(leaderboard[i])
            leaderboard[i] = leaderboard[i] + "\n"

        return leaderboard

    except FileNotFoundError:
        # display no leaderboard error message
        Messages("Resources/leaderboard_error.gif", 0, (250, 100), 3000)

        # log error
        error = "Cannot find leader board"
        function_name = read_leaderboard.__name__
        error_log(error, function_name)

        # create another leaderboard
        with open("leaderboard.txt", mode="a",
                  encoding="utf-8") as leaderboard:
            leaderboard.write("")
    except IndexError:
        return leaderboard


def display_leaderboard(leaderboard):
    '''
        Function to display leaderboard
        Will only display top 10 of the leaderboard
    '''
    try:
        if len(leaderboard) > 0:
            # Make turtle to display names
            leader = turtle.Turtle()
            leader.hideturtle()
            leader.penup()
            leader.speed(0)
            leader.goto(200, 120)

            # get top 10 players from leaderboard
            top_10_leaderboard = leaderboard[:10]
            i = 1
            for each in top_10_leaderboard:
                leader.write(each, font=("Arial", 10, "bold"))
                leader.goto(200, 120-20*i)
                i += 1
        else:
            pass
    except TypeError:
        pass


def save_leader_board(score, username="Anon"):
    '''
        Function to save leaderboard
    '''
    # format entry
    entry = f"{username}: {score.__str__()} \n"

    # write entry
    with open("leaderboard.txt", mode="a", encoding="utf-8") as leaderboard:
        leaderboard.write(entry)


def main():

    # initialize screen
    screen = turtle.Screen()

    # initialize score
    score = ScoreKeeper()

    # load metadata for puzzles
    puz_data = load_metadata()

    # add tiles images to the turtle library
    add_tiles_images(puz_data)

    # display splash screen
    splash_screen(screen)

    # get username from a text dialogue
    username = user_name()

    # get number of moves from a text dialogue
    moves = num_moves()

    # draw game board
    draw_board()
    add_button()
    quit_button()

    # read leaderboard
    leaderboard = read_leaderboard()

    # display leaderboard
    display_leaderboard(leaderboard)

    # load puzzle
    board, num_cols, num_rows, puzzle = load_puzzle(score, screen, puz_data)

    # get winning tiles positions
    win_con = get_winning_array(board, num_cols, num_rows)

    # make load button
    load_button(score, screen, puz_data, moves, username)

    # make reset button
    reset_button(board, win_con, num_cols, num_rows)

    # scramble tiles
    scramble_tiles(board, num_cols, num_rows, puzzle)

    # find blank tiles
    find_blank_square(board)

    # get position of all tiles and check for winning configuration
    # everytime the tile is clicked

    get_tile_pos(puzzle, score, username, win_con, board, screen, moves)

    turtle.done()


if __name__ == "__main__":
    main()
