from collections import deque

# Directions for movement and their respective pipe connectors
DIRECTIONS = {
    '═': [(0, -1, '═'), (0, 1, '═')],
    '║': [(-1, 0, '║'), (1, 0, '║')],
    '╔': [(0, 1, '═'), (1, 0, '║')],
    '╗': [(0, -1, '═'), (1, 0, '║')],
    '╚': [(0, 1, '═'), (-1, 0, '║')],
    '╝': [(0, -1, '═'), (-1, 0, '║')],
    '╠': [(0, -1, '═'), (0, 1, '═'), (1, 0, '║'), (-1, 0, '║')],
    '╣': [(0, -1, '═'), (0, 1, '═'), (1, 0, '║'), (-1, 0, '║')],
    '╦': [(0, -1, '═'), (0, 1, '═'), (1, 0, '║')],
    '╩': [(0, -1, '═'), (0, 1, '═'), (-1, 0, '║')],
    '*': [(0, -1, '═'), (0, 1, '═'), (1, 0, '║'), (-1, 0, '║')]
}

def parse_input(file_path):
    grid = {}
    sinks = set()
    source = None
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            obj, x, y = line.split()
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

def is_connected(pipe1, pipe2, direction):
    """
    Determines if two pipes are connected based on their type and direction of connection.
    """
    if direction == (0, 1):  # Right
        return pipe2 in ['═', '╠', '╦', '╩', '╚', '╔', '*'] and pipe1 in ['═', '╣', '╦', '╩', '╝', '╗', '*']
    elif direction == (0, -1):  # Left
        return pipe2 in ['═', '╣', '╦', '╩', '╝', '╗', '*'] and pipe1 in ['═', '╠', '╦', '╩', '╚', '╔', '*']
    elif direction == (1, 0):  # Down
        return pipe2 in ['║', '╦', '╩', '╠', '╚', '╔', '*'] and pipe1 in ['║', '╦', '╩', '╣', '╝', '╗', '*']
    elif direction == (-1, 0):  # Up
        return pipe2 in ['║', '╦', '╩', '╣', '╝', '╗', '*'] and pipe1 in ['║', '╦', '╩', '╠', '╚', '╔', '*']
    return False

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
        
        for dx, dy, valid_pipe in DIRECTIONS[current]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in grid and (nx, ny) not in visited:
                neighbor = grid[(nx, ny)]
                # Check if the current pipe and neighbor pipe are connected
                if is_connected(current, neighbor, (dx, dy)):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
                    if neighbor.isupper():
                        connected_sinks.add(neighbor)
                print(f"Checking ({nx}, {ny}): Neighbor={neighbor}, Current={current}, Direction=({dx}, {dy}), Valid_pipe={valid_pipe}")  # Debugging statement
        print("Queue after processing cell ({}, {}): {}".format(x, y, queue))  # Debugging statement
    
    print("Connected sinks:", connected_sinks)  # Debugging statement
    return ''.join(sorted(connected_sinks))

# Example usage:
if __name__ == "__main__":
    result = find_connected_sinks("input.txt")
    print("Result:", result)