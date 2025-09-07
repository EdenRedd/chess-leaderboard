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

