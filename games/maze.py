from PIL import Image, ImageDraw
import random
from collections import deque

class Maze:
    @staticmethod
    def create_maze(width, height, start_x, start_y, level):
        size_map = {
            (0, 2): (3, 3),
            (3, 4): (5, 3),
            (5, 6): (5, 5),
            (7, 8): (7, 5),
            (9, 10): (7, 7),
            (11, 12): (9, 7),
            (13, 14): (9, 9),
            (15, 16): (11, 9),
            (17, 18): (11, 11),
            (19, 20): (13, 11),
            (21, 23): (13, 13),
            (24, 27): (15, 13),
            (28, 32): (15, 15),
            (33, 38): (17, 15),
            (39, 44): (17, 17),
            (45, 50): (19, 17),
            (51, 56): (19, 19),
            (57, 62): (21, 19),
            (63, 68): (21, 21),
            (69, 74): (23, 21),
            (75, 9999999999): (23, 23),
        }
        for (low, high), (w, h) in size_map.items():
            if low <= level <= high:
                width, height = w, h
                break
        else: width = height = 23
        maze = [[1] * width for _ in range(height)]
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        def is_valid(nx, ny): 
            return 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1
        def carve_maze(x, y):
            maze[y][x] = 0
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny):
                    maze[y + dy // 2][x + dx // 2] = 0
                    carve_maze(nx, ny)
        carve_maze(start_x, start_y)
        return maze
    @staticmethod
    def save_maze_as_image(maze, cell_size, filename, start, end, user_id):
        height = len(maze)
        width = len(maze[0])
        img = Image.new("RGB", (width * cell_size, height * cell_size), "white")
        draw = ImageDraw.Draw(img)
        for y in range(height):
            for x in range(width):
                top_left = (x * cell_size, y * cell_size)
                bottom_right = ((x + 1) * cell_size, (y + 1) * cell_size)
                fill = "black" if maze[y][x] == 1 else "white"
                draw.rectangle([top_left, bottom_right], fill=fill, outline="gray")
        draw.rectangle([start[0] * cell_size, start[1] * cell_size, (start[0] + 1) * cell_size, (start[1] + 1) * cell_size], fill="lime")
        draw.rectangle([end[0] * cell_size, end[1] * cell_size, (end[0] + 1) * cell_size, (end[1] + 1) * cell_size], fill="red")
        img = img.resize((1000, 1000), Image.Resampling.NEAREST)
        img.save(filename)
        Maze.save_bordered_floor_image(maze, cell_size, start, end, user_id)
    @staticmethod
    def save_bordered_floor_image(maze, cell_size, start, end, user_id):
        height = len(maze)
        width = len(maze[0])
        img = Image.new("RGB", (width * cell_size, height * cell_size), "white")
        draw = ImageDraw.Draw(img)
        for y in range(height):
            for x in range(width):
                top_left = (x * cell_size, y * cell_size)
                bottom_right = ((x + 1) * cell_size, (y + 1) * cell_size)
                draw.rectangle([top_left, bottom_right], outline="gray")
        draw.rectangle([start[0] * cell_size, start[1] * cell_size, (start[0] + 1) * cell_size, (start[1] + 1) * cell_size], fill="lime")
        img = img.resize((1000, 1000), Image.Resampling.NEAREST)
        img.save(f'mazebordered{user_id}.png')
    @staticmethod
    def find_path(maze, start, end):
        width, height = len(maze[0]), len(maze)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        direction_labels = {(0, 1): "down", (1, 0): "right", (0, -1): "up", (-1, 0): "left"}
        queue = deque([start])
        came_from = {start: None}
        while queue:
            current = queue.popleft()
            if current == end: break
            for dx, dy in directions:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 0 and (nx, ny) not in came_from:
                    queue.append((nx, ny))
                    came_from[(nx, ny)] = current
        path, directions_list, step = [], [], end
        while step:
            path.append(step)
            if came_from[step]:
                prev_step = came_from[step]
                dx, dy = step[0] - prev_step[0], step[1] - prev_step[1]
                if (dx, dy) in direction_labels:
                    directions_list.append(direction_labels[(dx, dy)])
            step = came_from[step]
        path.reverse()
        directions_list.reverse()
        return path, directions_list
    @staticmethod
    def find_random_distant_point(maze, start, min_distance=3):
        width, height = len(maze[0]), len(maze)
        candidates = []
        for y in range(height):
            for x in range(width):
                if maze[y][x] == 0 and (x, y) != start:
                    distance = abs(start[0] - x) + abs(start[1] - y)
                    if distance >= min_distance:
                        candidates.append((x, y))
        if candidates: return random.choice(candidates)
        return None
    @staticmethod
    def save_mazes(user_id, level):
        start_x, start_y = 0, 0
        cell_size = 20
        maze = Maze.create_maze(0, 0, start_x, start_y, level)
        end_x, end_y = Maze.find_random_distant_point(maze, (start_x, start_y))
        path, directions_list = Maze.find_path(maze, (start_x, start_y), (end_x, end_y))
        Maze.save_maze_as_image(maze, cell_size, f"maze{user_id}.png", (start_x, start_y), (end_x, end_y), user_id)
        return directions_list
