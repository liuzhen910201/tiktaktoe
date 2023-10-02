import random
import copy
import time

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(map(lambda x: str(x) if x != ' ' else ' ', row)) + ' |')


    @staticmethod
    def print_board_nums():
        number_board = [[str(i+1) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        # Check diagonal
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False


class HumanPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.symbol + '\'s turn. Input move (1-9): ')
            try:
                val = int(square) - 1
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val


class RandomPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, game):
        return random.choice(game.available_moves())


class MonteCarloPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            return random.choice(game.available_moves())

        # 调整检索次数
        simulations = 200
        square = self.monte_carlo_tree_search(game, simulations)
        return square

    def monte_carlo_tree_search(self, game, simulations=50):
        scores = {move: 0 for move in game.available_moves()}

        for _ in range(simulations):
            for move in scores:
                copy_game = copy.deepcopy(game)
                copy_game.make_move(move, self.symbol)
                winner = play(copy_game, RandomPlayer('O'), RandomPlayer('X'), print_game=False)
                if winner == self.symbol:
                    scores[move] += 1

        best_move = max(scores, key=scores.get)
        return best_move


def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square+1}')
                game.print_board()
                print('')  # empty line

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter  # ends the loop and exits the game
            letter = 'O' if letter == 'X' else 'X'  # switch player

        # Tiny break to make it easier to read
        if print_game:
            time.sleep(0.8)

    if print_game:
        print('It\'s a tie!')


if __name__ == '__main__':
    x_player = HumanPlayer('X')
    o_player = MonteCarloPlayer('O')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)
