import curses
from curses import wrapper
import queue
import time

grid= [
    ["#", "S", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", " ", " ", "#", " ", "#", " ", "#"],
    ["#", "#", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", "#", "#", "#", " ", "#"],
    ["#", " ", " ", " ", "#", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "E", "#"]
]

def print_grid(grid, stdscr, path = []):
    Blue = curses.color_pair(1)
    Red = curses.color_pair(2)

    for i, row in enumerate(grid): #enumrate = index and value
        for j, value in enumerate(row):
            if (i, j) in path:        #shows the path taken in red color
                stdscr.addstr(i, j*2, "S", Red)
            else:
                stdscr.addstr(i, j*2, value, Blue)

def find_start(grid, start):
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None

def find_path(grid, stdscr):
    start = "S"
    end = "E"
    # wall = "#"
    start_position = find_start(grid, start)

    q = queue.Queue()

    q.put((start_position,[start_position])) #track cur_pos and path
    visited = set()

    while not q.empty():
        cur_pos, path = q.get()
        row, col = cur_pos

        stdscr.clear()
        #Calls the print_grid function to render the grid with the current path.
        print_grid(grid, stdscr, path)
        time.sleep(0.3)
        stdscr.refresh()

        if grid[row][col] == end:
            return path
        
        for neighbor in find_neighbors(grid, row, col):
            #checks if The neighbor cell has not been visited before and
            #The neighbor cell is not a wall(where # = wall)
            if neighbor not in visited and grid[neighbor[0]][neighbor[1]] != "#":
                new_path = path + [neighbor]
                q.put((neighbor, new_path))
                visited.add(neighbor) #mark neigbor as visited

def find_neighbors(grid, row, col):
    neighbors = []

    if row > 0: #up
        neighbors.append((row-1, col))
    if row+1 < len(grid):#down
        neighbors.append((row+1, col))
    if col > 0:#left
        neighbors.append((row, col-1))
    if col+1 < len(grid[0]):#right, 0 coz matrix may not always square(same r and c)
        neighbors.append((row, col+1))

    return neighbors

def main(stdscr):  #standard op screen
    #curses.init_pair(id, foreground_color, background_color)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path(grid, stdscr)
    stdscr.getch() #Waits for a key press to keep the window open

wrapper(main) #initializes curses module and call main
