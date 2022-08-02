from string import ascii_lowercase, ascii_uppercase
from random import randint #used to select a random coordinate 
__package__ = "game_functions"

def test_input(valid_input):
    """
    Verfies that user input matches expected values
    :param valid_input: list of valid inputs
    :return validated input as a lowercase string
    """
    #verify user input using list option
    user_input = str()
    while user_input not in valid_input: 
        user_input = input("Yes or No?: ").lower()
    return user_input

def play_again(): 
    """
    Initiates the game, and gathers user input for game settings.
    Also used to repeat play.

    :param:
    :return: none
    :testcode: test.py \ initial_user_input

    """

    #current and future user input variables.
    radar_allowed = str() #user option: Enables 'radar' (hints). 
    play_input = str() # create play as a string var
    game_options = {} #reset game options if present
    game_options["options"] = ["y","n","yes","no"]
    game_options["row_height"] = int(10)
    game_options["column_width"] = int(10)
    game_options["max_radar_use"] = round(((game_options["row_height"] * game_options["column_width"]) / 15))
    #Valid sizes are 2-10. (Future input)      
    print("\nWelcome to Battleship!") #Opening message
    
    #verify user input using list option
    print("Would you like to play a game?")
    play = test_input(game_options["options"])
    if play in "y" + "yes": #check for a yes
        #verify input using option list
        print("Would you like radar support?")
        radar_support = test_input(game_options["options"])
        if radar_support in "y" + "yes": #check for a yes
            print("\nWise leaders use all available information.", end = " ")
            print("Wise leaders are weak.\n") #begin the game
            game_options["radar_allowed"] = radar_support
            play_game(game_options) #begin the game
        elif radar_support in "n" + "no": #check for no
            print("\nI don't need no stinking intel!") 
            #brave and smart are not often bedfellows
            print("Have a great game!\n") #be nice
            game_options["radar_allowed"] = radar_support
            play_game(game_options) #begin the game
        else:
            print("Code WTF") #in case my code is worse than I thought
    elif play_input in "n" + "no": #check for no
        print("Well shucks...") #cry quietly
        raise SystemExit #abort!
    else:
        print("Program Failure - Mod: play_again | User Inputs Check")
        
    return

def build_board(game_options):
    """
    Build_board is used to draw the board, and fill it with empty 'ocean' tile
    based on game options column_width and row_height. This is done as a list
    of lists. Each row will contain a list of strings (" O ") for each column.
    
    :param game_options: global dictionary of game options
    :return: a list of lists called board is returned as described above.
    :testcode: test.py \ test_board_build
    """

    empty_board = [] #initiate a temp variable list
    for i in range(game_options["row_height"]): #loop through required rows
        column = [] #create a column list
        for j in range(game_options["column_width"]): #loop through required columns
            column.append(" O ") #create empty 'ocean' blocks
        empty_board.append(column) #add the row list as a new column on the board
    return empty_board #return the empty ocean board

def ship_hider(game_boards, game_options, ship_coords, key):
    """
    Uses the enemy_ship_placement dictionary with board height and length to iterate through hiding ships in unique locations
    :param ship_name: a string representing the name of a ship. Example: "battleship"
    :return: test_ship_placement: used by hide_ships to store a single ships coords as a list in a dictionary paired to a ship_name key 
    :testcode:

    """
    #randomized positions for hiding ships
    axis_select = bool(randint(1,2) % 2) #random T/F. T = hor, F = vert
    rand_row = randint(0, game_options["row_height"] - 1) #rand row select
    rand_col = randint(0, game_options["column_width"] - 1) #rand column select
    index = int(0) #create an index integer for use in coordinate definition
    
    test_ship_placement = [] #stores ship coordinates for testing overlap
    ship_coord = [] #used to store an integer list of coordinates for the ship

    if axis_select == True: #tests true and executes for hor positioning
        axis_select = bool(randint(1,2) % 2) #reset axis select
        while (rand_col + game_options["define_ships"][key][1]) >= (game_options["column_width"] - 1):
            rand_col = (rand_col + game_options["define_ships"][key][1])\
                    - (game_options["column_width"] - 1) #new rand start pt
        for hor_len in range(game_options["define_ships"][key][1]): 
            #populate the list of ship coordinates
            index = hor_len + rand_col #incremental index to build ship horizontally
            game_boards[ship_coords][key].append(str(rand_row) + ":" + str(index)) 
    elif axis_select == False: #tests false and executes for ver positioning
        axis_select = bool(randint(1,2) % 2) #rest axis select
        while (rand_row + game_options["define_ships"][key][1]) >= (game_options["row_height"] - 1):
            rand_row = (rand_row + game_options["define_ships"][key][1])\
                    - (game_options["row_height"] - 1) #new rand start pt
        for vert_hgt in range(game_options["define_ships"][key][1]): 
            #populate the list of ship coordinates
            index = vert_hgt + rand_row #incremental index to build ship horizontally
            game_boards[ship_coords][key].append(str(index) + ":" + str(rand_col)) 
    else:
        print("Program Failure - Mod: ship_hider | axis_select check")

    return test_ship_placement #return the non-overlapping ship coordinates

def hide_ships(game_options, game_boards, ship_coords):
    """
    Hides ships using random starting points & direction (horizontal/vertical)
    :param:
    :return:
   :testcode:

    """
    #hides ships on the hidden_ships board and stores them as a dictionary.
    #format: key of ship name paired to a list of ship coords based on length.
    game_options["define_ships"] = {"carrier":[1,5],"battleship":[2,4],\
        "cruiser":[3,3],"submarine":[4,3],"destroyer":[5,2]}

    for key in game_options["define_ships"]:
        game_boards[ship_coords][key] = []
        ship_hider(game_boards, game_options, ship_coords, key)
    return

def print_board(board, game_options):
    """  
    :param:
    :return:
    :testcode:
    """
    
    index = 1 #counts loops for creating and formatting new lines
    count = 0 #indexes the valid_rows_display var
    border_bar = "" #stores the length of the top and bottom bars
    column_labels = str() #stores a string of the formatted column labels
    
    #format column labels for printing based on board length
    for i in range(len(game_options["valid_columns_display"])):
        column_labels += (" " + str(game_options["valid_columns_display"][i])\
            + "  ")
    #format a string to use as a top and bottom border for the board
    for i in range(len(column_labels)-2): 
        border_bar += "_" #add underlines for the length of the column labels
    print("    %s" % column_labels) #print the column labels
    print("\n  " + "  __" + border_bar) #create a top border

    for list in board: #iterate through rows (lists)
        for item in list: #iterate through columns (list items)
            if index == 1: #print row labels on the first line
                print("%2s |" % (str(game_options["valid_rows_display"]\
                    [count])), end = "") #print row label
            print(item, end = " ") #print the indexed var
            #format new lines at the end of board width
            if index % len(game_options["valid_columns_display"]) == 0: 
                print("| " + str(game_options["valid_rows_display"][count]))
                count += 1 #increment count for use in labeling rows
                #reset count if above the size of board height
                if count > len(game_options["valid_rows_display"]) :
                    count = 0 #reset var    
            index += 1 #increment var used for horizontal sizing
            #reset var if above board width
            if index > len(game_options["valid_columns_display"]):
                index = 1 #reset var 
    print("  " + "  __"  + border_bar) #print a bottom border
    print("    %s" % column_labels) #print the column labels
    print("\n")

    return #none 

def radar_report(game_boards, game_options):
    """

    Needs fucntionality added to ensure radar does not report coordinates
    that have already been hit.

    :param:
    :return: 
    :testcode:

    """

    test_list = list()
  
    if len(game_boards["hints_given"]) >= game_options["max_radar_use"]:
        #print no more uses message
        print("\n\n\n" + "-"*65)
        print("Captain the radar officer is screaming something", end = " ")
        print("about giving it all they've got in a Scottish accent.")
        print("You're on your own.")
        print("-"*65 + "\n\n\n")
        return
    
    for key in game_boards["p2_ship_coords"]:
        test_list += game_boards["p2_ship_coords"][key]
    index_select = randint(0, len(test_list)-1)
    hint = str(test_list[index_select])
    
    while hint in game_boards["hints_given"]:
        index_select = randint(0, len(test_list)-1)
        hint = str(test_list[index_select])
    else:
        game_boards["hints_given"].append(hint)
    
    #reformat hint for user display indexes
    hint_temp = hint.split(":") #splits the hint into a two item tuple
    h = game_options["valid_rows_display"][int(hint_temp[0])]
    v = game_options["valid_columns_display"][int(hint_temp[1])]
    hint = (h + ":" + str(v))

    #print radar report
    print("\n\n\n" + "-"*65)
    print("Captain the radar officer is", end = " ")
    print("reporting activity at coordinates %s." % (hint))
    print("You've used radar %s times. You have %s uses left." % \
        (len(game_boards["hints_given"]), (game_options["max_radar_use"] - \
            len(game_boards["hints_given"]))))
    print("-"*65 + "\n\n\n")

    return 

def launch_missile(game_options, game_boards):
    """
  
    :param: game_options: global dictionary of game options
    :param: game_boards: global dictionary of game play boards
    :return: target_row and target_column formatted for use referencing list indexes
    :testcode:

    """
    coord_input = str() #initialize the user input variable with 0
    target_row = int() #define input variable for row
    target_column = int() #define input variable for column

    while target_row not in game_options["valid_rows_display"] or \
        target_column not in game_options["valid_columns_display"]:
        print("*"*55)
        print("      TEST: Tactical Execution System Targetting    ") 
        print("\n  Provide strike coordinates.") 
        print("  Example: Launch at the 2nd row's 3rd column use B3.") 
        print("  Valid rows are:   ", end = " ") 
        for i in game_options["valid_rows_display"]: #format and print 
            print(i, end = " ") #format to print on the same line 
        print("\n  Valid columns are:", end = " ")
        for i in game_options["valid_columns_display"]: #format and print
            print(i, end = " ") #format to print on the same line
        print("\n" + "*" * 55)  
        
        print("To retreat from battle in disgrace,", end = " ")
        print("forever being deemded a coward:")
        print("Enter your new name: loser\n")
        
        if game_options["radar_allowed"].lower() == "y":
            print("To ask for an intel report from the radar officer:")
            print("Enter: radar")
            print("*" * 55)
            print("\n")
            coord_input = input("Enter target coordinates, " + \
                "or option (radar (hint) | loser (quit): ")
        else:
            print("*" * 55)
            coord_input = \
                input("\nEnter coordinates, or option (loser (quit)): ")
        
        if coord_input.lower() == "loser":
            print("\nYou have brought shame down upon yourself,", end = " ")
            print("your name, your country, and your family.")
            print("Don't let it get to you. Have a great day!")
            raise SystemExit #abort I'm not worthy!
        elif coord_input.lower() == "radar":
            radar_report(game_boards, game_options)
        
        #set target_row to the upper case version of the 1st character
        target_row = coord_input[0].upper() 
        #set the target_column to the remainder of the string, allows 2+ digit
        target_column = coord_input[1:len(coord_input)]
        
        if target_column.isnumeric() == False: #very int conversion 
            target_column = int(0) #set it to 0 to continue the while loop
        target_column = int(target_column) #convert to an integer
    
    print("\nMissile Guidance Confirmed: Target Row:", end = " ")
    print("%2s | Target_Column: %2s | Coordinates: %2s" % \
        (target_row, target_column, (str(target_row) + str(target_column))))

    #convert user indexing from alpha to numeric index starting at 0
    target_row = game_options["valid_rows_display"].index(target_row) 
    target_column -= 1 #convert user indexing to system indexing starting at 0
    
    return target_row, target_column

def print_stats(game_options):
    """
    print_stats is used to format and print the game statistics
    
    :param: game_options: global dictionary of game options    
    :return: none
    :testcode: 

    """
    
    print("\n") 
    print(" " + "_" * 39) 
    print("|                                       |") 
    print("| Missiles fired:             %3s" % \
        str(game_options["p1_missiles_fired"]) + "       |")
    print("| Direct hits:                %3s" % \
        str(game_options["p1_direct_hits"]) + "       |")
    print("| Targetting accuracy:        %4s" % \
        str("{:.0%}".format(game_options["p1_direct_hits"] / \
            game_options["p1_missiles_fired"])) + "      |") 
    print("| Enemy hit points remaining: %3s / %3s |" % \
        (game_options["p1_hits_required"] - game_options["p1_direct_hits"], \
            game_options["p1_hits_required"])) #remaining hit points \ total
    print("|" + "-" * 39 + "|")
    #print(" " + "_" * 39) 
    print("\n") 
    
    return

def play_game(game_options):
    """
    Used for primary game fucntion after obtaining game play options from user
    :param: game_options: global dictionary of game options
    :return: none
    :testcode: 

    """
    #initialize module variables
    game_options["p1_missiles_fired"] = int(0) #variable to count attempts
    game_options["p1_direct_hits"] = int(0) #integer to track hits
    game_options["p2_missiles_fired"] = int(0) #integer to count attempts
    game_options["p2_direct_hits"] = int(0) #integer to track hits
    target_row = str()
    target_column = str()

    #create the valid_rows_display list.
    #Used to display the board, and verify board size.
    game_options["valid_rows_display"] = [] #initialize the empty list
    for i in range(0, game_options["row_height"]): 
        game_options["valid_rows_display"].append(ascii_uppercase[i]) 

    #create the valid_rows_compute list
    #valid indice. Used to for computations and checks.
    game_options["valid_rows_compute"] = [] #initialize the empty list
    for i in range(0, len(game_options["valid_rows_display"])):
        game_options["valid_rows_compute"].append(int(i)) 
    
    #create the valid_columns_display list
    game_options["valid_columns_display"] = [] #initialize the empty list
    #Used to display the board, and verify board size
    for i in range(1, game_options["column_width"] + 1): 
        game_options["valid_columns_display"].append(int(i))

    #create the valid_rows_compute list
    #valid indice. Used to for computations and checks.
    game_options["valid_columns_compute"] = [] #initialize the empty list
    for i in range(len(game_options["valid_columns_display"])):
        game_options["valid_columns_compute"].append(int(i))

    #two payer functionality is not yet designed
    #dictionary used to pass display boards and ship coords between functions
    game_boards = {}
    game_boards["p1_display_board"] = [] #displays game map to player 1
    game_boards["p2_display_board"] = [] #displays game map to player 2
    game_boards["p1_ship_coords"] = {} #stores player 1's ship coordinates.
    game_boards["p2_ship_coords"] = {} #stores player 2's ship coordinates.
    game_boards["hints_given"] = [] #stores hints that have been provided
    #Multiplayer function does not exist yet

    print("\n")
    game_boards["p1_display_board"] = build_board(game_options) #p1 display
    game_boards["p2_display_board"] = build_board(game_options) #p2 display
    
    #holds players ships for attack verification, two player = future
    hide_ships(game_options, game_boards, "p1_ship_coords")
    hide_ships(game_options, game_boards, "p2_ship_coords")
    game_options["p1_hits_required"] = int(0) #sum ship lengths = hit count
    for ship in game_boards["p1_ship_coords"]:
        game_options["p1_hits_required"] += \
            game_options["define_ships"][ship][1]
    game_options["p2_hits_required"] = int(0) #sum ship lengths = hit count 
    for ship in game_boards["p2_ship_coords"]:
        game_options["p2_hits_required"] += \
            game_options["define_ships"][ship][1]

    print(print_board(game_boards["p1_display_board"], game_options)) 
    print("\n") #formatting  (new lines)
    
    
    while game_options["p1_direct_hits"] < game_options["p1_hits_required"]:
        target_row, target_column = launch_missile(game_options, game_boards) 
        test_list = list()
        for key in game_boards["p2_ship_coords"]:
            test_list += game_boards["p2_ship_coords"][key]

        if game_boards["p1_display_board"][target_row][target_column] == " M ":
            game_options["p1_missiles_fired"] += 1 #increment count
            print("Sorry Captain, ", end = "")
            print("still no ship in that spot. No need to fire twice.")
            print_stats(game_options)
            print(print_board(game_boards["p1_display_board"], game_options))

        elif game_boards["p1_display_board"][target_row][target_column] \
            == " X ":
            game_options["p1_missiles_fired"] += 1 #increment count
            print("Those coordinates are still a hit.", end = " ")
            print("You're nothing if not thorough.") #insult the user
            print_stats(game_options)
            print(print_board(game_boards["p1_display_board"], game_options))

        elif (str(target_row) + ":" + str(target_column)) in test_list:
            game_options["p1_missiles_fired"] += 1 #increment count
            game_options["p1_direct_hits"] += 1 #increment count
            print("Captain, that's a direct hit!") #stroke user ego
            print_stats(game_options)
            game_boards["p1_display_board"][target_row][target_column] = " X "
            print(print_board(game_boards["p1_display_board"], game_options))

        elif (str(target_row) + ":" + str(target_column)) not in test_list:
            game_options["p1_missiles_fired"] += 1 #increment count
            print("Captain, that strike missed.") #tell captain of poor choice
            print_stats(game_options)
            game_boards["p1_display_board"][target_row][target_column] = " M "
            print(print_board(game_boards["p1_display_board"], game_options))
        else:
            print("Error in play_game hit verification logic")
    print("\n") #formatting  (new lines)
    print("Congratulations Captain! You've destroyed the enemy fleet!") 
    play_again(game_options)
    
    return #play_game is operational and returns no values
