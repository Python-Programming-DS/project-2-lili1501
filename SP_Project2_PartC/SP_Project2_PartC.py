"""
TIC TAC TOE GAME
> Description:
A 2 player program built to play tic tac toe

File used tictac_single.txt
> Objective: To train the ML model using txt file to maximize to predict
the best move for the computer using the trained model

By: Shesadree Priyadarshani
    
"""

import random
import joblib

# Reading the saved ML model from the SP_Project2_PartC directory
# to save time on training the model again
model = joblib.load('SP_Project2_PartC/best_tictac_model.pkl')
print ("Model loaded successfully.")

# Converting the board to input features and labels for pretrained ML model
# returning the board as 2D list from 1D list
def board_to_features_labels(board):
    mapping = {'X': 1, 'O': -1, ' ': 0}
    oneD_list = []
    for row in board:
        for box in row:
            oneD_list.append(mapping[box])
    return [oneD_list]

# define Board class to building the Game Board:

class Board:
     # this constructor initiates the board with empty cells
    def __init__(self):
        self.c = [[" "," "," "],
                  [" "," "," "],
                  [" "," "," "]]
      
    # this method prints the board. Recall that class methods are functions
    def printBoard(self):
        # it first prints the BOARD_HEADER constant
        # BOARD_HEADER constant
        BOARD_HEADER = "-----------------\n|R\\C| 0 | 1 | 2 |\n-----------------"
        print(BOARD_HEADER)

        # using a for-loop, it increments through the rows
        for i in range(3):
            print(f"| {i} | {self.c[i][0]} | {self.c[i][1]} | {self.c[i][2]} |")
            print("-----------------")
        
    def movesLeft(self):
        moves = []
        for row in range(3):
            for col in range(3):
                if self.c[row][col] == " ":
                    moves.append((row,col))
        return moves

    
# define Game class to implement the Game Logic:

class Game:

    # the constructor
    def __init__(self):
        self.board = Board()
        self.turn = 'X'

    # this method switches players 
    def switchPlayer(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'

    
    # this method validates the user's entry
    def validateEntry(self, row, col):
        # Check if row and col entered are in range
        if row < 0 or row > 2 or col < 0 or col >2:
            print(f"Invalid entry: try again.\nRow & column numbers must be either 0, 1, or 2.")

        # Check if the cell is available
        elif self.board.c[row][col] != " ":
            print(f"That cell is already taken.\nPlease make another selection.")

        else:
            print("Thankyou for your selection")
            return True
        return False


    # this method checks if the board is full
    def checkFull(self):
        for i in range(3):
            for j in range(3):
                if self.board.c[i][j]==" ":
                    return False
        # print("\nDRAW NOBODY WINS!")
        return True


    
    # this method checks for a winner
    def checkWin(self,player):
        board = self.board.c
        for i in range(3):
            if i == 0:
                if board[i][i] == player and board[i+1][i+1] == player and board[i+2][i+2] == player:
                    return True
                if board[i][i+2] == player and board[i+1][i+1] == player and board[i+2][i] == player:
                    return True
            if board[i][0] == player and board[i][1] == player and board[i][2] == player:
                return True
            if board[0][i] == player and board[1][i] == player and board[2][i] == player:
                return True
        return False
        

    # this method checks if the game has met an end condition by calling checkFull() and checkWin()
    def checkEnd(self):
        if self.checkWin('X'):
            print(f"X IS THE WINNER!")
            return True
        elif self.checkWin('O'):
            print(f"O IS THE WINNER!")
            return True
        elif self.checkFull():
            print("\nDRAW NOBODY WINS!")    
            return True
        return False    
        
    '''
        The ML model looks at the current board and picks the best cell(0-8)
        and convert the cell into row and column index as defined in tictac_single.txt
        if the predicted best move is not available, 
        it randomly picks one from the available cells
    '''
    def get_best_move_ml(self):
        features = board_to_features_labels(self.board.c)
        predictions = model.predict(features)[0]
        
        row = predictions // 3
        col = predictions % 3

        if self.board.c[row][col] != " ":
            cell_available = self.board.movesLeft()
            if cell_available is None:
                return None
            row, col = random.choice(cell_available)
        return (row, col)
        

    # this method initiate the tic-tac-toe game
    def playGame(self):
        print("\nHey Player! Let's play Tic-Tac-Toe!")
        self.board.printBoard()
        print(f"New Game: Player X goes first\n")
        while True:
            print(f"\n{self.turn}'s turn")
            if self.turn == 'X':
                print(f"Where do you want your {self.turn} placed?")
                #To highlight the user input as red
                print("\033[0mPlease enter row number and column number separated by a comma:\033[91m", end="\n")
                try:
                    row, col = map(int, input().split(",")) 
                except ValueError:
                    #To bring back the terminal back to default color text
                    print("\033[0m", end="")
                    print("Invalid input. Please enter two numbers separated by a comma.")
                    continue

                #To bring back the terminal back to default color text
                print("\033[0m", end="")
                print(f"You have entered row #{row}\n\t  and column #{col}")

                if self.validateEntry(row, col) == False:
                    continue
    
            # if the turn is O then computer makes its best move to maximise 
            # its chance of winning
            else:
                print(f"Computer is predicting its best move...")
                move = self.get_best_move_ml()
                if move:
                    row, col = move
                    print(f"Computer chose row #{row}\n\t and column #{col}")
                else:
                    print("No moves left!")
                    break
                


            self.board.c[row][col] = self.turn
            self.board.printBoard()

            if self.checkEnd() == True:
                break

            self.switchPlayer()

# main function
def main():
    # first initializes a variable to repeat the game
    another_game = 'y'

    # using while-loop that runs until the user says no for another game
    while another_game.lower() == 'y':
        tic_tac_toe = Game()
        tic_tac_toe.playGame()
        print("\n\033[0mAnother game? Enter Y or y for yes:\033[91m", end="\n")
        another_game = input()
        print("\033[0m", end="")
    
    print("Thank you for playing!")

if __name__ == "__main__":
    main()
