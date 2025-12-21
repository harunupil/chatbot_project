import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "card_prices.csv"


def get_card_price(card_name: str) -> str:
    """
    Look up a card price from CSV.
    """

    df = pd.read_csv(CSV_PATH, sep=";")

    # Normalize headers
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    match = df[df["card_name"].str.lower().str.contains(card_name.lower())]

    if match.empty:
        return f"❌ Card '{card_name}' not found."

    row = match.iloc[0]

    return (
        f"🃏 **{row['card_name']}**\n\n"
        f"- Game: {row['game']}\n"
        f"- Condition: {row['condition']}\n"
        f"- Price: **{row['price']} {row['currency']}**"
    )
