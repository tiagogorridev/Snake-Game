import tkinter as tk
import random

WIDTH = 700
HEIGHT = 700
VEL = 60
SIZE = 40
SNAKE_COL = '#993399'
FOOD_COL = '#ffff00'
BG = '#000333'

class Snake:
    def __init__(self):
        self.body = [[0, 0]]
        self.squares = []
        self.create_snake()
    def create_snake(self):
        for x, y in self.body:
            square = canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill=SNAKE_COL)
            self.squares.append(square)
            
class Food:
    def __init__(self):
        self.coordinates = [random.randint(0, (WIDTH // SIZE) - 1) * SIZE,
                            random.randint(0, (HEIGHT // SIZE) - 1) * SIZE]
        canvas.create_oval(self.coordinates[0], self.coordinates[1],
                           self.coordinates[0] + SIZE, self.coordinates[1] + SIZE, fill=FOOD_COL, tag='food')
def next_round():
    global game_running
    if game_running:
        x, y = snake.body[0]
        if direction == 'up':
            y -= SIZE
        elif direction == 'down':
            y += SIZE
        elif direction == 'left':
            x -= SIZE
        elif direction == 'right':
            x += SIZE
        snake.body.insert(0, [x, y])
        new_square = canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill=SNAKE_COL)
        snake.squares.insert(0, new_square)

        if x == food.coordinates[0] and y == food.coordinates[1]:
            global points
            points += 1
            label.config(text=f'SCORE: {points}')
            canvas.delete('food')
            food.__init__()
        else:
            del snake.body[-1]
            canvas.delete(snake.squares[-1])
            del snake.squares[-1]
        if collision():
            game_over()
        else:
            window.after(VEL, next_round)
def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction
def collision():
    x, y = snake.body[0]
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True
    if [x, y] in snake.body[1:]:
        return True
    return False
def game_over():
    global game_running
    game_running = False
    canvas.delete('all')
    canvas.create_text(WIDTH / 2, HEIGHT / 2, font=('consolas', 70), text='GAME OVER', fill='red')
    canvas.create_text(WIDTH / 2, HEIGHT / 2 + 100, font=('consolas', 30), text='Pressione ENTER', fill='white')
    window.bind('<Return>', restart_game)
def restart_game(event):
    global game_running, points, direction
    if not game_running:
        game_running = True
        points = 0
        direction = 'down'
        label.config(text=f'SCORE: {points}')
        canvas.delete('all')
        snake.__init__()
        food.__init__()
        next_round()
window = tk.Tk()
window.title('Snake Game')
window.resizable(False, False)
points = 0
direction = 'down'
game_running = True
label = tk.Label(window, text=f'SCORE: {points}', font=('consolas', 40))
label.pack()

canvas = tk.Canvas(window, bg=BG, height=HEIGHT, width=WIDTH)
canvas.pack()
window.update()
window.geometry(f'{window.winfo_width()}x{window.winfo_height()}+{int((window.winfo_screenwidth() - window.winfo_width()) / 2)}+{int((window.winfo_screenheight() - window.winfo_height()) / 2)}')

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Return>', restart_game)
snake = Snake()
food = Food()
next_round()
window.mainloop()