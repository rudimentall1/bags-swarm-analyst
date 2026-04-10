import tweepy
import time
from agents.swarm_orchestrator import SwarmOrchestrator

# Twitter API credentials (замени на свои)
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR_ACCESS_TOKEN_SECRET"

# Инициализация
orchestrator = SwarmOrchestrator(num_agents=3)
orchestrator.start_agents()

def get_tweet_text():
    consensus = orchestrator.get_consensus()
    if not consensus:
        return None
    
    best = consensus[0]
    tweet = f"🐝 Bags Swarm Analyst\n\n"
    tweet += f"🏆 Best token: {best['name']} (${best['symbol']})\n"
    tweet += f"💰 Price: ${best['price']}\n"
    tweet += f"📈 24h Change: {best['change']}%\n"
    tweet += f"🤖 Swarm consensus: {best['consensus_recommendation']} (score: {best['avg_score']:.1f})\n\n"
    tweet += f"#BagsHackathon #SwarmAI #CryptoSignals"
    return tweet

def post_tweet():
    try:
        auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        
        tweet = get_tweet_text()
        if tweet:
            api.update_status(tweet)
            print(f"[TWITTER] Posted: {tweet[:50]}...")
    except Exception as e:
        print(f"[TWITTER] Error: {e}")

if __name__ == "__main__":
    print("[TWITTER] Bot started. Posting every 6 hours...")
    while True:
        post_tweet()
        time.sleep(21600)  # 6 часов
