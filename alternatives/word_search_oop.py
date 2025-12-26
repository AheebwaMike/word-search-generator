# Author: Michael Aheebwa

from string import ascii_uppercase as uc
import random, time

class WordSearchGrid:
    def __init__(self, n_words, grid_size=15, words_file='words.txt', cheat=False):
        self.log_file = open('../log.txt', 'w')
        self.log_file.write(time.asctime().upper().center(100) + '\n')

        self.num_words = n_words
        self.words_file = words_file
        self.words = self.get_words_from_file()

        self.grid_size = grid_size
        self.directions = ['lr', 'rl', 'tb', 'bt', 'tr', 'tl', 'br', 'bl']
        self.grid = [
            [random.choice(uc) for _ in range(self.grid_size)]
            for _ in range(self.grid_size)
        ]

        self.cheat = cheat

    def get_words_from_file(self):
        with open(self.words_file, 'r') as wf:
            all_words = wf.read().split('\n')
            random.shuffle(all_words)
            words = all_words[:self.num_words]
            # starting with longer words reduces the chances of getting stuck while searching for a
            # suitable position in the grid to the word (hope so)
            words.sort(key=lambda wrd: len(wrd), reverse=True)
            self.log_file.write(f'Words to add: {words}\n\n')
            return words

    def add_word_to_grid(self, word: str, occupied_coordinates):
        self.log_file.write(f'Attempting to add "{word}" to the grid\n')
        direction = random.choice(self.directions)

        self.log_file.write(f'The word {word} will be added running in direction: {direction.upper()}\n')
        # search for viable position till found.
        is_pos_found = False
        max_search_iter = 150
        search_iter = 0

        self.log_file.write(f'Searching for a suitable position (coordinate) for "{word}" in the grid...\n')
        while not is_pos_found:
            all_word_coord = None

            match direction:
                case 'lr':
                    max_x = self.grid_size - len(word)
                    x = random.randint(0, max_x)
                    y = random.randint(0, self.grid_size - 1)
                    all_word_coord = [(x + i, y) for i in range(len(word))]

                case 'rl':
                    min_x = len(word)
                    x = random.randint(min_x, self.grid_size - 1)
                    y = random.randint(0, self.grid_size - 1)
                    all_word_coord = [(x - i, y) for i in range(len(word))]

                case 'tb':
                    max_y = self.grid_size - len(word)
                    x = random.randint(0, self.grid_size - 1)
                    y = random.randint(0, max_y)
                    all_word_coord = [(x, y + i) for i in range(len(word))]

                case 'bt':
                    min_y = len(word)
                    x = random.randint(0, self.grid_size - 1)
                    y = random.randint(min_y, self.grid_size - 1)
                    all_word_coord = [(x, y - i) for i in range(len(word))]

                case 'tr':
                    max_x = max_y = self.grid_size - len(word)
                    x = random.randint(0, max_x)
                    y = random.randint(0, max_y)
                    all_word_coord = [(x + i, y + i) for i in range(len(word))]

                case 'tl':
                    min_x = len(word)
                    max_y = self.grid_size - len(word)

                    x = random.randint(min_x, self.grid_size - 1)
                    y = random.randint(0, max_y)
                    all_word_coord = [(x - i, y + i) for i in range(len(word))]

                case 'br':
                    max_x = self.grid_size - len(word)
                    min_y = len(word)
                    x = random.randint(0, max_x)
                    y = random.randint(min_y, self.grid_size - 1)
                    all_word_coord = [(x + i, y - i) for i in range(len(word))]

                case 'bl':
                    min_x = min_y = len(word)
                    x = random.randint(min_x, self.grid_size - 1)
                    y = random.randint(min_y, self.grid_size - 1)
                    all_word_coord = [(x - i, y - i) for i in range(len(word))]

            continue_looking = True
            self.log_file.write(f'\tCoordinates Chosen: {all_word_coord}\n')
            self.log_file.write(f'\tTesting if chosen coordinates do not coincide with other words\n')

            for i, coord in enumerate(all_word_coord):
                for j, w in enumerate(occupied_coordinates):
                    compare_word = self.words[j]  # we won't shuffle the order of words, so this is guaranteed
                    if coord in w:
                        coinciding_letter = compare_word[w.index(coord)]
                        if coinciding_letter != word[i]:
                            continue_looking = False
                            self.log_file.write(f'\t\tCoordinates coincide, searching for other coordinates...\n')
                            break

                if not continue_looking:
                    break

            # if continue_looking is true after the loop, then all coordinates for the word
            # are ok, i.e. do not coincide with any of the words we have
            if continue_looking:
                occupied_coordinates.append(all_word_coord)
                self.log_file.write(f'--> Successfully found a place to put the word {word} in the grid!\n\n')
                is_pos_found = True

            search_iter += 1

            if search_iter >= max_search_iter:
                self.log_file.write(f'--> Failed to find suitable position for the word {word}\n')
                self.log_file.write(f'Search iterations exceeded {max_search_iter}\n\n')
                self.words.remove(word)
                break

        return occupied_coordinates
    
    def add_all_words_to_grid(self):
        # add the words to the grid to populate the occupied_coordinates list
        occupied = []
        for w in self.words:
            occupied = self.add_word_to_grid(w, occupied)

        # using the occupied_coordinates, we now add the words to our grid
        for i, occupied_coords in enumerate(occupied):
            for j, coord in enumerate(occupied_coords):
                c, r = coord
                self.grid[r][c] = self.words[i][j].upper() if not self.cheat \
                                  else self.words[i][j].lower()         # .lower() for dev cheat!

        self.log_file.close()
        return self.grid
    
    def show_grid(self):
        self.add_all_words_to_grid()
        
        random.shuffle(self.words)  # not execution-useful, just to remove the sorting when showing these words to user ;-)
        print(f'FIND THESE WORDS: (Reshuffled every run) \n{', '.join(self.words)}')
        print()
        for row in self.grid:
            line = '\t'.join(row)
            print(line)


if __name__ == '__main__':
    wordGrid = WordSearchGrid(n_words=15)
    wordGrid.show_grid()
