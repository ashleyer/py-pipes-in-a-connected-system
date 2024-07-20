def is_connected(cell1, cell2):
    """
    Check if two cells (with pipe characters) are connected through their shared edge.
    """
    openings = {
        '═': [(0, -1), (0, 1)],  # left and right
        '║': [(-1, 0), (1, 0)],  # top and bottom
        '╔': [(1, 0), (0, 1)],   # bottom and right
        '╗': [(1, 0), (0, -1)],  # bottom and left
        '╚': [(-1, 0), (0, 1)],  # top and right
        '╝': [(-1, 0), (0, -1)], # top and left
        '╠': [(0, -1), (0, 1), (1, 0)], # left, right, bottom
        '╣': [(0, -1), (0, 1), (-1, 0)],# left, right, top
        '╦': [(1, 0), (0, -1), (0, 1)], # bottom, left, right
        '╩': [(0, -1), (0, 1), (-1, 0)] # left, right, top
    }
    
    special_openings = [(-1, 0), (1, 0), (0, -1), (0, 1)] # top, bottom, left, right

    if cell1 in ['*'] or cell2 in ['*']:
        return True
    if cell1.isalpha() or cell2.isalpha():
        return True
    
    for direction in openings.get(cell1, []):
        if (-direction[0], -direction[1]) in openings.get(cell2, []):
            return True
    
    return False


def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    objects = []
    for line in lines:
        obj, x, y = line.strip().split()
        x, y = int(x), int(y)
        objects.append((obj, x, y))
    return objects


def build_grid(objects):
    max_x = max([x for _, x, _ in objects])
    max_y = max([y for _, _, y in objects])
    
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for obj, x, y in objects:
        grid[y][x] = obj
    return grid


def find_connected_sinks(grid):
    from collections import deque
    
    def neighbors(x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                yield nx, ny
    
    def bfs(source_x, source_y):
        visited = set()
        queue = deque([(source_x, source_y)])
        sinks = set()
        
        while queue:
            x, y = queue.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            if grid[y][x].isalpha():
                sinks.add(grid[y][x])
            
            for nx, ny in neighbors(x, y):
                if (nx, ny) not in visited and is_connected(grid[y][x], grid[ny][nx]):
                    queue.append((nx, ny))
        
        return sinks
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '*':
                source_x, source_y = x, y
                break
    
    return bfs(source_x, source_y)


def connected_sinks(file_path):
    objects = read_input(file_path)
    grid = build_grid(objects)
    sinks = find_connected_sinks(grid)
    return ''.join(sorted(sinks))


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 pipe_system.py <input_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = connected_sinks(file_path)
    print(result)