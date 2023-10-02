import random
import copy
import math

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

def print_board(board):
    for row in board:
        print(" ".join(row))
    print()

def check_winner(board):
    # Check rows
    for row in board:
        if all(cell == row[0] and cell != ' ' for cell in row):
            return row[0]

    # Check columns
    for col in range(len(board[0])):
        if all(board[row][col] == board[0][col] and board[row][col] != ' ' for row in range(len(board))):
            return board[0][col]

    # Check diagonals
    if all(board[i][i] == board[0][0] and board[i][i] != ' ' for i in range(len(board))) or \
       all(board[i][len(board)-1-i] == board[0][len(board)-1] and board[i][len(board)-1-i] != ' ' for i in range(len(board))):
        return board[0][0]

    return None


def is_board_full(board):
    return all(board[i][j] != ' ' for i in range(len(board)) for j in range(len(board[0])))

def get_empty_cells(board):
    return [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == ' ']

def make_move(board, move, player):
    board[move[0]][move[1]] = player

def available_moves(board):
    return [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == ' ']

def ucb_score(node):
    if node.visits == 0:
        return float('inf')
    return node.wins / node.visits + 1.4 * (2 * math.log(node.parent.visits) / node.visits) ** 0.5

def select_best_child(node):
    if not node.children:
        return node

    return max(node.children, key=ucb_score)


def expand(state, player):
    possible_moves = [(i, j) for i in range(3) for j in range(3) if state[i][j] == '']
    if not possible_moves:
        # 没有有效移动时，仍然返回一个新的节点表示当前状态
        new_child = Node(state, parent=None)  # 这里的 parent 可以根据你的逻辑调整
        return new_child

    move = find_best_move(Node(state=state), player, simulations=1)
    new_state = [row[:] for row in state]
    new_state[move[0]][move[1]] = player  # 使用正确的玩家信息
    new_child = Node(new_state, parent=None)  # 这里的 parent 可以根据你的逻辑调整
    return new_child




def backpropagate(node, result, player):
    while node:
        node.visits += 1
        if result == 'Tie':
            node.wins += 0.5
        elif result == player:
            node.wins += 1

        node = node.parent



def player_switch(current_state=None):
    count_x = sum(row.count('X') for row in current_state)
    count_o = sum(row.count('O') for row in current_state)
    if count_x > count_o:
        return 'O'
    else:
        return 'X'

def find_best_move(board, player, simulations=10):
    root = Node(state=board)
    for _ in range(simulations):
        node = root
        while node.children:
            node = select_best_child(node)

        expanded_node = expand(node.state, player)
        if expanded_node:
            result = simulate(expanded_node, player)
            if result is not None:
                backpropagate(expanded_node, result, player)

    if not root.children:
        # 如果没有子节点，返回一个默认的移动（这里假设棋盘是3x3）
        return 1, 1  # 或者选择其他默认的移动
    else:
        best_child = max(root.children, key=lambda x: x.visits)
        if best_child:
            return find_move(root, best_child)
        else:
            return 1, 1  # 处理找不到最佳子节点的情况




def simulate(node, player, max_depth=10):
    current_state = node.state
    current_player = player
    depth = 0

    while not check_winner(current_state) and not is_board_full(current_state) and depth < max_depth:
        # Instead of random choice, use your find_best_move function
        move = find_best_move(current_state, current_player, simulations=1)
        make_move(current_state, move, current_player)
        current_player = player_switch(current_state)
        depth += 1

    winner = check_winner(current_state)
    print("获胜者：", winner)
    return winner if winner else None







def find_move(root, child):
    if child:
        for i in range(len(root.state)):
            for j in range(len(root.state[0])):
                if root.state[i][j] != child.state[i][j]:
                    return i, j
    return 1, 1  # 处理找不到最佳子节点的情况

if __name__ == "__main__":
    board_size = 3
    board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
    player = 'X'  # 初始化玩家

    while not check_winner(board) and not is_board_full(board):
        if player_switch(board) == 'X':
            row, col = map(int, input("Enter your move (row col): ").split())
            print("row:", row, "col:", col)  # 在这里打印
            if board[row][col] == ' ':
                make_move(board, (row, col), 'X')
            else:
                print("Invalid move. Try again.")
                continue
        else:
            print("Computer is thinking...")
            row, col = find_best_move(board, player, simulations=10)  # 传递玩家信息
            make_move(board, (row, col), 'O')

            # 在这里打印
            print("row:", row, "col:", col)

    winner = check_winner(board)
    if winner:
        print(f"{winner} wins!")
    else:
        print("It's a tie!")

