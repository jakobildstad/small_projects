import numpy as np
from itertools import product

path = <Enter file path>
run_game = True

def main():
    board = startup_program()

    while not is_win(board) and run_game:
        print_board(board)
        print_info()
        ask_and_update(board)

    if is_win(board):
        print_board(board)
        print("STATUS: Game won. Congratulations!")
    else:
        print("STATUS: Shutting off.")


def ask_and_update(board):
    nl1 = ["1", "2", "3", "4", "5", "6", "7", "8", "9"] #numberlist 1 and 2
    nl2 = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]

    while True:
        ans = input("--->  ")
        if valid_ans(ans, nl1, nl2):
            break

    if ans[0:4] == "save":
        try:
            if ans[-4:] != ".txt":
                print("Did you remember the filename with .txt at the end?")
                while True:
                    ans = input("--->  ")
                    if ans[-4:] == ".txt":
                        break
            np.savetxt(path + ans[5:], board, fmt="%s")
            print(f"STATUS: Game saved as {path + ans[5:]}")
        except Exception as e:
            print(e)

    elif ans[0:4] == "quit":
        global run_game
        run_game = False

    elif ans[0:3] == "del":
        row = int(ans[5])
        col = int(ans[8])
        board[row][col] = "*"
        print("STATUS: Board updated.")
    
    elif ans[0] in nl1:
        n = ans[0]
        row = int(ans[3])
        col = int(ans[6])
        if is_legal_move(board, n, row, col):
            board[row][col] = ans[0]
            print("STATUS: Board updated.")
        else:
            print("STATUS: Illegal input. Try again.")


def is_legal_move(board, n, row, col):
    i = row - row%3 #start indexes of sections
    j = col - col%3

    if n in board[row] or n in [board[i][col] for i in range(len(board))] or n in np.array([board[k][j:j+3] for k in range(i, i+3)]).reshape(-1):
        return False
    return True


def valid_ans(ans, nl1, nl2):
    try:
        return (ans[0] in nl1 and ans[3] in nl2 and ans[6] in nl2) or (ans[0:3] == "del" and ans[5] in nl2 and ans[8] in nl2) or (ans[0:4] in ["save", "quit"])
    except:
        return False


def startup_program():
    print("Do you want to load existing game? (Y/N)  ")
    ans = input("--->  ").upper() #answer

    if ans == "Y":
        print("Enter the name of your file.")
        print("Remember to have the file in same folder and to put .txt at the end")

        while True:
            filename = input("--->  ")
            if filename[-4:] == ".txt":
                break
        
        bd = np.loadtxt(path + filename, dtype="str")
        print("STATUS: Game loaded.")
        if (9, 9) != bd.shape:
            raise "File not compatible"
    else:
        print("STATUS: New game created.")
        bd = np.full((9, 9), "*", dtype="str")
    
    print("INFORMATION: Input <save filename> if you want to save. Input <quit> if you want to quit.")

    return bd


def print_info():
    print("Input format: <n (row, col)>. n must be an integer between 0 and 10 or del if you want to delete that number.")


def print_board(bd): #board
    cdnt = np.arange(0, 9) #coordinate

    for i in range(len(bd)):
        if i == 0:
            print(f"    {0:<2}{1:<2}{2:<4}{3:<2}{4:<2}{5:<4}{6:<2}{7:<2}{8:<4}")
        if i in [0, 3, 6]:
            print(f"  +{("-"*7+"+")*3}")
        print(f"{cdnt[i]:<2}| {bd[i][0]:<2}{bd[i][1]:<2}{bd[i][2]:<2}| {bd[i][3]:<2}{bd[i][4]:<2}{bd[i][5]:<2}| {bd[i][6]:<2}{bd[i][7]:<2}{bd[i][8]:<2}|")
    print(f"  +{("-"*7+"+")*3}")


def is_win(bd): #board
    for i in range(len(bd)):
        if not rowcol_is_unique(bd[i]):
            return False
        elif not rowcol_is_unique([bd[j][i] for j in range(len(bd))]):
            return False
    if not sections_are_unique(bd):
        return False
    return True


def sections_are_unique(bd):
    for i, j in product(range(0,9,3), range(0,9,3)):
        if len(set(np.array([bd[k][j:j+3] for k in range(i, i+3)]).reshape(-1))) != 9:
            return False
    return True


def rowcol_is_unique(rowcol):
    if len(set(rowcol)) == 9 and "*" not in rowcol:
        return True
    return False


main()
