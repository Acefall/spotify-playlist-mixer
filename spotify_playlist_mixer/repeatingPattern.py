class RepeatingPattern:
    """Provides an infinite loop iterator to a list.
    """

    def __init__(self, pattern: list):
        self.pattern = pattern

    def __iter__(self):
        self.cursor = -1
        return self

    def __next__(self):
        self.cursor = (self.cursor + 1) % len(self.pattern)
        return self.pattern[self.cursor]
