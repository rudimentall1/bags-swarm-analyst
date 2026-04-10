import random

def get_popular_tokens():
    mock_tokens = [
        {"name": "Agent Elon", "symbol": "ELONAI", "price": 0.023, "volume_24h": 45000, "price_change_24h": 12.5},
        {"name": "Swarm Bot", "symbol": "SWRM", "price": 0.11, "volume_24h": 23000, "price_change_24h": -2.3},
        {"name": "Creator Coin", "symbol": "CR8", "price": 0.55, "volume_24h": 89000, "price_change_24h": 5.1},
        {"name": "AI Trader", "symbol": "AITR", "price": 0.007, "volume_24h": 120000, "price_change_24h": 25.0},
        {"name": "DePIN Node", "symbol": "NODE", "price": 1.25, "volume_24h": 15000, "price_change_24h": -1.0},
    ]
    for token in mock_tokens:
        token["price"] = round(token["price"] * random.uniform(0.95, 1.05), 4)
        token["volume_24h"] = int(token["volume_24h"] * random.uniform(0.8, 1.2))
    return mock_tokens

def get_token_by_symbol(symbol):
    tokens = get_popular_tokens()
    for token in tokens:
        if token['symbol'].lower() == symbol.lower():
            return token
    return None
