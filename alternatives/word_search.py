from string import ascii_uppercase as uc
import random, time

log_file = open('../log.txt', 'w')
log_file.write(time.asctime().upper().center(100) + '\n')


GRID_SIZE = 15         # number of letters on each edge
num_words = 20         # number of words to play with
grid = [
    [random.choice(uc) for _ in range(GRID_SIZE)]
    for _ in range(GRID_SIZE)
]
directions = ['lr', 'rl', 'tb', 'bt', 'tr', 'tl', 'br', 'bl']


# read the words file
with open('words', 'r') as wf:
    all_words = wf.read().split('\n')
    random.shuffle(all_words)
    words = all_words[:num_words]
    # starting with longer words reduces the chances of getting stuck while searching for a
    # suitable position in the grid to the word (hope so)
    words.sort(key=lambda wrd: len(wrd), reverse=True)
    log_file.write(f'Words to add: {words}\n\n')

# function to add single word to the grid
def add_word_to_grid(word: str, occupied_coordinates):
    log_file.write(f'Attempting to add "{word}" to the grid\n')
    direction = random.choice(directions)

    log_file.write(f'The word {word} will be added running in direction: {direction.upper()}\n')
    # search for viable position till found.
    is_pos_found = False
    max_search_iter = 150
    search_iter = 0

    log_file.write(f'Searching for a suitable position (coordinate) for "{word}" in the grid...\n')
    while not is_pos_found:
        all_word_coord = None

        match direction:
            case 'lr':
                max_x = GRID_SIZE - len(word)
                x = random.randint(0, max_x)
                y = random.randint(0, GRID_SIZE - 1)
                all_word_coord = [(x+i, y) for i in range(len(word))]

            case 'rl':
                min_x = len(word)
                x = random.randint(min_x, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                all_word_coord = [(x-i, y) for i in range(len(word))]

            case 'tb':
                max_y = GRID_SIZE - len(word)
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, max_y)
                all_word_coord = [(x, y+i) for i in range(len(word))]

            case 'bt':
                min_y = len(word)
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(min_y, GRID_SIZE - 1)
                all_word_coord = [(x, y-i) for i in range(len(word))]

            case 'tr':
                max_x = max_y = GRID_SIZE - len(word)
                x = random.randint(0, max_x)
                y = random.randint(0, max_y)
                all_word_coord = [(x+i, y+i) for i in range(len(word))]

            case 'tl':
                min_x = len(word)
                max_y = GRID_SIZE - len(word)

                x = random.randint(min_x, GRID_SIZE - 1)
                y = random.randint(0, max_y)
                all_word_coord = [(x-i, y+i) for i in range(len(word))]

            case 'br':
                max_x = GRID_SIZE - len(word)
                min_y = len(word)
                x = random.randint(0, max_x)
                y = random.randint(min_y, GRID_SIZE - 1)
                all_word_coord = [(x + i, y - i) for i in range(len(word))]

            case 'bl':
                min_x = min_y = len(word)
                x = random.randint(min_x, GRID_SIZE - 1)
                y = random.randint(min_y, GRID_SIZE - 1)
                all_word_coord = [(x - i, y - i) for i in range(len(word))]

        continue_looking = True
        log_file.write(f'\tCoordinates Chosen: {all_word_coord}\n')
        log_file.write(f'\tTesting if chosen coordinates do not coincide with other words\n')

        for i, coord in enumerate(all_word_coord):
            for j, w in enumerate(occupied_coordinates):
                compare_word = words[j]                             # we won't shuffle the order of words, so this is guaranteed
                if coord in w:
                    coinciding_letter = compare_word[w.index(coord)]
                    if coinciding_letter != word[i]:
                        continue_looking = False
                        break

            if not continue_looking:
                break

        # if continue_looking is true after the loop, then all coordinates for the word
        # are ok, i.e. do not coincide with any of the words we have
        if continue_looking:
            occupied_coordinates.append(all_word_coord)
            log_file.write(f'--> Successfully found a place to put the word {word} in the grid!\n\n')
            is_pos_found = True

        search_iter += 1

        if search_iter >= max_search_iter:
            log_file.write(f'--> Failed to find suitable position for the word {word}\n')
            log_file.write(f'Search iterations exceeded {max_search_iter}\n\n')
            words.remove(word)
            break

    return occupied_coordinates


# add the words to the grid to populate the occupied_coordinates list
occupied  = []
for w in words:
    occupied = add_word_to_grid(w, occupied)


# using the occupied_coordinates, we now add the words to our grid
for i, occupied_coords in enumerate(occupied):
    for j, coord in enumerate(occupied_coords):
        c, r = coord
        grid[r][c] = words[i][j].upper()       # .lower() for dev cheat!


random.shuffle(words)  # not execution-useful, just to remove the sorting when showing these words to user ;-)
print(f'FIND THESE WORDS: (Reshuffled every run) \n{', '.join(words)}')
print()
for row in grid:
    line = '\t'.join(row)
    print(line)


# close log file
log_file.close()
