# Lab: Dungeon Exploration

You are writing the pathfinding logic for a dungeon game. The dungeon is a graph: each room is a vertex, and each passage between rooms is an edge. Your code will need to answer two questions that any dungeon crawler needs to solve:

1. Which rooms are reachable from the entrance?
2. What is the shortest route to the boss in terms of tiles walked?

## The Dungeon

| Room A          | Room B          | Tiles to traverse |
|-----------------|-----------------|-------------------|
| Entrance Hall   | Torch Corridor  | 3                 |
| Entrance Hall   | Map Room        | 2                 |
| Entrance Hall   | Flooded Passage | 4                 |
| Torch Corridor  | Map Room        | 3                 |
| Torch Corridor  | Trap Room       | 5                 |
| Map Room        | Crystal Chamber | 4                 |
| Trap Room       | Armoury         | 3                 |
| Crystal Chamber | Armoury         | 3                 |
| Crystal Chamber | Boss Chamber    | 5                 |
| Armoury         | Boss Chamber    | 7                 |

All passages are undirected, a player can move in either direction. The number on each passage is how many tiles a player must traverse to pass through it.

The Flooded Passage is a dead end. The Trap Room connects through a hidden back passage into the Armoury. The Trap Room is only accessible via a long passage from the Torch Corridor (5 tiles), but once inside, a hidden back passage leads directly to the Armoury at just 3 tiles.

## Mapping the dungeon

Before worrying about movement cost, a player needs to know which rooms they can actually reach from the entrance. For this part, ignore the costs entirely and treat all passages as equal.

### Build the graph
Draw a map of the graph on a piece of paper, then use the `Vertex` class from the lecture to construct the dungeon.

```python
class Vertex:
    def __init__(self, value):
        self.value = value
        self.adjacent_vertices = []

    def add_adjacent_vertex(self, vertex):
        self.adjacent_vertices.append(vertex)
        vertex.adjacent_vertices.append(self)
```

Create a vertex for each room and add passages from the table above.

### Traversal
Use BFS and DFS traversal to print out the order in which each room is visited.

### Finding the furthest room
You want to know how many **hops** (not the number of tiles) each room is from the Entrance Hall. Before writing any code, think about how DFS and BFS each move through the graph:

- DFS follows a single path as deep as it can go before backtracking. At any point during the traversal, it knows exactly how many steps it has taken along the current path.
- BFS fans out in all directions simultaneously, visiting all rooms one hop away before moving to rooms two hops away. It does not follow a single path.

DFS is more naturally suited to tracking hop count from the source. Modify your chosen traversal to track the number of hops from the Entrance Hall to each room. One way to do this is to pass the hop count as a parameter as an accumulator increments with each recursive call:

```python 
def dfs_traverse(vertex, visited=None, hops=0):
    # your code here
```

Print each room alongside its hop count:

``` raw
Entrance Hall: 0 hops
Torch Corridor: 1 hop
...
```

- Which room is furthest from the Entrance Hall?
- Are there any rooms at the same number of hops? What does that tell you about the structure of the dungeon?

## Finding the shortest route

Knowing which rooms are reachable is not enough, a player also wants to walk as few **tiles** as possible. This is where movement costs matter.

Modify your implementation to store a movement cost on each passage corresponding to the tiles to traverse in the table above.

Use the `Room` class below:

```python
class Room:
    def __init__(self, name):
        self.name = name
        self.passages = {}      # {Room: cost}

    def __eq__(self, other):
        return isinstance(other, Room) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return f"Room({self.name})"

    def add_passage(self, room, cost):
        self.passages[room] = cost


def connect(a, b, cost):
    a.add_passage(b, cost)
    b.add_passage(a, cost)
```

Rebuild the dungeon using this class and add all passages with their costs from the table.

### Dijkstra's Algorithm
Using the implementation from the lecture, run Dijkstra's algorithm from the Entrance Hall.

The lecture implementation returns two dictionaries: `cheapest_fares` and `previous_station`. In this dungeon context these are the same idea, a dictionary of the lowest known tile count to each room, and a dictionary recording which room we came from to achieve it.

Write a function that reconstructs and prints the full route to every reachable room:

```raw
Boss Chamber
  Route: Entrance Hall - Map Room - Crystal Chamber - Boss Chamber
  Total tiles: 11
```
  
The `shortest_route` function from the lecture is a good starting point, you will need to adapt the variable names to match your Room class, and call it once for each room in the dungeon.
