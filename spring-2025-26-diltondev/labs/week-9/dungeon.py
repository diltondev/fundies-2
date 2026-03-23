# Vertex (unweighted) mode:
from abc import ABC, abstractmethod
import heapq

class Vertex:
    @classmethod
    def make_default_dungeon(cls) -> "Vertex":
        entrance_hall = cls("Entrance Hall")
        torch_corridor = cls("Torch Corridor")
        map_room = cls("Map Room")
        flooded_passage = cls("Flooded Passage")
        trap_room = cls("Trap Room")
        crystal_chamber = cls("Crystal Chamber")
        armoury = cls("Armoury")
        boss_chamber = cls("Boss Chamber")
        entrance_hall.add_adjacent_vertex(torch_corridor)
        entrance_hall.add_adjacent_vertex(map_room)
        entrance_hall.add_adjacent_vertex(flooded_passage)
        torch_corridor.add_adjacent_vertex(map_room)
        torch_corridor.add_adjacent_vertex(trap_room)
        map_room.add_adjacent_vertex(crystal_chamber)
        trap_room.add_adjacent_vertex(armoury)
        crystal_chamber.add_adjacent_vertex(armoury)
        crystal_chamber.add_adjacent_vertex(boss_chamber)
        armoury.add_adjacent_vertex(boss_chamber)
        return entrance_hall
    
    value: str
    adjacent_vertices: list["Vertex"]
    
    def __init__(self, value):
        self.value = value
        self.adjacent_vertices = []

    def add_adjacent_vertex(self, vertex: "Vertex"):
        self.adjacent_vertices.append(vertex)
        vertex.adjacent_vertices.append(self)

    

class Room:
    passages: dict["Room": int]
    
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
        
    def connect(a: "Room", b: "Room", cost: int):
        a.add_passage(b, cost)
        b.add_passage(a, cost)
     
    
    
class Dungeon:
    entrance: Room
    @classmethod
    def make_default_dungeon(cls) -> "Dungeon":
        entrance_hall = Room("Entrance Hall")
        torch_corridor = Room("Torch Corridor")
        map_room = Room("Map Room")
        flooded_passage = Room("Flooded Passage")
        trap_room = Room("Trap Room")
        crystal_chamber = Room("Crystal Chamber")
        armoury = Room("Armoury")
        boss_chamber = Room("Boss Chamber")
        Room.connect(entrance_hall, torch_corridor, 3)
        Room.connect(entrance_hall, map_room, 2)
        Room.connect(entrance_hall, flooded_passage, 4)
        Room.connect(torch_corridor, map_room, 3)
        Room.connect(torch_corridor, trap_room, 5)
        Room.connect(map_room, crystal_chamber, 4)
        Room.connect(trap_room, armoury, 3)
        Room.connect(crystal_chamber, armoury, 3)
        Room.connect(crystal_chamber, boss_chamber, 5)
        Room.connect(armoury, boss_chamber, 7)
        dungeon = cls()
        dungeon.entrance = entrance_hall
        return dungeon
    
    
    def get_shortest_distances_and_last_rooms(self) -> tuple[dict[Room, int], dict[Room: Room]]:
        q = []
        heapq.heappush(q, (0, self.entrance))
        distances: dict[Room: int] = dict()
        distances[self.entrance] = 0
        last_room: dict[Room: Room] = dict()
        last_room[self.entrance] = None

        while q:
            distance, room = heapq.heappop(q)
            for neighbor, path_dist in room.passages.items():
                if neighbor not in distances or distances[neighbor] > distance + path_dist:
                    heapq.heappush(q, (path_dist + distance, neighbor))
                    distances[neighbor] = path_dist + distance
                    last_room[neighbor] = room
        paths: dict[Room, list[Room]] = dict()
        
        return distances, last_room
    
    def get_shortest_distances_and_paths(self) -> tuple[dict[Room, int], dict[Room: list[Room]]]:
        distances, last_rooms = self.get_shortest_distances_and_last_rooms()
        all_rooms = [pair[0] for pair in last_rooms.items()]
        all_paths: dict[Room: list[Room]] = dict()
        for destination in all_rooms:
            path = []
            cur = destination
            while cur is not None:
                path.append(cur)
                cur = last_rooms.get(cur)
            path.reverse()
            all_paths[destination] = path
        return (distances, all_paths)
    
    def get_shortest_distances(self):
        return self.get_shortest_distances_and_last_rooms()[0]

        
   
            
                    

    