from dataclasses import dataclass
from typing import Any, Dict

Url = str  # Placeholder, replace with proper type if needed

@dataclass
class trend_score:
    direction: int
    delta: int

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "trend_score":
        return cls(
            direction=data["direction"],
            delta=data["delta"]
        )

@dataclass
class trend_rank:
    direction: int
    delta: int

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "trend_rank":
        return cls(
            direction=data["direction"],
            delta=data["delta"]
        )

@dataclass
class playerData:
    player_id: str
    id: Url
    url: Url
    username: str
    score: int
    rank: int
    country: Url
    name: str
    status: str
    avatar: Url
    trend_score: trend_score
    trend_rank: trend_rank
    flair_code: str
    win_count: int
    loss_count: int
    draw_count: int

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "playerData":
        return cls(
            player_id=data["player_id"],
            id=data["@id"],
            url=data["url"],
            username=data["username"],
            score=data["score"],
            rank=data["rank"],
            country=data["country"],
            name=data["name"],
            status=data["status"],
            avatar=data["avatar"],
            trend_score=trend_score.from_json(data["trend_score"]),
            trend_rank=trend_rank.from_json(data["trend_rank"]),
            flair_code=data["flair_code"],
            win_count=data["win_count"],
            loss_count=data["loss_count"],
            draw_count=data["draw_count"],
        )