from app.services.parser import parse_csv
from app.services.calculator import calculate_metrics

print("=== YOUR REAL DATA ===")
with open("trades_export__2_.csv", "rb") as f:
    trades = parse_csv(f.read())
metrics = calculate_metrics(trades)
for key, value in metrics.items():
    print(f"{key}: {value}")

print("\n=== TEST DATASET ===")
with open("test_trades.csv", "rb") as f:
    trades = parse_csv(f.read())
metrics = calculate_metrics(trades)
for key, value in metrics.items():
    print(f"{key}: {value}")