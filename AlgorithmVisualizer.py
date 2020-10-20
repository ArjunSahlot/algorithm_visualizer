import time
from queue import PriorityQueue

import pygame

''' Constants '''
pygame.init()
WIDTH = 1000
ROWS = 50 # Lower number for increased performance
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm Visualizer, By: Arjun Sahlot")
font = pygame.font.SysFont('comicsans', 100)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 120)
ORANGE = (255, 140, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BROWN = (110,50,10)


''' Functions/Classes/Gameloop '''
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.width = width
        self.color = WHITE
        self.neighbors = []
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_checking(self):
        return self.color == YELLOW

    def is_checked(self):
        return self.color == ORANGE

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == GREEN

    def is_end(self):
        return self.color == RED

    def is_path(self):
        return self.color == BROWN

    def reset(self):
        self.color = WHITE

    def make_checking(self):
        self.color = YELLOW

    def make_checked(self):
        self.color = ORANGE

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = RED

    def make_path(self):
        self.color = BROWN

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])


def reconstruct_path(came_from, start, end, draw, current):
    while current in came_from:
        current = came_from[current]
        if current != start:
            current.make_path()
        draw()


def celldistance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x2-x1) + abs(y2-y1)


def not_found_mesg(window, width):
    text = font.render("Path Not Found", 1, BLACK)
    window.blit(text, (width//2 - text.get_width()//2, 100))
    pygame.display.update()
    time.sleep(2)


def bestfirst(window, draw, width, grid, start, end):
    count = 0
    checked_set = PriorityQueue()
    checked_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = celldistance(start.get_pos(), end.get_pos())

    checked_set_checker = {start}

    while not checked_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = checked_set.get()[2]

        if current == end:
            reconstruct_path(came_from, start, end, draw, current)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = celldistance(neighbor.get_pos(), end.get_pos())

                if neighbor not in checked_set_checker:
                    count += 1
                    checked_set.put((f_score[neighbor], count, neighbor))
                    checked_set_checker.add(neighbor)
                    neighbor.make_checked()

        draw()

        if current != start:
            current.make_checking()

    not_found_mesg(window, width)


def dijkstras(window, draw, width, grid, start, end):
        count = 0
        checked_set = PriorityQueue()
        checked_set.put((0, count, start))
        came_from = {}
        g_score = {node: float("inf") for row in grid for node in row}
        g_score[start] = 0

        checked_set_checker = {start}

        while not checked_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = checked_set.get()[2]
            # checked_set_checker.remove(current)

            if current == end:
                reconstruct_path(came_from, start, end, draw, current)
                end.make_end()
                return True

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score

                    if neighbor not in checked_set_checker:
                        count += 1
                        checked_set.put((g_score[neighbor], count, neighbor))
                        checked_set_checker.add(neighbor)
                        neighbor.make_checked()

            draw()

            if current != start:
                current.make_checking()

        not_found_mesg(window, width)


def alphastar(window, draw, width, grid, start, end):
    count = 0
    checked_set = PriorityQueue()
    checked_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = celldistance(start.get_pos(), end.get_pos())

    checked_set_checker = {start}

    while not checked_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = checked_set.get()[2]
        # checked_set_checker.remove(current)

        if current == end:
            reconstruct_path(came_from, start, end, draw, current)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + celldistance(neighbor.get_pos(), end.get_pos())

                if neighbor not in checked_set_checker:
                    count += 1
                    checked_set.put((f_score[neighbor], count, neighbor))
                    checked_set_checker.add(neighbor)
                    neighbor.make_checked()

        draw()

        if current != start:
            current.make_checking()

    not_found_mesg(window, width)


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(Node(i,j,gap,rows))

    return grid


def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(window, GREY, (j*gap, 0), (j*gap, width))


def draw_window(window, grid, rows, width):
    window.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(window)
    draw_grid(window, rows, width)
    pygame.display.update()


def click_pos(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = x // gap
    col = y // gap

    return row, col


def main(window, rows, width):
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw_window(window, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = click_pos(pos, rows, width)
                node = grid[row][col]
                if start == None and node != end:
                    start = node
                    start.make_start()
                elif end == None and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = click_pos(pos, rows, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN and start != None and end != None:
                if event.key == pygame.K_a:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    alphastar(window, lambda: draw_window(window, grid, rows, width), width, grid, start, end)

                if event.key == pygame.K_d:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    dijkstras(window, lambda: draw_window(window, grid, rows, width), width, grid, start, end)

                if event.key == pygame.K_b:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    bestfirst(window, lambda: draw_window(window, grid, rows, width), width, grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


    pygame.quit()


main(WINDOW, ROWS, WIDTH)
