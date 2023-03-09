import os
import numpy as np
from operator import itemgetter

INPUT_DIR = "input"
OUTPUT_DIR = "output"

global score
score = 0

class Snake():
    def __init__(self, length: int) -> None:
        self.length = length
        self.score = 0
        self.sequence = []
    
    def __lt__(self, other):
        return self.length < other.length
    
    def __sub__(self, other):
        return Snake(length=self.length - other.length)
    
    def __str__(self) -> str:
        return str(self.length)
    
    def __repr__(self) -> str:
        return self.__str__()


def solution(input):
    params = (int(val) for val in input[0].split(" "))
    n_rows, n_cols, n_snakes = params
    snakes = np.array([])
    
    for snakes_length in input[1].split(" "):
        snakes = np.append(snakes, Snake(length=int(snakes_length)))

    # print([np.array(row.strip().split(" ")) for row in input[2:]])
    grid = np.array([np.array(row.strip().split(" ")) for row in input[2:]])
    print(n_rows, n_cols, n_snakes)
    # print(snakes)
    # print(grid)

    output = list()
    x, y = 0, 0
    for snake in snakes:
        x, y = crawl(grid, snake, 0, 0)
        output.append(" ".join(snake.sequence))

    print(sum([snake.score for snake in snakes]))
    global score
    score += sum([snake.score for snake in snakes])

    # print(output)
    return "\n".join(output) + "\n"


def crawl(grid, snake: Snake, start_i_x=0, start_i_y=0):
    def next(start_i_x, start_i_y):
        # print(n_rows, n_cols, start_i_x, start_i_y)
        if start_i_x >= n_rows:
            start_i_x = 0
            start_i_y += 1
            if start_i_y >= n_cols:
                raise ValueError
        if grid[(start_i_x+1)%n_rows][start_i_y].isdigit():
            return (start_i_x+1)%n_rows, start_i_y, "D", int(grid[(start_i_x+1)%n_rows][start_i_y])
        elif grid[start_i_x][(start_i_y+1)%n_cols].isdigit():
            return start_i_x, (start_i_y+1)%n_cols, "R", int(grid[start_i_x][(start_i_y+1)%n_cols])
        else:
            raise ValueError
    
    def start(start_i_x, start_i_y):
        if start_i_x >= n_rows:
            start_i_x = 0
            start_i_y += 1
            if start_i_y >= n_cols:
                raise ValueError
        i = start_i_x*n_rows + start_i_y
        x, y = i//n_rows, i%n_rows
        try:
            val = grid[x][y]
        except IndexError:
            # print(n_cols, n_rows, i, x, y)
            raise ValueError
        while i < n_cols * n_rows:
            if not val.isdigit() or int(val) < 0:
                i += 1
                x, y = i//n_rows, i%n_rows
                try:
                    val = grid[x][y]
                    if grid[x][y-1].isdigit():
                        return start(x, y)
                    if grid[x-1][y].isdigit():
                        return start(x, y)
                except IndexError:
                    # print(n_cols, n_rows, i, x, y)
                    raise ValueError
            else:
                return x, y
        raise ValueError

    n_rows, n_cols = grid.shape
    # start_i_x, start_i_y = np.unravel_index(grid.argmax(), grid.shape)
    # random_x, random_y = None, None
    # while True:
    #     random_x, random_y = np.random.choice(grid.shape[0]), np.random.choice(grid.shape[1])
    #     if grid[random_x][random_y] != "-" and grid[random_x][random_y] != "*":
    #         start_i_x, start_i_y = random_x, random_y
    #         break
    try:
        # print(start_i_x, start_i_y)
        start_i_x, start_i_y = start(start_i_x, start_i_y)
        # print(start_i_x, start_i_y)
    except ValueError:
        snake.sequence = [""]
        snake.score = 0
        return start_i_x+1, start_i_y
    

    # indices = np.transpose(((grid != "-") & (grid != "*")).nonzero())
    # start_i_x, start_i_y = indices[np.random.choice(indices.shape[0])]

    snake.sequence.extend([str(start_i_y), str(start_i_x)])
    snake.score += int(grid[start_i_x][start_i_y])
    grid[start_i_x][start_i_y] = "-"

    for _ in range(snake.length-1):
        # neighbour_relevance = list()
        # for direction, i_x, i_y in (("D", (start_i_x+1)%n_rows, (start_i_y)%n_cols), 
        #                             ("U", (start_i_x-1)%n_rows, (start_i_y)%n_cols), 
        #                             ("L", (start_i_x)%n_rows, (start_i_y-1)%n_cols), 
        #                             ("R", (start_i_x)%n_rows, (start_i_y+1)%n_cols)):
        #     val = grid[i_x][i_y]
        #     # neighbour_relevance.append((direction, i_x, i_y, int(val)))
        #     try:
        #         neighbour_relevance.append((direction, i_x, i_y, int(val)))
        #     except ValueError:
        #         print(val)
        #         pass
        # try:
        #     neighbour_relevance_i = max(neighbour_relevance, key=itemgetter(3))
        # except ValueError:
        #     snake.sequence = [""]
        #     snake.score = 0
        #     break

        # direction, start_i_x, start_i_y, score = neighbour_relevance_i
        # snake.sequence.append(direction)
        # snake.score += score
        # grid[start_i_x][start_i_y] = "-"

        try:
            start_i_x, start_i_y, direction, score = next(start_i_x, start_i_y)
        except ValueError:
            snake.sequence = [""]
            snake.score = 0
            return start_i_x+1, start_i_y
        snake.sequence.append(direction)
        snake.score += score
        grid[start_i_x][start_i_y] = "-"

    #     print(grid)
    # print()
    return start_i_x+1, start_i_y


if __name__ == "__main__":
    input_files = os.listdir("input")
    for file_name in sorted(input_files)[7:]:
        print(file_name)
        with open(os.path.join(INPUT_DIR, file_name), "r") as file:
            input_content = file.readlines()
        output = solution(input_content)

        with open(os.path.join(OUTPUT_DIR, file_name), "w") as file:
            file.write(output)
        # print(output)
        print()

    print(score)