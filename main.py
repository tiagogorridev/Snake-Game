from tkinter import *
import random

WIDTH = 700
HEIGHT = 700
VEL = 60
SIZE = 40
BODY_DIVISION = 3
SNAKE_COL = '#993399'
FOOD_COL = '#ffff00'
BG = '#000333'

class Snake:
    def __init__(self):
        self.body_size = BODY_DIVISION
        self.coordinates = []
        self.squares = []
        for i in range(0, BODY_DIVISION):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SIZE, y + SIZE, fill=SNAKE_COL, tag='snake')
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, int(WIDTH / SIZE) - 1) * SIZE
        y = random.randint(0, int(HEIGHT / SIZE) - 1) * SIZE

        self.coordinates = [x,y]
        canvas.create_oval(x, y, x+SIZE, y+SIZE, fill=FOOD_COL, tag='food')

def next_round(snake, food):
    x, y = snake.coordinates[0]

    if direct == 'up':
        y -= SIZE
    elif direct == 'down':
        y += SIZE
    elif direct == 'left':
        x -= SIZE
    elif direct == 'right':
        x += SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill=SNAKE_COL)
    snake.squares.insert(0,square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global points
        points += 1

        label.config(text='SCORE:{}'.format(points))
        canvas.delete('food')
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if colision(snake):
        game_over()
    else:
        window.after(VEL, next_round, snake, food)

def change_direction(new_direction):
    global direct
    if new_direction == 'left':
        if direct != 'right':
            direct = new_direction
    elif new_direction == 'right':
        if direct != 'left':
            direct = new_direction
    elif new_direction == 'up':
        if direct != 'down':
            direct = new_direction
    elif new_direction == 'down':
        if direct != 'up':
            direct = new_direction

def colision(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= WIDTH:
        return True
    elif y < 0 or y >= WIDTH:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 70), text='GAME OVER', fill='red', tag='gameover')

window = Tk()
window.title('Snake Game')
window.resizable(False, False)
points = 0
direct = 'down'

label = Label(window, text='SCORE:{}'.format(points), font=('consolas',40))
label.pack()

canvas = Canvas(window, bg=BG, height=HEIGHT, width=WIDTH)
canvas.pack()
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f'{window_width}x{window_height}+{x}+{y}')

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_round(snake, food)
window.mainloop()