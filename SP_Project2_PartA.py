"""
Tic-Tac-Toe

This program is a simple Tic-Tac-Toe game using classes and objects.
    
    
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
        print("\nDRAW NOBODY WINS!")
        return True


    
    # this method checks for a winner
    def checkWin(self):
        board = self.board.c
        turn = self.turn
        for i in range(3):
            if i == 0:
                if board[i][i] == turn and board[i+1][i+1] == turn and board[i+2][i+2] == turn:
                    print(f"{turn} IS THE WINNER!")
                    return True
                if board[i][i+2] == turn and board[i+1][i+1] == turn and board[i+2][i] == turn:
                    print(f"{turn} IS THE WINNER!")
                    return True
            if board[i][0] == turn and board[i][1] == turn and board[i][2] == turn:
                print(f"{turn} IS THE WINNER!")
                return True
            if board[0][i] == turn and board[1][i] == turn and board[2][i] == turn:
                print(f"{turn} IS THE WINNER!")
                return True
        return False
        

    # this method checks if the game has met an end condition by calling checkFull() and checkWin()
    # hint: you can call a class method using self.method_name() within another class method, e.g., self.checkFull()
    def checkEnd(self):
        if self.checkWin() == True :
            return True
        elif self.checkFull() == True:
            return True
        else:
            return False
    


    # this method runs the tic-tac-toe game
     # hint: you can call a class method using self.method_name() within another class method
    def playGame(self):
        print("\n Hey Player! Let's play Tic-Tac-Toe!")
        self.board.printBoard()
        print(f"New Game: Player X goes first\n")
        while True:
            print(f"\n{self.turn}'s turn")
            print(f"Where do you want your {self.turn} placed?")
            #To highlight the user input as red
            print("\033[0mPlease enter row number and column number separated by a comma:\033[91m", end="\n")
            row, col = map(int, input().split(","))

            #To bring back the terminal back to default color text
            print("\033[0m", end="")
            print(f"You have entered row #{row}\n\t  and column #{col}")

            if self.validateEntry(row, col) == True:
                self.board.c[row][col] = self.turn
                self.board.printBoard()

                if self.checkEnd() == True:
                    break

                self.switchPlayer()
                # self.board.printBoard()




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
