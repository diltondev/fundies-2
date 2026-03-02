from observer import SpawnPoint, PlayerAlert, RareBroadcast
from strategy import SortByName, SortByDistance, SortByCP, NearbyList


def main() -> None:
    # Observer
    print("--- Pokémon spawning nearby ---\n")

    point = SpawnPoint("Town Square")
    point.subscribe(PlayerAlert("Ash"))
    point.subscribe(PlayerAlert("Gary"))
    point.subscribe(RareBroadcast())

    point.spawn("Rattata", cp=120, rarity="common", distance_km=0.1)
    point.spawn("Snorlax", cp=1800, rarity="uncommon", distance_km=0.8)
    point.spawn("Dragonite", cp=2800, rarity="rare", distance_km=0.3)
    point.spawn("Pidgey", cp=80, rarity="common", distance_km=0.5)
    point.spawn("Mewtwo", cp=4000, rarity="rare", distance_km=1.2)

    # Strategy
    print("\n--- Nearby Pokémon — sorted views ---\n")

    spawns = point.get_all()
    nearby = NearbyList(SortByName())

    print("By name:")
    for s in nearby.generate(spawns):
        print(f"- {s.name} {s.distance_km}km  CP {s.cp}")

    nearby.set_strategy(SortByDistance())
    print("\nBy distance (closest first):")
    for s in nearby.generate(spawns):
        print(f"-  {s.name} {s.distance_km}km  CP {s.cp}")

    nearby.set_strategy(SortByCP())
    print("\nBy CP (highest first):")
    for s in nearby.generate(spawns):
        print(f"-  {s.name} CP {s.cp}")


if __name__ == "__main__":
    main()
