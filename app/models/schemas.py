from pydantic import BaseModel
from datetime import datetime


class Trade(BaseModel):
    """Normalized trade object — same structure regardless of data source."""
    id: int
    contract: str
    entered_at: datetime
    exited_at: datetime
    entry_price: float
    exit_price: float
    fees: float
    commissions: float
    gross_pnl: float
    net_pnl: float
    size: int
    direction: str
    trade_day: str
    duration_seconds: int
    is_winner: bool

    # TODO v2: add account_id when multi-account support is added
    # TODO v2: add contract multiplier for accurate tick value calculations
