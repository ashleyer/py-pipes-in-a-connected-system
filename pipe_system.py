from collections import deque

# Directions for movement and their respective pipe connectors
DIRECTIONS = {
    '═': [(0, -1, '═', '╠', '╦', '╩', '╚', '╔'), (0, 1, '═', '╣', '╦', '╩', '╝', '╗')],
    '║': [(-1, 0, '║', '╦', '╩', '╠', '╔', '╗'), (1, 0, '║', '╦', '╩', '╠', '╚', '╝')],
    '╔': [(0, 1, '═', '╣', '╦', '╩', '╝', '╗'), (1, 0, '║', '╦', '╩', '╠', '╚', '╝')],
    '╗': [(0, -1, '═', '╠', '╦', '╩', '╚', '╔'), (1, 0, '║', '╦', '╩', '╠', '╚', '╝')],
    '╚': [(0, 1, '═', '╣', '╦', '╩', '╝', '╗'), (-1, 0, '║', '╦', '╩', '╠', '╔', '╗')],
    '╝': [(0, -1, '═', '╠', '╦', '╩', '╚', '╔'), (-1, 0, '║', '╦', '╩', '╠', '╔', '╗')],
    '╠': [(0, -1, '═', '╠', '╦', '╩', '╚', '╔'), (1, 0, '║', '╦', '╩', '╠', '╚', '╝'), (-1, 0, '║', '╦', '╩', '╠', '╔', '╗')],
    '╣': [(0, 1, '═', '╣', '╦', '╩', '╝', '╗'), (1, 0, '║', '╦', '╩', '╠', '╚', '╝'), (-1, 0, '║', '╦', '╩', '╠', '╔', '╗')],
    '╦': [(0, -1, '═', '╠', '╦', '╩', '╚', '╔'), (0, 1, '═', '╣', '╦', '╩', '╝', '╗'), (1, 0, '║', '╦', '╩', '╠', '╚', '╝')],
    '╩': [(0, -1, '═', '╠', '╦', '╩', '╚', '╔'), (0, 1, '═', '╣', '╦', '╩', '╝', '╗'), (-1, 0, '║', '╦', '╩', '╠', '╔', '╗')],
    '*': [(0, -1, '═', '╠', '╦', '╩', '╚', '╔'), (0, 1, '═', '╣', '╦', '╩', '╝', '╗'), (1, 0, '║', '╦', '╩', '╠', '╚', '╝'), (-1, 0, '║', '╦', '╩', '╠', '╔', '╗')]
}

def parse_input(file_path):
    grid = {}
    sinks = set()
    source = None
    with open(file_path, 'r') as f:
        for line in f:
            obj, x, y = line.strip().split()
            x, y = int(x), int(y)
            grid[(x, y)] = obj
            if obj == '*':
                source = (x, y)
            elif obj.isupper():
                sinks.add(obj)
    print("Parsed grid:", grid)  # Debugging statement
    print("Source:", source)     # Debugging statement
    print("Sinks:", sinks)       # Debugging statement
    return grid, source, sinks

def find_connected_sinks(file_path):
    grid, source, sinks = parse_input(file_path)
    if not source:
        return ""
    
    queue = deque([source])
    visited = set([source])
    connected_sinks = set()

    print("Initial queue:", queue)  # Debugging statement
    
    while queue:
        x, y = queue.popleft()
        current = grid[(x, y)]
        
        for dx, dy, *valid_pipes in DIRECTIONS[current]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in grid and (nx, ny) not in visited:
                neighbor = grid[(nx, ny)]
                if neighbor in valid_pipes or neighbor == '*':
                    visited.add((nx, ny))
                    queue.append((nx, ny))
                    if neighbor.isupper():
                        connected_sinks.add(neighbor)
        print("Queue after processing cell ({}, {}): {}".format(x, y, queue))  # Debugging statement
    
    print("Connected sinks:", connected_sinks)  # Debugging statement
    return ''.join(sorted(connected_sinks))

# Example usage:
if __name__ == "__main__":
    result = find_connected_sinks("input.txt")
    print("Result:", result)
