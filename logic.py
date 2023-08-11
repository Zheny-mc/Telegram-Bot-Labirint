from random import choice

cols = 0
rows = 0
grid_cell = []

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def check_cell(self, x, y):
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
           return False
        return grid_cell[x + y * cols]

    def check_neighbours(self):
        neighbours = []

        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)

        def add_neighbour(cell: Cell):
            if cell and not cell.visited:
                neighbours.append(cell)

        add_neighbour(top)
        add_neighbour(right)
        add_neighbour(bottom)
        add_neighbour(left)

        return choice(neighbours) if neighbours else None

def remove_walls(current_cell: Cell, next_cell: Cell):
    dx = current_cell.x - next_cell.x
    dy = current_cell.y - next_cell.y

    if dx == 1:
        current_cell.walls['left'] = False
        next_cell.walls['right'] = False
    if dx == -1:
        current_cell.walls['right'] = False
        next_cell.walls['left'] = False
    if dy == 1:
        current_cell.walls['top'] = False
        next_cell.walls['bottom'] = False
    if dy == -1:
        current_cell.walls['bottom'] = False
        next_cell.walls['top'] = False

def check_wall(grid_cell, x, y):
    if x % 2 == 0 and y % 2 == 0:
        return False
    if x % 2 == 1 and y % 2 == 1:
        return True

    if x % 2 == 0:
        grid_x = x // 2
        grid_y = (y - 1) // 2
        return grid_cell[grid_x + grid_y * cols].walls['bottom']
    else:
        grid_x = (x - 1) // 2
        grid_y = y // 2
        return grid_cell[grid_x + grid_y * cols].walls['right']


def get_map_cell(cols_, rows_):
    global cols
    global rows
    global grid_cell

    cols = cols_
    rows = rows_

    grid_cell = [Cell(x, y) for y in range(rows) for x in range(cols)]
    current_cell = grid_cell[0]
    current_cell.visited = True

    stack = []
    while True:
        next_cell: Cell = current_cell.check_neighbours()
        if next_cell:
            next_cell.visited = True
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
            stack.append(current_cell)
        elif stack:
            current_cell = stack.pop()
        else:
            break

    return [check_wall(grid_cell, x, y) for y in range(rows*2 - 1) for x in range(cols*2 - 1)]

def check_step(user_data: dict, step: str):
    new_x, new_y = user_data['x'], user_data['y']

    if step == 'left':
        new_x -= 1
    elif step == 'right':
        new_x += 1
    elif step == 'up':
        new_y -= 1
    elif step == 'down':
        new_y += 1

    map_cell = user_data['map']
    if new_x < 0 or new_x > 2 * cols - 2 or new_y < 0 or new_y > 2 * rows - 2:
        return ()

    if map_cell[new_x+new_y * (2 * cols - 1)]:
        return ()

    return (new_x, new_y)

def is_win(user_data: dict, step: str):
    new_x, new_y = user_data['x'], user_data['y']

    if step == 'left':
        new_x -= 1
    elif step == 'right':
        new_x += 1
    elif step == 'up':
        new_y -= 1
    elif step == 'down':
        new_y += 1

    map_cell = user_data['map']



