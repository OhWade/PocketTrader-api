from app.services.parser import parse_csv

with open("trades_export__2_.csv", "rb") as f:
    file_bytes = f.read()

trades = parse_csv(file_bytes)

for trade in trades:
    print(f"{trade.contract} | {trade.direction} | gross: ${trade.gross_pnl} | net: ${trade.net_pnl} | winner: {trade.is_winner}")
