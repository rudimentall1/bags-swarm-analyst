from flask import Flask, render_template, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.swarm_orchestrator import SwarmOrchestrator

app = Flask(__name__)
orchestrator = SwarmOrchestrator(num_agents=3)
orchestrator.start_agents()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/consensus')
def api_consensus():
    consensus = orchestrator.get_consensus()
    if consensus:
        return jsonify(consensus)
    return jsonify([])

@app.route('/api/agents')
def api_agents():
    agents_data = []
    for i, agent in enumerate(orchestrator.agents):
        if agent.opinion:
            best = agent.opinion[0]
            agents_data.append({
                "id": agent.agent_id,
                "best_token": best["symbol"],
                "score": round(best["score"], 1),
                "recommendation": best["recommendation"]
            })
    return jsonify(agents_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
