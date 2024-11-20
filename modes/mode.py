from datetime import timedelta
from enum import Enum, auto

from modes import storm, clear
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sources.forecast import ForecastProvider
    from state.state import State

class Mode(Enum):
    Storm = auto()
    Clear = auto()

    def run(self, state: "State", provider: "ForecastProvider"):
        if self is Mode.Storm:
            storm.run(state, provider)
            return
        
        if self is Mode.Clear:
            clear.run(provider)
            return
        
        raise Exception('unexpected mode')
    
    def interval(self) -> timedelta:
        if self is Mode.Storm:
            return timedelta(minutes=10)
        
        if self is Mode.Clear:
            return timedelta(minutes=30)

        raise Exception('unexpected mode')