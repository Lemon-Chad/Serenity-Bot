from objects.items import Item
from typing import List


class Storage:
    items: List[Item]
    size: int
    name: str
    
    def __init__(self, name: str, size: int, *contents: List[Item]):
        self.items = list(contents)
        self.size = size
        self.name = name
        
    def take_index(self, index: int) -> Item:
        return self.items.pop(index)
        
    def take_item(self, item: Item) -> None:
        self.items.remove(item)
        
    def insert_item(self, item: Item) -> bool:
        if len(self.items) >= self.size:
            return False
        self.items.append(item)
        return True
