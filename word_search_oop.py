# Author: Michael Aheebwa

import random
import time
import os
from string import ascii_uppercase as uc
from PIL import Image, ImageDraw, ImageFont


class WordSearchGrid:
    def __init__(self, n_words, grid_size=15, words_file='words.txt', cheat=False):
        self.num_words = n_words
        self.grid_size = grid_size
        self.words_file = words_file
        self.cheat = cheat

        self.dir_map = {
            'lr': (1, 0), 'rl': (-1, 0), 'tb': (0, 1), 'bt': (0, -1),
            'tr': (1, 1), 'tl': (-1, 1), 'br': (1, -1), 'bl': (-1, -1)
        }

        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.words = []
        self.placed_words = []

    @staticmethod
    def _log(message):
        with open('log.txt', 'a') as f:
            f.write(f"{message}\n")

    def get_words_from_file(self):
        if not os.path.exists(self.words_file):
            return ["PYTHON", "CODE", "SEARCH", "GRID", "PILLOW", "IMAGE"]

        with open(self.words_file, 'r') as wf:
            all_words = [w.strip().upper() for w in wf.read().splitlines() if w.strip()]

        random.shuffle(all_words)
        words = sorted(all_words[:self.num_words], key=len, reverse=True)
        return words

    def _get_coordinates(self, word, start_pos, direction):
        dx, dy = self.dir_map[direction]
        x, y = start_pos
        coords = []

        for i in range(len(word)):
            new_x, new_y = x + (i * dx), y + (i * dy)
            if not (0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size):
                return None
            coords.append((new_x, new_y))
        return coords

    def generate(self):

        self.words = self.get_words_from_file()

        for word in self.words:
            placed = False
            attempts = 0
            max_attempts = 200

            while not placed and attempts < max_attempts:
                attempts += 1
                start_x = random.randint(0, self.grid_size - 1)
                start_y = random.randint(0, self.grid_size - 1)

                dirs = list(self.dir_map.keys())
                random.shuffle(dirs)

                for d in dirs:
                    coords = self._get_coordinates(word, (start_x, start_y), d)
                    if coords and self._can_place(word, coords):
                        self._place_word(word, coords)
                        self.placed_words.append(word)
                        placed = True
                        break

        self._fill_random_letters()

    def _can_place(self, word, coords):
        for i, (x, y) in enumerate(coords):
            current_char = self.grid[y][x]
            if current_char is not None and current_char != word[i]:
                return False
        return True

    def _place_word(self, word, coords):
        char_case = str.lower if self.cheat else str.upper
        for i, (x, y) in enumerate(coords):
            self.grid[y][x] = char_case(word[i])

    def _fill_random_letters(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x] is None:
                    self.grid[y][x] = random.choice(uc)

    def save_as_png(self, filename="word_search.png"):
        """Creates a PNG image with a properly wrapped word list at the bottom."""
        cell_size = 40
        margin = 50
        grid_pixel_size = self.grid_size * cell_size

        # Calculate how much extra space we need for the word list
        # We'll allow 3 words per line
        words_per_row = 3
        num_rows_words = (len(self.placed_words) // words_per_row) + 1
        word_list_height = num_rows_words * 30 + 40  # 30px per line + padding

        # Total image height = Grid + Margins + Word List Space
        img_width = grid_pixel_size + (margin * 2)
        img_height = grid_pixel_size + (margin * 2) + word_list_height

        img = Image.new('RGB', (img_width, img_height), color='white')
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 24)
            list_font = ImageFont.truetype("arial.ttf", 18)
        except:
            font = ImageFont.load_default()
            list_font = ImageFont.load_default()

        # 1. Draw the grid letters
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                char = self.grid[y][x]
                # Center the letter slightly within its 40x40 cell
                pos_x = margin + (x * cell_size) + 10
                pos_y = margin + (y * cell_size)
                draw.text((pos_x, pos_y), char, fill="black", font=font)

        # 2. Draw a separator line between grid and word list
        separator_y = grid_pixel_size + margin + 10
        draw.line([(margin, separator_y), (img_width - margin, separator_y)], fill="gray", width=2)

        # 3. Draw the word list in columns
        draw.text((margin, separator_y + 10), "FIND THESE WORDS:", fill="black", font=list_font)

        start_y = separator_y + 40
        col_width = (img_width - (margin * 2)) // words_per_row

        for i, word in enumerate(self.placed_words):
            row = i // words_per_row
            col = i % words_per_row

            w_x = margin + (col * col_width)
            w_y = start_y + (row * 25)  # 25px vertical spacing between word rows

            draw.text((w_x, w_y), f"• {word}", fill="blue", font=list_font)

        img.save(filename)
        print(f"Game saved successfully as {filename}")

    def show_grid(self):
        if not self.placed_words:
            self.generate()

        # Display in console
        for row in self.grid:
            print("\t".join(row))

        # Save to file
        self.save_as_png()


if __name__ == '__main__':
    word_search = WordSearchGrid(n_words=10, grid_size=15)
    word_search.show_grid()