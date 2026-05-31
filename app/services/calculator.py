from app.models.schemas import Trade


def format_duration(seconds: float) -> str:
    """Format duration seconds into the most human-readable unit.

    Scales automatically from milliseconds to months.
    - Under 1 second:  milliseconds  (algo/HFT trades)
    - Under 60 seconds: seconds      (scalpers)
    - Under 3600 seconds: minutes    (day traders)
    - Under 86400 seconds: hours     (intraday swing)
    - Under 2592000 seconds: days    (short swing)
    - 2592000 and above: weeks/months (long swing)
    """
    if seconds < 1:
        ms = round(seconds * 1000, 1)
        return f"{ms}ms"
    elif seconds < 60:
        return f"{round(seconds, 1)}s"
    elif seconds < 3600:
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m}m {s}s"
    elif seconds < 86400:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        return f"{h}h {m}m"
    elif seconds < 2592000:
        d = int(seconds // 86400)
        h = int((seconds % 86400) // 3600)
        return f"{d}d {h}h"
    else:
        weeks = round(seconds / 604800, 1)
        return f"{weeks} weeks"


def calculate_metrics(trades: list[Trade]) -> dict:
    """Calculate performance metrics from a list of normalized Trade objects.

    Returns a dictionary of trading statistics based on net PnL.
    """
    if not trades:
        return {"error": "No trades provided"}

    total_trades = len(trades)
    winners = [t for t in trades if t.is_winner]
    losers = [t for t in trades if not t.is_winner]

    winning_trades = len(winners)
    losing_trades = len(losers)

    win_rate = round((winning_trades / total_trades) * 100, 2)

    total_net_pnl = round(sum(t.net_pnl for t in trades), 2)
    total_fees = round(sum(t.fees + t.commissions for t in trades), 2)

    avg_winner = round(sum(t.net_pnl for t in winners) / winning_trades, 2) if winners else 0
    avg_loser = round(sum(t.net_pnl for t in losers) / losing_trades, 2) if losers else 0

    gross_wins = sum(t.net_pnl for t in winners)
    gross_losses = abs(sum(t.net_pnl for t in losers))
    profit_factor = round(gross_wins / gross_losses, 2) if gross_losses > 0 else 0

    # Max drawdown — largest peak to trough drop in cumulative net PnL
    peak = 0
    max_drawdown = 0
    cumulative = 0
    for t in trades:
        cumulative += t.net_pnl
        if cumulative > peak:
            peak = cumulative
        drawdown = peak - cumulative
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    max_drawdown = round(max_drawdown, 2)

    # Average hold time formatted to most readable unit
    avg_seconds = sum(t.duration_seconds for t in trades) / total_trades
    avg_hold_time = format_duration(avg_seconds)

    return {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": win_rate,
        "total_net_pnl": total_net_pnl,
        "total_fees_paid": total_fees,
        "profit_factor": profit_factor,
        "avg_winner": avg_winner,
        "avg_loser": avg_loser,
        "max_drawdown": max_drawdown,
        "avg_hold_time": avg_hold_time,

        # TODO v2: points caught requires contract tick multiplier per instrument
        # TODO v2: (MES = $5/point, MNQ = $2/point, MGC = $10/point, etc.)
        # TODO v2: add RR when stop loss data is available via journaling
        # TODO v2: add daily breakdown metrics
        # TODO v2: add per-contract breakdown
    }