import time
import threading
from bags_mock_data import get_popular_tokens

class SwarmAnalyst:
    def __init__(self):
        self.tokens = []
        self.running = True

    def analyze(self):
        self.tokens = get_popular_tokens()
        self.tokens.sort(key=lambda x: x['volume_24h'], reverse=True)
        return self.tokens[:3]

    def get_best_opportunity(self):
        tokens = self.analyze()
        if not tokens:
            return None
        best = max(tokens, key=lambda x: x['price_change_24h'])
        return best

    def get_token_info(self, symbol):
        from bags_mock_data import get_token_by_symbol
        return get_token_by_symbol(symbol)

    def start_loop(self, callback, interval=30):
        def loop():
            while self.running:
                best = self.get_best_opportunity()
                if best:
                    callback(best)
                time.sleep(interval)
        threading.Thread(target=loop, daemon=True).start()
