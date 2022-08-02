#Module Import
import string

# Variable Declaration
vertical_height = 10
horizontal_length = 10
alphabet = list(string.ascii_uppercase) #used to create row labels and verify row data
board = []
hidden_ships = []
option = ("y","n")

def build_board (vertical_height, horizontal_length):
    #Function to draw the board
    board = []
    for i in range(vertical_height):
        column = []
        for j in range(horizontal_length):
            column.append(" X ")
        board.append(column)
    return board

#def build_board (vertical_height, horizontal_length):
#    #Function to draw the board
#    column = []
#    board = []
#    for i in range(horizontal_length):
#        column.append(" X ")
#    for i in range(vertical_height):
#        board.append(column)
#    return board

def print_board(board, horizontal_length, vertical_height,alphabet):
    index = 1 #used to count loops for creating and formatting new lines
    border_bar = "  __" #used to store the length of the top and bottom bars
    count = 0 #Used for indexing the alphabet var
    column_labels = "   " #used to label the columns
    
    for i in range(horizontal_length): #Create the border bar and column labels based on board width
        border_bar = border_bar + "____" #Append lines to border bar
        column_labels = column_labels + " " + str(1 + i) + "  " #Add number labels to column label var
    
    print(column_labels) #label the columns
    print(border_bar) #create a top border
    print("\n") #create a new line
    
    for i in board: #iterate through rows
        for j in i: #iterate through columns
            if index == 1: #print row labels on the first line
                print(alphabet[count] + " |", end = "") #print row label
            print(j, end = " ") #print the indexed var                
            if index % horizontal_length == 0: #format new lines at the end of board width
                print(" | " + alphabet[count] + "\n") #label the row and begin new line
                count += 1 #increment count for use in labeling rows
                if count > vertical_height: #reset count if above the size of board height
                    count = 0 #reset var                    
            index += 1 #increment var used for horizontal sizing
            if index > horizontal_length: #reset var if above board width
                index = 1 #reset var
    print(border_bar) #print a bottom border
    return column_labels #print the lower column labels

def launch_missile(alphabet):
    target_row = "" #define input variable for row
    target_column = "" #define input variable for column
    valid_row = alphabet[0:vertical_height] #create a list of valid row inputs
    valid_column = [*range(1, horizontal_length+1, 1)] #create a list of valid column inputs
    
    while target_row.isalpha() == False or target_row not in valid_row: #prompt for valid input
        try:
            target_row = input("Which row letter will you strike?" + str(valid_row)) #gather row input
        except:
            pass #pass exceptions back to the loop
        else: #format and print user input
            target_row = target_row.upper() #store as upper case
            #print(target_row + "\n") #print the users input
    while target_column not in valid_column: #prompt for valid input
        try:
            target_column = input("Which column number will you strike?" + str(valid_column)) #gather column input
            try:
                target_column = int(target_column) #attempt to convert user input to an integer
            except:
                pass #pass exceptions back to the loop
        except:
            pass #pass exceptions back to the loop
        return target_row, target_column - 1 #subtracting 1 accounts for 0 index

def hide_ships(board_map):
    hidden_ships = board_map
    #carrier (5)
    hidden_ships[0][1] = " O "
    hidden_ships[0][2] = " O "
    hidden_ships[0][3] = " O "
    hidden_ships[0][4] = " O "
    hidden_ships[0][5] = " O "
    #battleship (4)
    hidden_ships[7][1] = " O "
    hidden_ships[7][2] = " O "
    hidden_ships[7][3] = " O "
    hidden_ships[7][4] = " O "    
    #cruiser (3)
    hidden_ships[2][1] = " O "
    hidden_ships[2][2] = " O "    
    hidden_ships[2][3] = " O "
    #submarine (3)
    hidden_ships[7][9] = " O "
    hidden_ships[8][9] = " O "    
    hidden_ships[9][9] = " O "    
    #destroyer (2)
    hidden_ships[3][6] = " O "
    hidden_ships[4][6] = " O "    
    return hidden_ships
    
def play_again(): #Game opening
    play = str()
    print("\nWelcome to Battleship!")
    while play.lower() not in option:
        try:
            play = input("Would you like to play a game? (Y/N): ").lower()
        except:
            pass
        else:
            if play == "y":
                print("Have a great game!\n")
                play_game()
            else:
                print("Well shucks...")
                raise SystemExit
def play_game():
    #build one board to show missile strikes, and one to hide enemy ships
    board = build_board(vertical_height, horizontal_length) #build board based on height & width vars
    hidden_ships = build_board(vertical_height, horizontal_length) #build a 2nd board to store hidden ships
    hidden_ships = hide_ships(hidden_ships)# hide ships on the hidden board
    hits_required = int(0)
    for i in range(vertical_height):
        hits_required = hits_required + hidden_ships[i].count(' O ')
    missiles_fired = int(0)
    direct_hits = int(0)

    print(print_board(board, horizontal_length, vertical_height, alphabet)) #print the board to screen
    print("\n")
    #print(print_board(hidden_ships, horizontal_length, vertical_height, alphabet)) #print the hidden ships to screen
    while direct_hits < hits_required:
        target_row, target_column = launch_missile(alphabet) #run launch missile module to accept target coordinates
        print("\n" * 5)
        print("\nYou launch a ship to ship missile at coordinates: " + target_row + str(target_column + 1) + "\n") #let the user know where they attack add 1 for 0 index
        target_row_int = alphabet.index(target_row)#create an integer variable for the row letter chosen
        if hidden_ships[target_row_int][target_column] == " O ":
            missiles_fired += 1
            direct_hits += 1
            targetting_accuracy = int(100 * direct_hits / missiles_fired)
            print("Captain, that's a direct hit!")
            print("Missiles fired:      " + str(missiles_fired))
            print("Direct hits:         " + str(direct_hits))
            print("Targetting Accuracy: " + str(targetting_accuracy) + " %")
            print("\n")
            board[target_row_int][target_column] = " H "
            print(print_board(board, horizontal_length, vertical_height, alphabet)) #print the board to screen
        else:
            missiles_fired += 1
            direct_hits += 0
            targetting_accuracy = int(100 * direct_hits / missiles_fired)
            print("Captain, that strike missed.")
            print("Missiles fired:      " + str(missiles_fired))
            print("Direct hits:         " + str(direct_hits))
            print("Targetting Accuracy: " + str(targetting_accuracy) + " %")
            print("\n")
            board[target_row_int][target_column] = " M "
            print(print_board(board, horizontal_length, vertical_height, alphabet)) #print the board to screen
    print("\n")
    print("Congratulations Captain! You've destroyed the enemy fleet!") 
    play_again()

play_again()
