import random


class LootTable:
    def __init__(self, *entries):
        assert len(entries) % 2 == 0, "Must be in format (item1, weight1, item2, weight2...)"
        
        self.entries = {
            entries[i * 2]: entries[i * 2 + 1]
            for i in range(round(len(entries) / 2))
        }
        
        top = sum(self.entries.values())
        self.entries = {
            k: v / top
            for (k, v) in self.entries.items()
        }
    
    def drop(self, r=None):
        if r is None:
            r = random.random()
        tail = 0
        for (k, v) in self.entries.items():
            if tail <= r < tail + v:
                return k
            tail += v
        return list(self.entries.keys())[-1]
