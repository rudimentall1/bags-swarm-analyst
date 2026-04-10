import time
import threading
import json
import random

class AnalystAgent:
    def __init__(self, agent_id, api_key=None):
        self.agent_id = agent_id
        self.api_key = api_key
        self.opinion = None
        self.running = True

    def analyze(self, tokens_data):
        if not tokens_data:
            return None
        
        analyzed = []
        for token in tokens_data:
            score = self.calculate_score(token)
            analyzed.append({
                "name": token["name"],
                "symbol": token["symbol"],
                "price": token["price"],
                "volume": token["volume_24h"],
                "change": token["price_change_24h"],
                "score": score,
                "recommendation": "BUY" if score > 70 else "HOLD" if score > 40 else "SELL"
            })
        
        analyzed.sort(key=lambda x: x["score"], reverse=True)
        self.opinion = analyzed
        return analyzed

    def calculate_score(self, token):
        score = 0
        if token["price_change_24h"] > 0:
            score += min(50, token["price_change_24h"] * 2)
        else:
            score += max(0, 50 + token["price_change_24h"] * 2)
        
        volume_score = min(30, token["volume_24h"] / 5000)
        score += volume_score
        score += random.randint(0, 20)
        
        return min(100, max(0, score))

    def get_best_token(self):
        if not self.opinion:
            return None
        return self.opinion[0]

    def start(self, data_callback, interval=30):
        def loop():
            while self.running:
                tokens_data = data_callback()
                if tokens_data:
                    self.analyze(tokens_data)
                time.sleep(interval)
        threading.Thread(target=loop, daemon=True).start()

    def stop(self):
        self.running = False
