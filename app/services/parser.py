import csv
import io
from datetime import datetime, timezone
from app.models.schemas import Trade


def parse_duration(duration_str: str) -> int:
    """Convert TradeDuration string to total seconds.

    Example input: '00:01:14.1020610'
    """
    try:
        if "." in duration_str:
            duration_str = duration_str.split(".")[0]
        parts = duration_str.split(":")
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return (hours * 3600) + (minutes * 60) + seconds
    except Exception:
        return 0


def parse_timestamp(ts_str: str) -> datetime:
    """Parse Topstep timestamp string to UTC datetime.

    Example input: '05/28/2026 18:30:01 -07:00'
    """
    # TODO v2: accept user timezone preference for display formatting
    # TODO v2: tag trades by NYSE session (pre-market, regular, after-hours)
    # TODO v2: flag trades outside NYSE calendar as weekend/holiday trades
    ts_str = ts_str.strip()
    dt = datetime.strptime(ts_str, "%m/%d/%Y %H:%M:%S %z")
    return dt.astimezone(timezone.utc)


def parse_csv(file_bytes: bytes) -> list[Trade]:
    """Parse a Topstep CSV export into a list of normalized Trade objects.

    Handles BOM character, timezone normalization, and net PnL calculation.
    """
    content = file_bytes.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))

    trades = []

    for row in reader:
        try:
            gross_pnl = float(row["PnL"])
            fees = float(row["Fees"])
            commissions = float(row["Commissions"])
            net_pnl = gross_pnl - fees - commissions

            trade = Trade(
                id=int(row["Id"]),
                contract=row["ContractName"].strip(),
                entered_at=parse_timestamp(row["EnteredAt"]),
                exited_at=parse_timestamp(row["ExitedAt"]),
                entry_price=float(row["EntryPrice"]),
                exit_price=float(row["ExitPrice"]),
                fees=fees,
                commissions=commissions,
                gross_pnl=gross_pnl,
                net_pnl=round(net_pnl, 2),
                size=int(row["Size"]),
                direction=row["Type"].strip(),
                trade_day=row["TradeDay"].strip()[:10],
                duration_seconds=parse_duration(row["TradeDuration"]),
                is_winner=net_pnl > 0
            )
            trades.append(trade)

        except Exception as e:
            # TODO v2: return partial errors instead of silently skipping
            print(f"Skipping row {row.get('Id', 'unknown')}: {e}")
            continue

    return trades
