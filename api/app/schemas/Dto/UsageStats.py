from typing import Dict, Optional, Any


class UsageStats:
    def __init__(self):
        self.model_id: Optional[str] = None
        self.input_tokens: int = 0
        self.output_tokens: int = 0
        self.estimated_cost: float = 0.0
        self.latency_ms: int = 0

    def populate(self, model_id: str, input_tokens: int, output_tokens: int, cost: float, latency: int):
        self.model_id = model_id
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.estimated_cost = cost
        self.latency_ms = latency

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "estimated_cost": round(self.estimated_cost, 6),
            "latency_ms": self.latency_ms
        }