from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class trend_rank:
    direction: int
    delta: int

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "trend_rank":
        if data is None:
            return cls(direction=0, delta=0)  # default fallback
        return cls(
            direction=data.get("direction", 0),
            delta=data.get("delta", 0),
        )