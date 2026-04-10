import threading
import time
from .analyst_agent import AnalystAgent
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from bags_mock_data import get_popular_tokens

class SwarmOrchestrator:
    def __init__(self, num_agents=3):
        self.agents = []
        self.consensus = None
        self.running = True
        
        for i in range(num_agents):
            agent = AnalystAgent(f"analyst_{i+1}")
            self.agents.append(agent)
    
    def get_tokens_data(self):
        return get_popular_tokens()
    
    def start_agents(self):
        for agent in self.agents:
            agent.start(self.get_tokens_data, interval=30)
    
    def get_consensus(self):
        opinions = []
        for agent in self.agents:
            if agent.opinion:
                opinions.append(agent.opinion)
        
        if not opinions:
            return None
        
        consensus = {}
        for opinion in opinions:
            for token in opinion:
                symbol = token["symbol"]
                if symbol not in consensus:
                    consensus[symbol] = {
                        "scores": [],
                        "recommendations": [],
                        "token_info": token
                    }
                consensus[symbol]["scores"].append(token["score"])
                consensus[symbol]["recommendations"].append(token["recommendation"])
        
        result = []
        for symbol, data in consensus.items():
            avg_score = sum(data["scores"]) / len(data["scores"])
            rec = max(set(data["recommendations"]), key=data["recommendations"].count)
            result.append({
                "symbol": symbol,
                "name": data["token_info"]["name"],
                "price": data["token_info"]["price"],
                "volume": data["token_info"]["volume"],
                "change": data["token_info"]["change"],
                "avg_score": avg_score,
                "consensus_recommendation": rec,
                "agents_count": len(data["scores"])
            })
        
        result.sort(key=lambda x: x["avg_score"], reverse=True)
        self.consensus = result
        return result
    
    def get_best_consensus(self):
        if not self.consensus:
            self.get_consensus()
        if self.consensus:
            return self.consensus[0]
        return None
    
    def start_consensus_loop(self, callback, interval=30):
        def loop():
            while self.running:
                consensus = self.get_consensus()
                if consensus and callback:
                    callback(consensus)
                time.sleep(interval)
        threading.Thread(target=loop, daemon=True).start()
