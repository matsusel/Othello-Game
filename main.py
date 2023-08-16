import datetime

from reversi import *

def minimax(game, node, depth, maximizing_player):
    if depth == 0 or node.is_terminal():
        return game.heuristic_count_border() + game.heuristic_count_stones + game.heuristic_count_border

    if maximizing_player:
        best_value = float('-inf')
        for child in node.generate_children():
            value = minimax(game, game.board, depth - 1, False)
            best_value = max(best_value, value)
        return best_value
    else:
        best_value = float('inf')
        for child in node.generate_children():
            value = minimax(game, game.board, depth - 1, True)
            best_value = min(best_value, value)
        return best_value

def print_board(board):
    valid_moves = game.get_valid_moves()
    print(valid_moves)
    print("   ", end="")
    for j in range(8):
        print(f"{j} ", end="")
    print()
    for j in range(8):
        print(f"{j} ", end="")
        for i in range(8):
            if (j,i) in valid_moves:
                print("o", end=" ")
            elif board[j][i] == 0:
                print(".", end=" ")
            elif board[j][i] == 1:
                print("B", end=" ")
            else:
                print("W", end=" ")
        print()

game = Othello()
#print_board(game.board)
time_start = datetime.datetime.now()
for i in range(0,100):
    while not game.is_game_over():
        #print(game.heuristic_count_stones())
        #print(game.heuristic_count_valid_moves())
        #print(game.heuristic_count_border())
        valid_moves = game.get_valid_moves()
        depth = 4

        if game.turn == -1:
            #print(f"{valid_moves} (turn: {'W'})")
            #x = int(input("Enter x-coordinate: "))
            #y = int(input("Enter y-coordinate: "))
            #if (x, y) not in valid_moves:
            #    print("Invalid move, try again.")
            #    continue
            #game.make_move(y, x)
            #print(f"(turn: {'W'})")
            game.make_best_move()
            #print_board(game.board)
        else:
            #print(f" (turn: {'B'})")
            game.make_best_move()
            #print_board(game.board)
            #print(f"{valid_moves} (turn: {'B'})")
#perf_counter
time_end = datetime.datetime.now()
print(game.get_winner())
print((time_end-time_start)/100)
#print_board(game.board)
if __name__ == '__main__':
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
