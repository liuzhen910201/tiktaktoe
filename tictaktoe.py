# Author:Friskwml
# b站: Frisk_wml
# CreateTime: 2023/8/13

from tkinter import *
import random
def new_game():
    global player
    player = random.choice(players)
    label.config(text= player + '的回合')
    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text='', bg='#F0F0F0')
def next_turn(row, column):
    global player
    if buttons[row][column]['text'] == '' and check_winner() is False:
        if player == players[0]:
            buttons[row][column]['text'] = player

            if check_winner() is False:
                player = players[1]
                label.config(text=(players[1] + '的回合'))

            elif check_winner() is True:
                label.config(text=(players[0] + '获胜'))

            elif check_winner() == 'Tie':
                label.config(text=('平局'))

        elif player == players[1]:
            buttons[row][column]['text'] = player

            if check_winner() is False:
                player = players[0]
                label.config(text=(players[0] + '的回合'))

            elif check_winner() is True:
                label.config(text=(players[1] + '获胜'))

            elif check_winner() == 'Tie':
                label.config(text=('平局'))
def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != '':
            buttons[row][0].config(bg='green')
            buttons[row][1].config(bg='green')
            buttons[row][2].config(bg='green')
            return True
    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != '':
            buttons[0][column].config(bg='green')
            buttons[1][column].config(bg='green')
            buttons[2][column].config(bg='green')
            return True
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != '':
        buttons[0][0].config(bg='green')
        buttons[1][1].config(bg='green')
        buttons[2][2].config(bg='green')
        return True
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != '':
        buttons[0][2].config(bg='green')
        buttons[1][1].config(bg='green')
        buttons[2][0].config(bg='green')
        return True

    if empty_space() is False:
        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg='yellow')
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
    window = Tk()
    window.title("井字棋游戏")

    players = ['X', 'O']
    player = random.choice(players)
    buttons = [[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]]
    label = Label(window, text="{}的回合".format(player),
                  font=('consolas', 40))
    label.pack()
    menu = Menu(window)
    window.config(menu=menu)
    game_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label='游戏', menu=game_menu)
    game_menu.add_command(label='新游戏', command=new_game)
    frame = Frame()
    frame.pack()
    for row in range(3):
        for column in range(3):
            buttons[row][column] = Button(frame, text='',
                                          font=('consolas', 40),
                                          command=lambda row=row, column=column:
                                          next_turn(row, column),
                                          width=5, height=2)
            buttons[row][column].grid(row=row, column=column)
    window.mainloop()

