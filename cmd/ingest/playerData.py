from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

class Url(str):
    def __new__(cls, value):
        result = urlparse(value)
        if not all([result.scheme, result.netloc]):
            raise ValueError(f"Invalid URL: {value}")
        return str.__new__(cls, value)

@dataclass
class Player:
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
    trend_score: str #replace with data class
    trend_rank: str #replace with data class
    flair_code: str
    win_count: int
    loss_count: int
    draw_count: int






