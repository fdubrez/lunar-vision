from enum import IntEnum
from typing import Dict

from pydantic import BaseModel


class LanderStatus(IntEnum):
    SPAWNED = 0
    ALIVE = 1
    LANDED = 2
    DEAD = 3

    def __repr__(self):
        return self.name

class LanderData(BaseModel):
    name: str
    vx: float
    vy: float
    angle: float
    altitude: float
    usedFuel: int
    status: LanderStatus

class LanderRotation(IntEnum):
    CLOCKWISE = 0
    COUNTERCLOCKWISE = 1
    NONE = 2

class LanderAction(BaseModel):
    thrust: bool
    rotate: LanderRotation

    def export(self) -> Dict:
        return {"thrust": self.thrust, "rotate": self.rotate.value}