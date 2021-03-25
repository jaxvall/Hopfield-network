from tkinter import *
from itertools import product
import numpy as np
import math


class Paint(object):

    def __init__(self):
        self.root = Tk()
        self.cell_size = 20
        self.canvas_size = 32
        self.pat_len = self.canvas_size * self.canvas_size

        self.weights = np.zeros(
            (self.pat_len,  self.pat_len))
        self.pattern = np.ones((self.pat_len,)) * -1

        self.rect_ids = np.zeros((self.canvas_size, self.canvas_size))

        self.store_btn = Button(self.root, text='Store', command=self.store)
        self.store_btn.grid(row=0, column=0)

        self.recall_btn = Button(
            self.root, text='Recall', command=self.async_recall)
        self.recall_btn.grid(row=0, column=1)

        self.clear_btn = Button(
            self.root, text='Clear', command=self.clear)
        self.clear_btn.grid(row=0, column=2)

        self.loading_lbl = Label(
            self.root, text='', width=9)
        self.loading_lbl.grid(row=0, column=3)

        self.clear_w_btn = Button(
            self.root, text='Clear weights', command=self.clear_weights)
        self.clear_w_btn.grid(row=0, column=4)

        self.close_btn = Button(
            self.root, text='Close', command=self.quit)
        self.close_btn.grid(row=0, column=5)

        self.canvas = Canvas(self.root, width=650, height=650)
        self.canvas.grid(row=1, columnspan=6)
        self.canvas.bind('<B1-Motion>', self.fill_square)
        for (i, j) in product(range(self.canvas_size), range(self.canvas_size)):
            x1 = (i * self.cell_size)
            y1 = (j * self.cell_size)
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            rect = self.canvas.create_rectangle(
                x1, y1, x2, y2, fill='white', outline="bisque4")
            self.rect_ids[i][j] = rect

        self.root.mainloop()

    def fill_square(self, event):
        i = int(event.x / self.cell_size)
        j = int(event.y / self.cell_size)
        valid_idx = range(self.canvas_size)

        if set([i, j]).issubset(valid_idx):
            self.pattern[j * self.canvas_size + i] = 1
            self.canvas.itemconfig(int(self.rect_ids[i][j]), fill='black')

        return

    def store(self):
        new_weights = np.zeros((self.pat_len, self.pat_len))
        for i in range(self.pat_len):
            for j in range(self.pat_len):
                new_weights[i][j] = self.pattern[i] * self.pattern[j]

        self.loading_lbl.config(text='Stored!')
        self.canvas.update()

        self.weights += new_weights
        self.clear()
        return

    def sign(self, v):
        if v > 0:
            return 1
        else:
            return -1

    def fill_from_recall(self, value, index):
        i = index % self.canvas_size
        j = math.floor(index / self.canvas_size)

        color = 'black'
        if value == -1:
            color = 'white'

        self.canvas.itemconfig(int(self.rect_ids[i][j]), fill=color)

        return

    def async_recall(self):
        new_pattern = self.pattern.copy()
        conv = False
        ep = 0
        max_ep = 100
        while not conv or ep > max_ep:
            old_pattern = new_pattern.copy()
            rand_list = np.random.choice(
                self.pat_len, self.pat_len, replace=False)
            for i in rand_list:
                val = self.sign(new_pattern @ self.weights[i].T)
                new_pattern[i] = val
                self.fill_from_recall(val, i)
                self.canvas.update()

            if np.array_equal(new_pattern, old_pattern):
                conv = True
                self.loading_lbl.config(text='Recall done!')
                self.canvas.update()
            ep += 1

        return

    def clear_weights(self):
        self.weights = np.zeros(
            (self.pat_len, self.pat_len))

    def clear(self):
        for (i, j) in product(range(self.canvas_size), range(self.canvas_size)):
            self.canvas.itemconfig(int(self.rect_ids[i][j]), fill='white')

        self.pattern = np.ones((self.pat_len,)) * -1
        self.loading_lbl.config(text='')
        return

    def quit(self):
        self.root.destroy()


if __name__ == '__main__':
    Paint()
