from collections import deque
from pymongo import MongoClient

def find_shortest_path():
    CONNECTION_STRING = "mongodb+srv://kishorebabu200409:kishore26@cluster0.hf4t5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(CONNECTION_STRING)
    db = client['number_plate_recognition']
    path_collection = db['parkingspace']

    # Fetch the parking grid from MongoDB
    path_data = path_collection.find_one()
    if not path_data:
        return [], None

    grid = path_data['path']

    if not grid or not grid[0]:
        return [], None

    rows, cols = len(grid), len(grid[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left
    queue = deque([(0, 0, [])])  # (row, col, path_so_far)
    visited = set([(0, 0)])

    while queue:
        r, c, path = queue.popleft()

        # If it's a free space (0) and not the starting position
        if grid[r][c] == 0 and (r, c) != (0, 0):
            # Fill the nearest free space with 1 (occupied)
            grid[r][c] = 1  

            # Find the next nearest free space
            next_nearest_free_space = None
            queue2 = deque([(r, c)])
            visited2 = set([(r, c)])

            while queue2:
                rr, cc = queue2.popleft()
                if grid[rr][cc] == 0:
                    next_nearest_free_space = (rr, cc)
                    break
                for dr, dc in directions:
                    nr, nc = rr + dr, cc + dc
                    if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited2:
                        visited2.add((nr, nc))
                        queue2.append((nr, nc))

            # Update MongoDB with modified grid, nearest space, and path taken
            path_collection.update_one(
                {"_id": path_data["_id"]},
                {
                    "$set": {
                        "path": grid,
                        "nearest_free_space": (r, c),  # Nearest free space now occupied
                        "path_to_nearest": path + [(r, c)]  # Store path taken
                    }
                }
            )

            return path + [(r, c)], (r, c)

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, path + [(nr, nc)]))

    return [], None  # No free space found

# Run function
# path, nearest_free_space = find_shortest_path()

# print("Shortest Path:", path)
# print("Nearest Free Space Position:", nearest_free_space)
