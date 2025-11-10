"""
TIC TAC TOE GAME
> Description:
A 2 player program built to play tic tac toe

File used Project2_PartA.py
> Objective: To implement min max logic to maximize the computer's chance of winning

By: Shesadree Priyadarshani
    
"""

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
        
    def minmax_score(self,is_maximizing):
        # return 1 if computer wins (O), -1 if player wins (X), 0 for draw
        if self.checkWin('O'):
            return 1
        if self.checkWin('X'):
            return -1
        if self.checkFull():
            return 0
        
        '''
           turn checks which player's making a move right now
           Intializing best_move whether we are maximizing or minimizing

           if the computer(O) is maximizing, we set best_move to negative infinity
           if the player(X) is minimizing, we set best_move to positive infinity
        '''
        if is_maximizing:
            player = 'O'
            best_move = -float('inf')   
        else:
            player = 'X'
            best_move = float('inf')
            
        
        ''' 
            for each available move we get from movesLeft,
            we simulate the move by placing the ('O','X') on the board,
            let the oponent play their best move(recursively),undo the move.
            Decide which move led to the best score and return that score
        '''
        for row, col in self.board.movesLeft():
            self.board.c[row][col] = player
            score = self.minmax_score(not is_maximizing)
            self.board.c[row][col] = " "
            
            if is_maximizing:
                best_move = max(score, best_move)
            else:
                best_move = min(score, best_move)
        return best_move
    
    def get_best_move(self):
        #intialise the best score and move
        best_score = -float('inf')
        best_move = None

        # Find the best move for the computer (O)
        for row, col in self.board.movesLeft():
            self.board.c[row][col] = 'O'
            score = self.minmax_score(False)
            self.board.c[row][col] = " "
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_move
        

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
                print(f"Computer is taking its time thinking...")
                move = self.get_best_move()
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
