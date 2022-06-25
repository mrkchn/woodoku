import random
import itertools
import numpy as np

from pieces import SHAPE, PIECES, NUM_PIECES, NUM_REGIONS

class Game:
    def __init__(self):
        self.board = np.zeros(SHAPE, dtype=int)
        self.score = 0
        self.pieces = self.get_random_pieces()
        self.game_over = False

    def get_random_pieces(self):
        return random.sample(PIECES, NUM_PIECES)

    def pad_piece(self, piece, point):
        return np.pad(piece,
                      [(point[0], SHAPE[0]-point[0]-piece.shape[0]),
                       (point[1], SHAPE[1]-point[1]-piece.shape[1])],
                      mode="constant")

    def check_game_over(self):
        legal_moves = 0
        for piece in self.pieces:
            legal_moves += len(self.get_legal_points(piece))
        if legal_moves == 0:
            print("Game Over! No legal moves left!")
            print(f"Final Score is: {self.score}")
            self.game_over = True
        return self.game_over

    def get_scoreboard(self, piece, point):
        # add piece to board
        board = self.board + self.pad_piece(piece, point)
        score = self.score + piece.sum()

        # calculate score and reset full rows / cols / regions
        col_sum = np.sum(board, axis=0) >= SHAPE[0]
        score += col_sum.sum() * SHAPE[0]

        row_sum = np.sum(board, axis=1) >= SHAPE[1]
        score += row_sum.sum() * SHAPE[1]

        cleared_regions = []
        for i in range(NUM_REGIONS):
            for j in range(i+1):
                if board[i*NUM_REGIONS:(i+1)*NUM_REGIONS, j*NUM_REGIONS:(j+1)*NUM_REGIONS].sum() >= SHAPE[0]:
                    score += SHAPE[0]
                    cleared_regions.append((i, j))
                    board[i*NUM_REGIONS:(i+1)*NUM_REGIONS, j*NUM_REGIONS:(j+1)*NUM_REGIONS] = 0

        # reset board
        board[:, col_sum] = 0
        board[row_sum, :] = 0

        cleared_rows = []
        cleared_cols = []
        if col_sum.sum() > 0:
            cleared_cols.extend(np.where(col_sum)[0])
        if row_sum.sum() > 0:
            cleared_rows.extend(np.where(row_sum)[0])

        return score, board, cleared_regions, cleared_rows, cleared_cols

    def add_piece(self, piece, point):
        # remove used piece from available pieces
        new_pieces = []
        for p in self.pieces:
            if not np.array_equal(p, piece):
                new_pieces.append(p)
        if not len(new_pieces):
            self.pieces = self.get_random_pieces()
        else:
            self.pieces = new_pieces

        self.score, self.board, cleared_regions, cleared_rows, cleared_cols = self.get_scoreboard(piece, point)
        print(f"Placed\n{piece}\n at {point}")
        if cleared_regions:
            print(f"Cleared Region(s): {cleared_regions}")
        if cleared_rows:
            print(f"Cleared Rows(s): {cleared_rows}")
        if cleared_cols:
            print(f"Cleared Columns(s): {cleared_cols}")
        print(f"Current Score is {self.score}")
        print(f"New Board is:\n{self.board}")
        # if no legal points for all remaining pieces, game is over
        self.check_game_over()

    def is_legal_point(self, piece, point):
        return (point[0] + piece.shape[0]-1 < SHAPE[0]) and (point[1] + piece.shape[1]-1 < SHAPE[1])

    def fits(self, piece, point):
        return self.is_legal_point(piece, point) and np.all(self.board + self.pad_piece(piece, point) < 2)

    def get_legal_points(self, piece):
        return [point for point in list(itertools.product(range(SHAPE[0]), range(SHAPE[1]))) if self.fits(piece, point)]


if __name__ == '__main__':
    game = Game()
    while not game.game_over:
        moves = [(piece, point) for piece in game.pieces for point in game.get_legal_points(piece)]
        scores = []
        boards = []
        for (piece, point) in moves:
            score, board, regions, rows, columns = game.get_scoreboard(piece, point)
            scores.append(score)
            boards.append(board)

        best_piece, best_point = moves[np.argmax(scores)]

        game.add_piece(best_piece, best_point)


