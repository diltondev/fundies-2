def log_spawn(func):
    """Decorator that logs each call to spawn() on a SpawnPoint.

    Prints: [LOG] <spawn_point_name>: Spawning <pokemon_name>
    """

    def wrapper(self, *args, **kwargs):
        print(f"[LOG] {self.name}: Spawning {args[0]}")
        # print(f'Self: {self}, Args: {args}, Kwargs: {kwargs}')
        return func(self, *args, **kwargs)

    return wrapper
