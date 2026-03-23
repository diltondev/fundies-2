from collections import deque

from dungeon import Room, Vertex, Dungeon

def dfs_traverse(vertex: Vertex, visited: list[Vertex] = list(), hops=0):
    if vertex in visited:
        return
    print(f"{vertex.value}: {hops} {"hops" if hops != 1 else "hop"}")
    visited.append(vertex)
    for v in vertex.adjacent_vertices:
        dfs_traverse(v, visited, hops + 1)
        
def bfs_traverse(vertex: Vertex):
    visited = [vertex]
    q = deque([vertex])
    distances = {vertex: 0}
    while q:
        vertex = q.popleft()
        for v in vertex.adjacent_vertices:
            if v not in visited:
                visited.append(v)
                distances[v] = distances[vertex] + 1
                q.append(v)
    for dist in distances.items():
        print(f"{dist[0].value}: {dist[1]} {"hops" if dist[1] != 1 else "hop"}")
        
    

if __name__ == "__main__":
    print("Running DFS on unweighted dungeon (# Hops)")
    entrance_hall = Vertex.make_default_dungeon()
    dfs_traverse(entrance_hall)
    
    print("\n")
    print("Running BFS on unweighted dungeon (# Hops)")
    bfs_traverse(entrance_hall)
    
    print("\n")
    print("Running Dijkstra's on Dungeon")
    d = Dungeon.make_default_dungeon()
    distances, paths = d.get_shortest_distances_and_paths()
    
    #find boss room in keys of distances
    boss_room = None
    for room in distances.keys():
        if room.name == "Boss Chamber":
            boss_room = room
            break
    print(f"Shortest path to Boss Chamber: {distances[boss_room]} cost, path: {[room.name for room in paths[boss_room]]}")
    