def log_spawn(func):
    """Decorator that logs each call to spawn() on a SpawnPoint.

    Prints: [LOG] <spawn_point_name>: Spawning <pokemon_name>
    """
    def wrapper(self, *args, **kwargs):
        # TODO: print a log line using self.name and args[0]
        pass
    return wrapper
