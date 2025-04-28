import tkinter as tk
import random
import time
import pygame

pygame.mixer.init()

try:
    click_sound = pygame.mixer.Sound("click.wav")
    explosion_sound = pygame.mixer.Sound("explosion.wav")
    win_sound = pygame.mixer.Sound("win.wav")
except FileNotFoundError:
    class SilentSound:
        def play(self):
            pass
    click_sound = explosion_sound = win_sound = SilentSound()

class Cell(tk.Button):
    def __init__(self, master, x, y, game):
        super().__init__(
            master,
            width=2,
            height=1,
            font=('Arial', 12, 'bold'),
            relief='raised',
            bg='lightgreen',
            disabledforeground='black'
        )
        self.x, self.y = x, y
        self.game = game
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.bind('<Button-1>', self.left_click)
        self.bind('<Button-3>', self.right_click)

    def left_click(self, event):
        if self.game.over:
            return
        if not self.game.started:
            self.game.place_mines_safe(self.x, self.y)
            self.game.start_timer()
            self.game.started = True
        if not self.is_flagged:
            self.reveal()
            if self.is_mine:
                self.config(text='💣', bg='red')
                explosion_sound.play()
                self.game.game_over()
            elif self.game.check_win():
                self.game.win()

    def right_click(self, event):
        if self.game.over:
            return
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
            self.config(text='🚩' if self.is_flagged else '')

    def reveal(self):
        if self.is_revealed or self.is_flagged or self.game.over:
            return
        self.is_revealed = True
        click_sound.play()

        count = self.game.count_mines_around(self.x, self.y)
        self.config(relief='sunken', bg='white')

        if self.is_mine:
            return

        if count > 0:
            colors = {
                1: 'blue',
                2: 'green',
                3: 'red',
                4: 'darkblue',
                5: 'darkred',
                6: 'teal',
                7: 'black',
                8: 'gray'
            }
            self.config(text=str(count), disabledforeground=colors.get(count, 'black'))
        else:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx or dy:
                        nx, ny = self.x + dx, self.y + dy
                        if 0 <= nx < self.game.size and 0 <= ny < self.game.size:
                            self.game.cells[nx][ny].reveal()

        self.config(state='disabled')


class Minesweeper:
    def __init__(self, master, size=8, mines=10):
        self.master = master
        self.size = size
        self.mines = mines
        self.started = False
        self.over = False
        self.cells = [[None for _ in range(size)] for _ in range(size)]

        self.top_frame = tk.Frame(master)
        self.top_frame.pack(pady=5)

        self.reset_btn = tk.Button(self.top_frame, text='😃 Reset', font=('Arial', 12), command=self.reset_game)
        self.reset_btn.pack(side='left', padx=5)

        self.timer_label = tk.Label(self.top_frame, text='Time: 0', font=('Arial', 12))
        self.timer_label.pack(side='right', padx=5)
        self.start_time = None
        self.timer_running = False

        self.frame = tk.Frame(master)
        self.frame.pack()

        for x in range(size):
            for y in range(size):
                self.cells[x][y] = Cell(self.frame, x, y, self)
                self.cells[x][y].grid(row=x, column=y)

    def place_mines_safe(self, safe_x, safe_y):
        safe_zone = {(safe_x + dx, safe_y + dy)
                     for dx in [-1, 0, 1]
                     for dy in [-1, 0, 1]
                     if 0 <= safe_x + dx < self.size and 0 <= safe_y + dy < self.size}

        available = [(x, y) for x in range(self.size) for y in range(self.size)
                     if (x, y) not in safe_zone]
        mine_positions = random.sample(available, self.mines)

        for x, y in mine_positions:
            self.cells[x][y].is_mine = True

    def count_mines_around(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx or dy:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        if self.cells[nx][ny].is_mine:
                            count += 1
        return count

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f'Time: {elapsed}')
            self.master.after(1000, self.update_timer)

    def reset_game(self):
        self.frame.destroy()
        self.top_frame.destroy()
        self.__init__(self.master, size=self.size, mines=self.mines)

    def game_over(self):
        self.timer_running = False
        self.over = True
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.config(text='💣', bg='gray')
                cell.config(state='disabled')
        self.reset_btn.config(text='💀 Game Over')

    def check_win(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def win(self):
        self.timer_running = False
        self.over = True
        for row in self.cells:
            for cell in row:
                cell.config(state='disabled')
        self.reset_btn.config(text='😎 You Win!')
        win_sound.play()


class StartScreen:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(pady=50)

        tk.Label(self.frame, text="Minesweeper", font=('Arial', 24, 'bold')).pack(pady=10)

        tk.Button(self.frame, text="Small (8x8)", font=('Arial', 14),
                  command=lambda: self.start_game(8, 10)).pack(pady=5)
        tk.Button(self.frame, text="Medium (14x14)", font=('Arial', 14),
                  command=lambda: self.start_game(14, 40)).pack(pady=5)
        tk.Button(self.frame, text="Large (20x20)", font=('Arial', 14),
                  command=lambda: self.start_game(20, 99)).pack(pady=5)

    def start_game(self, size, mines):
        self.frame.destroy()
        Minesweeper(self.master, size=size, mines=mines)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Minesweeper")
    StartScreen(root)
    root.mainloop()
