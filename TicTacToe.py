import math
numbers = ["1","2","3","4","5","6","7","8","9"]
MoveStack = []

def display_board(board):
    print("")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def CreateBoard():
    return [[f"{(i + j * 3) + 1 }" for i in range(3)] for j in range(3)]

def CheckWinner(board):
    for row in board:
        if "".join(row) == "XXX" or "".join(row) == "OOO":
            return True
    
    pattern = ""
    for i in range(3):
        pattern =  board[0][i] + board[1][i] + board[2][i]
        if pattern == "XXX" or pattern == "OOO":
            return True
    pattern = ""
    row = 0
    col = 0
    
    for _ in range(3):
        pattern += board[row][col]
        row += 1
        col += 1
    if pattern == "XXX" or pattern == "OOO":
        return True
    pattern = ""
    row = 0
    col = 2
    
    for _ in range(3):
        pattern += board[row][col]
        row += 1
        col += -1
        if pattern == "XXX" or pattern == "OOO":
            return True
        
    return False

def findIJ(number):
    for j in range(3):
        for i in range(3):
            if (i + j * 3) + 1 == number:
                return (j,i)
                   
def enter_letter(board, player,number):
    original = findIJ(number)
    row = original[0]
    col = original[1]
    if 0 <= row < 3 and 0 <= col < 3 and board[row][col] in numbers:
        board[row][col] = player
        MoveStack.append(number)
        return True
    else:
        print("Invalid move. Try again.")
        return False
    
def UndoMove(board):
    move = MoveStack.pop()
    original = findIJ(move)
    row = original[0]
    col = original[1]
    board[row][col] = f"{move}"

def GetMoves(board):
    Moves = []
    for i in range(3):
        for j in range(3):
            if board[j][i] in numbers:
                Moves.append(board[j][i])
    return Moves

def FullBoard(board):
    return all(all(char.isalpha() for char in element) for row in board for element in row)

def MiniMax(board,MaximisingPlayer):
    if CheckWinner(board):
        if MaximisingPlayer:
            #someone one and it wasnt the bots turn because it's their turn now
            return [None,-1]  
        else:
            return [None,1]
    elif FullBoard(board):
        return [None,0]
    
    if MaximisingPlayer:
        maxEval = -math.inf
        BestMove = 0
        for move in GetMoves(board):
            enter_letter(board, "O", int(move))
            currentEval = MiniMax(board,False)[1]
            UndoMove(board)
            if maxEval < currentEval:
                maxEval = currentEval
                BestMove = int(move)
        return [BestMove,maxEval]
    else:
        minEval = math.inf
        for move in GetMoves(board):
            enter_letter(board, "X", int(move))
            currentEval = MiniMax(board,True)[1]
            UndoMove(board)
            minEval = min(currentEval,minEval)
        return [None,minEval]
    
def MiniMaxAB(board,MaximisingPlayer,alpha,beta):
    if CheckWinner(board):
        if MaximisingPlayer:
            #someone one and it wasnt the bots turn because it's their turn now
            return [None,-1]  
        else:
            return [None,1]
    elif FullBoard(board):
        return [None,0]
    
    if MaximisingPlayer:
        maxEval = -math.inf
        BestMove = 0
        for move in GetMoves(board):
            enter_letter(board, "O", int(move))
            currentEval = MiniMaxAB(board,False,alpha,beta)[1]
            UndoMove(board)
            alpha = max(alpha,currentEval)
            if maxEval < currentEval:
                maxEval = currentEval
                BestMove = int(move)
            if beta <= alpha:
                break
        return [BestMove,maxEval]
    
    else:
        minEval = math.inf
        for move in GetMoves(board):
            enter_letter(board, "X", int(move))
            currentEval = MiniMaxAB(board,True,alpha,beta)[1]
            UndoMove(board)
            minEval = min(currentEval,minEval)
            beta = min(beta,currentEval)
            if beta <= alpha:
                break
        return [None,minEval]


def TicTacToe():
    # "X" is the player "O" is the computer
    board = CreateBoard()
    display_board(board)
    ans = input("Do you want to go first (yes/no): ")
    while ans != "yes" and ans != "no":
        ans = input("Do you want to go first (yes/no): ")

    player_turn = "X" if ans == "yes" else "O"
    GameOver = False
    while not GameOver:
        if player_turn == "O":
            alpha = -math.inf
            beta = math.inf
            number = MiniMaxAB(board,True,alpha,beta)
        else:
            try:
                number = []
                move = int(input(f"Enter your move (1 to 9) (Anything else to Exit): "))
                number.append(move)
                if number[0] > 9 or number[0] <= 0:
                    exit()
            except:
                exit()
        if enter_letter(board, player_turn,number[0]):
                    display_board(board)
                    if CheckWinner(board):
                        print(f"{"Player" if player_turn == "X" else "Computer"} wins!!") 
                        GameOver = True
                    elif FullBoard(board):
                        print("Draw") 
                        GameOver = True
                    # Switch to the other player's turn
                    player_turn = "O" if player_turn == "X" else "X"
                    number = []
        if GameOver:
            Again = input("Do you want to play again (y/n): ").lower()
            while Again != "y" and Again != "n":
                Again = input("Please enter 'y' or 'n': ").lower()
            GameOver = True if Again == "n" else False
            if not GameOver:
                ans = input("Do you want to go first (yes/no): ")
                while ans != "yes" and ans != "no":
                    ans = input("Do you want to go first (yes/no): ")
                player_turn = "X" if ans == "yes" else "O"
                board = CreateBoard()
                display_board(board)



TicTacToe()
 
