from webtris_graph import (
    BreadthFirstSearch,
    RouteSegment,
    DepthFirstSearch,
    DijkstrasAlgoSearch,
    RouteSegmentExternal,
    SearchStrategy,
)
from datetime import datetime

test_data = {
    "7-12": [
        {"id": 138, "description": "M25/4546A"},
        {"id": 144, "description": "M25/4681A"},
        {"id": 479, "description": "M25/4806A"},
        {"id": 544, "description": "M25/4700A"},
        {"id": 547, "description": "M25/4515A"},
        {"id": 598, "description": "M25/4727A"},
        {"id": 699, "description": "M25/4479A"},
        {"id": 752, "description": "M25/4475A"},
        {"id": 778, "description": "M25/4811A"},
        {"id": 885, "description": "M25/4565A"},
        {"id": 1069, "description": "M25/4607A"},
        {"id": 1135, "description": "M25/4690A"},
        {"id": 1221, "description": "M25/4757A"},
        {"id": 1270, "description": "M25/4534A"},
        {"id": 1442, "description": "M25/4605A"},
        {"id": 1479, "description": "M25/4721A"},
        {"id": 1914, "description": "M25/4704A"},
        {"id": 1990, "description": "M25/4620A"},
        {"id": 2005, "description": "M25/4483A"},
        {"id": 2089, "description": "M25/4777A"},
        {"id": 2097, "description": "M25/4497A"},
        {"id": 2149, "description": "M25/4826A"},
        {"id": 2419, "description": "M25/4617J"},
        {"id": 2486, "description": "M25/4509A"},
        {"id": 2530, "description": "M25/4752A"},
        {"id": 2636, "description": "M25/4787A"},
        {"id": 3003, "description": "M25/4696A"},
        {"id": 3323, "description": "M25/4583A"},
        {"id": 3437, "description": "M25/4490A"},
        {"id": 3714, "description": "M25/4822A"},
        {"id": 3835, "description": "M25/4658A"},
        {"id": 3897, "description": "M25/4792A"},
        {"id": 4000, "description": "M25/4551A"},
        {"id": 4092, "description": "M25/4522A"},
        {"id": 4145, "description": "M25/4501A"},
        {"id": 4202, "description": "M25/4662A"},
        {"id": 4223, "description": "M25/4617A"},
        {"id": 4714, "description": "M25/4762A"},
        {"id": 4719, "description": "M25/4470A"},
        {"id": 4761, "description": "M25/4747A"},
        {"id": 4894, "description": "M25/4802A"},
        {"id": 5107, "description": "M25/4817A"},
        {"id": 5118, "description": "M25/4686A"},
        {"id": 5138, "description": "M25/4772A"},
        {"id": 5176, "description": "M25/4767A"},
        {"id": 5261, "description": "M25/4742A"},
        {"id": 5288, "description": "M25/4592A"},
        {"id": 5457, "description": "M25/4528A"},
        {"id": 5526, "description": "M25/4637A"},
        {"id": 5546, "description": "M25/4783A"},
        {"id": 5712, "description": "M25/4653A"},
        {"id": 5842, "description": "M25/4712A"},
        {"id": 5875, "description": "M25/4507A"},
        {"id": 5914, "description": "M25/4666A"},
        {"id": 5990, "description": "M25/4797A"},
        {"id": 6156, "description": "M25/4537A"},
        {"id": 6252, "description": "M25/4732A"},
    ],
    "12-13": [
        {"id": 8, "description": "M25/4876A"},
        {"id": 1811, "description": "M25/4848A"},
        {"id": 1910, "description": "M25/4860A"},
        {"id": 2952, "description": "M25/4866A"},
        {"id": 2992, "description": "M25/4832A"},
        {"id": 3319, "description": "M25/4854A"},
        {"id": 5245, "description": "M25/4879A"},
        {"id": 5662, "description": "M25/4843A"},
        {"id": 5681, "description": "M25/4836A"},
    ],
    "13-14": [
        {"id": 279, "description": "M25/4909A"},
        {"id": 737, "description": "M25/4883A"},
        {"id": 3671, "description": "M25/4898A"},
        {"id": 4053, "description": "M25/4903A"},
        {"id": 4354, "description": "M25/4887A"},
        {"id": 5317, "description": "M25/4892A"},
    ],
    "14-Heathrow": [
        {"id": 746, "description": "M25/7106B"},
        {"id": 2153, "description": "M25/7108B"},
        {"id": 2977, "description": "M25/7113B"},
    ],
    "A30": [{"id": 9005, "description": "6178/1"}],
}


def test_make_routesegment():
    segment = RouteSegment(
        name="segment",
        site_ids=[138, 144, 479],
        date=datetime(2025, 3, 10, 12, 45, 0),
        length=3,
    )
    print(f"avg_speed = {segment.get_average_speed()}")
    print(f"traversal time = {segment.get_traversal_time()}")
    assert True


def test_dfs():
    date = datetime(2025, 3, 10, 12, 45, 0)
    segA = RouteSegment(name="segA", site_ids=[138, 144, 479], date=date, length=3)
    segB = RouteSegment(name="segB", site_ids=[544, 547, 598], date=date, length=3)
    segC = RouteSegment(name="segC", site_ids=[699, 752, 778], date=date, length=3)

    segA.next_segments.append(segB)
    segB.next_segments.append(segC)
    search = DepthFirstSearch()
    result = search.search(segA, segC)
    print(f"DFS returns: {result}")


def test_bfs():
    date = datetime(2025, 3, 10, 12, 45, 0)
    segA = RouteSegment(name="segA", site_ids=[138, 144, 479], date=date, length=3)
    segB = RouteSegment(name="segB", site_ids=[544, 547, 598], date=date, length=3)
    segC = RouteSegment(name="segC", site_ids=[699, 752, 778], date=date, length=3)
    segD = RouteSegment(name="segD", site_ids=[885, 1069, 1135], date=date, length=3)
    segE = RouteSegment(name="segE", site_ids=[1221, 1270, 1442], date=date, length=3)

    segA.next_segments.append(segB)
    segA.next_segments.append(segD)
    segB.next_segments.append(segC)
    segC.next_segments.append(segE)
    segD.next_segments.append(segE)
    search = BreadthFirstSearch()
    result = search.search(segA, segE)
    print(f"BFS returns: {result}")


def test_dijkstra():
    """
    A function to spawn an instance of and test DijkstrasAlgoSearch()
    """
    date = datetime(2025, 3, 10, 12, 45, 0)
    segA = RouteSegment(name="segA", site_ids=[138, 144, 479], date=date, length=3)
    segB = RouteSegment(name="segB", site_ids=[544, 547, 598], date=date, length=3)
    segC = RouteSegment(name="segC", site_ids=[699, 752, 778], date=date, length=3)
    segD = RouteSegment(name="segD", site_ids=[885, 1069, 1135], date=date, length=3)
    segE = RouteSegment(name="segE", site_ids=[1221, 1270, 1442], date=date, length=3)

    segA.next_segments.append(segB)
    segA.next_segments.append(segD)
    segB.next_segments.append(segC)
    segC.next_segments.append(segE)
    segD.next_segments.append(segE)
    search = DijkstrasAlgoSearch()
    result = search.search(segA, segE)
    print(f"Dijkstras returns: {result}")


# Make the RouteSegment combinations for AE3 possible Gatwick -> Heathrow routes
DATE = datetime(2026, 1, 19, 8, 50, 0)
gatwick = RouteSegmentExternal("Gatwick", DATE, 0, 1)
m25_j12 = RouteSegment("M25 J12", [site["id"] for site in test_data["7-12"]], DATE, 23)
gatwick.next_segments.append(m25_j12)
m25_j13 = RouteSegment("M25 J13", [site["id"] for site in test_data["12-13"]], DATE, 3)
local_roads_heathrow = RouteSegmentExternal(
    "Local Roads to Heathrow", DATE, 12, 12 / (20 / 60)
)  # 12 miles per (20 minutes/60 minutes per hour) gets speed to go 12 miles in 20 minutes
m25_j12.next_segments.append(m25_j13)
m25_j12.next_segments.append(local_roads_heathrow)
a30_heathrow = RouteSegment(
    "A30 to Heathrow", [site["id"] for site in test_data["A30"]], DATE, 3.8
)
m25_j13.next_segments.append(a30_heathrow)
m25_j14 = RouteSegment(
    "M25 J14 to Heathrow", [site["id"] for site in test_data["13-14"]], DATE, 3
)
m25_j13.next_segments.append(m25_j14)
heathrow = RouteSegmentExternal("Heathrow", DATE, 0, 1)
local_roads_heathrow.next_segments.append(heathrow)
a30_heathrow.next_segments.append(heathrow)
m25_j14.next_segments.append(heathrow)


def pretty_print_search(results: list[RouteSegment]):
    result_str = ""
    total_time = 0
    total_distance = 0
    for r in results:
        result_str += str(r) + " "
        total_time += r.get_traversal_time()
        total_distance += r.length
    total_time *= 60
    result_str = result_str.strip() + f". Total journey time: {total_time:.1f} minutes. Total distance: {total_distance} miles"
    return result_str.strip()


if __name__ == "__main__":
    search: SearchStrategy = DepthFirstSearch()
    print(f"DFS route: {pretty_print_search(search.search(gatwick, heathrow))}\n")
    search = BreadthFirstSearch()
    print(f"BFS route: {pretty_print_search(search.search(gatwick, heathrow))}\n")
    search = DijkstrasAlgoSearch()
    print(
        f"Dijkstra's route (time-min): {pretty_print_search(search.search(gatwick, heathrow))}\n"
    )
    """
    Expected output with date set as 2025-03-10T14:12:00Z:

    DFS route: Gatwick segment taking 0.0 minutes M25 J12 segment taking 27.8 minutes M25 J13 segment taking 2.9 minutes A30 to Heathrow segment taking 4.0 minutes Heathrow segment taking 0.0 minutes. Total journey time: 34.7 minutes. Total distance: 29.8

    BFS route: Gatwick segment taking 0.0 minutes M25 J12 segment taking 27.8 minutes Local Roads to Heathrow segment taking 20.0 minutes Heathrow segment taking 0.0 minutes. Total journey time: 47.8 minutes. Total distance: 35

    Dijkstra's route (time-min): Gatwick segment taking 0.0 minutes M25 J12 segment taking 27.8 minutes M25 J13 segment taking 2.9 minutes M25 J14 to Heathrow segment taking 3.4 minutes Heathrow segment taking 0.0 minutes. Total journey time: 34.1 minutes. Total distance: 29
    """
