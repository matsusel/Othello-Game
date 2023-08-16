import copy


class Othello:
    def __init__(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.board[3][3] = self.board[4][4] = 1
        self.board[3][4] = self.board[4][3] = -1
        self.turn = 1

    def get_valid_moves(self):
        valid_moves = []
        for j in range(8):
            for i in range(8):
                if self.board[j][i] == 0:
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == dj == 0:
                                continue
                            x, y = j + di, i + dj
                            flip = False
                            while 0 <= x < 8 and 0 <= y < 8:
                                if self.board[x][y] == 0:
                                    break
                                if self.board[x][y] == self.turn:
                                    if flip:
                                        valid_moves.append((j, i))
                                    break
                                x += di
                                y += dj
                                flip = True
        return valid_moves

    def make_move(self, xmove, ymove):
        i = xmove
        j = ymove
        self.board[i][j] = self.turn
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == dj == 0:
                    continue
                x, y = i + di, j + dj
                flip = False
                while 0 <= x < 8 and 0 <= y < 8:
                    if self.board[x][y] == 0:
                        break
                    if self.board[x][y] == self.turn:
                        if flip:
                            while (x, y) != (i, j):
                                x -= di
                                y -= dj
                                self.board[x][y] = self.turn
                        break
                    x += di
                    y += dj
                    flip = True
        self.turn = -self.turn

    def heuristic_count_stones(self):
        return sum([elem for row in self.board for elem in row]) * self.turn

    def heuristic_count_border(self):
        suma = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if i == 0 or i == 7 or j == 0 or j == 7:
                    suma += self.board[i][j]
        return suma * self.turn

    def heuristic_count_valid_moves(self):
        return len(self.get_valid_moves())



    def get_winner(self):
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(-1) for row in self.board)
        if black_count > white_count:
            return "Black wins!"
        elif black_count < white_count:
            return "White wins!"
        else:
            return "Tie!"

    def is_game_over(self):
        return not self.get_valid_moves()

    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.is_game_over():
            # self.heuristic_count_stones()
            # self.heuristic_count_border()
            # self.heuristic_count_valid_moves()
            if self.turn == 1:
                return   self.heuristic_count_valid_moves()
            else:
                return self.heuristic_count_valid_moves()

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_valid_moves():
                x,y = move
                self.make_move(y,x)
                eval = self.minimax(depth - 1, False)
                self.undo_move(y,x)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_valid_moves():
                self.make_move(*move)
                eval = self.minimax(depth - 1, True)
                self.undo_move(*move)
                min_eval = min(min_eval, eval)
            return min_eval

    def minimax_alphabeta(self, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or self.is_game_over():
            return self.heuristic_count_valid_moves()

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_valid_moves():
                x, y = move
                self.make_move(y, x)
                eval = self.minimax_alphabeta(depth - 1, False, alpha, beta)
                self.undo_move(y, x)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_valid_moves():
                x, y = move
                self.make_move(y, x)
                eval = self.minimax_alphabeta(depth - 1, True, alpha, beta)
                self.undo_move(y, x)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def make_best_move(self):
        boardtmp = copy.deepcopy(self.board)
        best_eval = float('-inf')
        best_move = None
        for move in self.get_valid_moves():
            self.make_move(*move)
            eval = self.minimax(5, False)
            self.undo_move(*move)
            if eval > best_eval:
                best_eval = eval
                best_move = move
        self.board = copy.deepcopy(boardtmp)

        if best_move is not None:
            self.make_move(*best_move)

    def make_best_move_alphabeta(self):
        boardtmp = copy.deepcopy(self.board)
        best_eval = float('-inf')
        best_move = None
        for move in self.get_valid_moves():
            self.make_move(*move)
            eval = self.minimax_alphabeta(5, False)
            self.undo_move(*move)
            if eval > best_eval:
                best_eval = eval
                best_move = move
        self.board = copy.deepcopy(boardtmp)

        if best_move is not None:
            self.make_move(*best_move)

    def undo_move(self, xmove, ymove):
        i = xmove
        j = ymove
        self.board[i][j] = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == dj == 0:
                    continue
                x, y = i + di, j + dj
                flip = False
                while 0 <= x < 8 and 0 <= y < 8:
                    if self.board[x][y] == 0:
                        break
                    if self.board[x][y] == self.turn:
                        if flip:
                            while (x, y) != (i, j):
                                x -= di
                                y -= dj
                                self.board[x][y] = self.turn
                        break
                    x += di
                    y += dj
                    flip = True
        self.turn = -self.turn
