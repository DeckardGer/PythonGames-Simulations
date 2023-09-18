from this import d
from Object import Object

class Levels:
    def __init__(self):
        self.level = 0
        
    def getNextLevel(self):
        self.level += 1
        return self.loadLevel(self.level)
    
    def loadLevel(self, levelID):
        level = [
            Object((-5, 0), (5, 20)),
            Object((0, -5), (36, 5)),
            Object((36, 0), (5, 20)),
            Object((0, 20), (36, 5))
        ]
        
        if levelID == 1:
            level.append(Object((16, 0), (4, 4)))
            level.append(Object((16, 8), (4, 4)))
            level.append(Object((16, 16), (4, 4)))
        elif levelID == 2:
            pass
        
        return level