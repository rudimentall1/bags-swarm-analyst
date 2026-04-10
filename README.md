# Bags Swarm Analyst

P2P swarm of AI agents analyzing creator tokens on Bags platform. 3 independent agents reach consensus on BUY/HOLD/SELL recommendations.

## Features

- 3 AI agents with independent scoring algorithms
- Swarm consensus mechanism (majority vote)
- Real-time web dashboard with live updates
- Telegram bot with commands: /best_token, /analyze, /agents
- Mock data integration (ready for real Bags API)

## Live Demo

## Demo Video

[https://youtu.be/-KjBGF13DKw](https://www.youtube.com/watch?v=VsWcIVbkeQQ)
- **Web Dashboard:** http://212.113.107.0:5001
- **Telegram Bot:** @bags_swarm_analyst_bot

## Tech Stack

- Python 3.10+
- Flask (web dashboard)
- python-telegram-bot
- Multi-agent architecture with P2P consensus

## Commands

| Command | Description |
|---------|-------------|
| `/best_token` | Best token by swarm consensus |
| `/analyze` | Full swarm analysis |
| `/agents` | Each agent's opinion |
| `/token <symbol>` | Info about specific token |

## Installation

```bash
git clone https://github.com/rudimentall1/bags-swarm-analyst.git
cd bags-swarm-analyst
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python bot_swarm.py
bags-swarm-analyst/
├── agents/
│   ├── __init__.py
│   ├── analyst_agent.py      # Individual AI agent
│   └── swarm_orchestrator.py # P2P consensus
├── web/
│   ├── app.py                # Flask dashboard
│   └── templates/
│       └── index.html
├── bags_mock_data.py         # Mock Bags API data
├── bot_swarm.py              # Telegram bot
├── twitter_bot.py            # Twitter bot (optional)
└── requirements.txt

## Token

- **Name:** Bags Swarm Token
- **Symbol:** BST
- **Address:** `4ofVjw56C5mFvJ9js3Qy6y8ro4DveZCkYaUU6a4JpV3a`
- **Network:** Solana Devnet
- **Decimals:** 9
- **Total Supply:** 1,000,000 BST

License
MIT

Author
Rinat (@rudimentall1)
