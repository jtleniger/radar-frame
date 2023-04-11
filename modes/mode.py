from datetime import timedelta
from enum import Enum, auto

from modes import storm, clear

class Mode(Enum):
    Storm = auto()
    Clear = auto()

    def run(self, state, config):
        if self is Mode.Storm:
            storm.run(state, config)
            return
        
        if self is Mode.Clear:
            clear.run(state, config)
            return
        
        raise Exception('unexpected mode')
    
    def interval(self) -> timedelta:
        if self is Mode.Storm:
            return timedelta(minutes=10)
        
        if self is Mode.Clear:
            return timedelta(minutes=30)

        raise Exception('unexpected mode')