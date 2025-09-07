from dataclasses import dataclass, field
from typing import Any, Dict, Optional

# Reuse one class for both trend_score and trend_rank since they share shape
@dataclass(frozen=True)
class TrendChange:
    direction: int = 0
    delta: int = 0

    @classmethod
    def from_json(cls, data: Optional[Dict[str, Any]]) -> "TrendChange":
        if not data:  # handles None or {}
            return cls()

        def to_int(v, default=0):
            try:
                return int(v)
            except (TypeError, ValueError):
                return default

        return cls(
            direction=to_int(data.get("direction"), 0),
            delta=to_int(data.get("delta"), 0),
        )


@dataclass
class PlayerData:
    player_id: str
    id: str
    url: str
    username: str
    score: int
    rank: int
    country: str
    name: Optional[str]
    status: str
    avatar: str
    trend_score: TrendChange = field(default_factory=TrendChange)
    trend_rank: TrendChange = field(default_factory=TrendChange)
    flair_code: str = ""
    win_count: int = 0
    loss_count: int = 0
    draw_count: int = 0

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "PlayerData":
        return cls(
            player_id=data["player_id"],
            id=data["@id"],
            url=data["url"],
            username=data["username"],
            score=int(data["score"]),
            rank=int(data["rank"]),
            country=data["country"],
            name=data.get("name"),
            status=data["status"],
            avatar=data["avatar"],
            trend_score=TrendChange.from_json(data.get("trend_score")),
            trend_rank=TrendChange.from_json(data.get("trend_rank")),
            flair_code=data["flair_code"],
            win_count=int(data["win_count"]),
            loss_count=int(data["loss_count"]),
            draw_count=int(data["draw_count"]),
        )
