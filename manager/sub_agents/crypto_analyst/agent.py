from datetime import datetime
import requests
from google.adk.agents import Agent

# Common crypto symbol → CoinGecko ID
COINGECKO_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "DOGE": "dogecoin",
    "ADA": "cardano",
    "XRP": "ripple",
    "DOT": "polkadot",
    "AVAX": "avalanche-2",
    "MATIC": "matic-network",
}

def get_crypto_price(symbol: str) -> dict:
    """Retrieves current crypto price using CoinGecko."""
    print(f"--- Tool: get_crypto_price called for {symbol} ---")

    try:
        symbol_upper = symbol.upper()

        # Convert ticker to CoinGecko ID
        cg_id = COINGECKO_MAP.get(symbol_upper)

        if cg_id is None:
            return {
                "status": "error",
                "error_message": f"Unsupported symbol: {symbol}. Try BTC, ETH, SOL, etc."
            }

        # Call CoinGecko API
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={cg_id}&vs_currencies=usd"
        response = requests.get(url).json()

        if cg_id not in response:
            return {
                "status": "error",
                "error_message": f"Could not fetch price for {symbol}. CoinGecko returned no data."
            }

        price = response[cg_id]["usd"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "status": "success",
            "symbol": symbol_upper,
            "price": price,
            "timestamp": timestamp,
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching crypto price: {str(e)}",
        }

crypto_analyst = Agent(
    name="crypto_analyst",
    model='gemini-2.5-flash',
    description="Tracks crypto prices like BTC, ETH, SOL, etc.",
    instruction="""
    You are a crypto price assistant.

    When the user asks for a crypto price:
    1. Use get_crypto_price to fetch the latest value.
    2. Return a clear summary including symbol, price, and timestamp.
    3. If the crypto price cannot be fetched, inform the user.
    
    Example:
    "BTC: $42,520 (updated 2025-01-10 12:10:00)"
    """,
    tools=[get_crypto_price],
)
