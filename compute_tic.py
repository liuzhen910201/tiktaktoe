import tkinter as tk
import random

def new_game():
    global player
    player = random.choice(players)
    label.config(text= player + '的回合')
    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text='', bg='#F0F0F0')

def restart_game():
    new_game()

def quit_game():
    window.destroy()

def computer_turn():
    if check_winner() is False and empty_space():
        while True:
            row = random.randint(0, 2)
            column = random.randint(0, 2)
            if buttons[row][column]['text'] == '':
                buttons[row][column]['text'] = player
                break
        if check_winner() is False:
            player_switch()
            label.config(text=(player + '的回合'))
            check_winner()  # 在每一步之后检查胜负

def player_turn(row, column):
    global player
    if buttons[row][column]['text'] == '' and check_winner() is False:
        buttons[row][column]['text'] = player
        if check_winner() is False:
            player_switch()
            label.config(text=(player + '的回合'))
            check_winner()  # 在每一步之后检查胜负

def player_switch():
    global player
    if player == players[0]:
        player = players[1]
    else:
        player = players[0]

def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != '':
            buttons[row][0].config(bg='green')
            buttons[row][1].config(bg='green')
            buttons[row][2].config(bg='green')
            label.config(text=(buttons[row][0]['text'] + '获胜'))
            return True
    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != '':
            buttons[0][column].config(bg='green')
            buttons[1][column].config(bg='green')
            buttons[2][column].config(bg='green')
            label.config(text=(buttons[0][column]['text'] + '获胜'))
            return True
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != '':
        buttons[0][0].config(bg='green')
        buttons[1][1].config(bg='green')
        buttons[2][2].config(bg='green')
        label.config(text=(buttons[0][0]['text'] + '获胜'))
        return True
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != '':
        buttons[0][2].config(bg='green')
        buttons[1][1].config(bg='green')
        buttons[2][0].config(bg='green')
        label.config(text=(buttons[0][2]['text'] + '获胜'))
        return True

    if empty_space() is False:
        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg='yellow')
        label.config(text=('平局'))
        return 'Tie'
    else:
        return False

def empty_space():
    space = 9
    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] != '':
                space -= 1

    if space == 0:
        return False
    else:
        return True

if __name__ == '__main__':
    window = tk.Tk()
    window.title("井字棋游戏")

    players = ['X', 'O']
    player = random.choice(players)
    buttons = [[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]]
    label = tk.Label(window, text="{}的回合".format(player), font=('consolas', 40))
    label.pack()

    frame = tk.Frame()
    frame.pack()

    for row in range(3):
        for column in range(3):
            buttons[row][column] = tk.Button(frame, text='',
                                             font=('consolas', 40),
                                             command=lambda row=row, column=column: player_turn(row, column),
                                             width=5, height=2)
            buttons[row][column].grid(row=row, column=column, padx=5, pady=5)

    restart_button = tk.Button(window, text="重新开始", command=restart_game)
    restart_button.pack(side=tk.LEFT, padx=10, pady=10)

    quit_button = tk.Button(window, text="退出游戏", command=quit_game)
    quit_button.pack(side=tk.LEFT, padx=10, pady=10)

    computer_turn_button = tk.Button(window, text="电脑对局", command=computer_turn)
    computer_turn_button.pack(side=tk.LEFT, padx=10, pady=10)

    window.mainloop()
