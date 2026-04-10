import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from agents.swarm_orchestrator import SwarmOrchestrator

BOT_TOKEN = "8766320286:AAEqCdfpHSgmHgyzesDjkgSJghZBp777370"

orchestrator = SwarmOrchestrator(num_agents=3)
orchestrator.start_agents()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐝 Bags Swarm Analyst (P2P)\n\n"
        "3 AI agents analyze tokens and reach consensus.\n\n"
        "Commands:\n"
        "/best_token - show best token by swarm consensus\n"
        "/analyze - show full swarm analysis\n"
        "/agents - show each agent's opinion\n"
        "/token <symbol> - info about specific token"
    )

async def best_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    best = orchestrator.get_best_consensus()
    if best:
        msg = f"🏆 Swarm Consensus: Best token\n"
        msg += f"Name: {best['name']} (${best['symbol']})\n"
        msg += f"Price: ${best['price']}\n"
        msg += f"24h Volume: ${best['volume']:,}\n"
        msg += f"Change: {best['change']}%\n"
        msg += f"Consensus: {best['consensus_recommendation']} (score: {best['avg_score']:.1f})"
    else:
        msg = "No data yet"
    await update.message.reply_text(msg)

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    consensus = orchestrator.get_consensus()
    if consensus:
        msg = "📊 Swarm Consensus Analysis:\n\n"
        for token in consensus[:5]:
            msg += f"• {token['name']} (${token['symbol']}): {token['consensus_recommendation']} "
            msg += f"(score: {token['avg_score']:.1f}) | Δ{token['change']}%\n"
    else:
        msg = "No data yet"
    await update.message.reply_text(msg)

async def agents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🤖 Agent Opinions:\n\n"
    for i, agent in enumerate(orchestrator.agents):
        if agent.opinion and len(agent.opinion) > 0:
            best = agent.opinion[0]
            msg += f"Agent {i+1}: {best['name']} (${best['symbol']}) - {best['recommendation']} "
            msg += f"(score: {best['score']:.1f})\n"
        else:
            msg += f"Agent {i+1}: analyzing...\n"
    await update.message.reply_text(msg)

async def token_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /token <symbol> (e.g., /token AITR)")
        return
    symbol = context.args[0].upper()
    
    # Ищем в консенсусе
    consensus = orchestrator.get_consensus()
    if consensus:
        for token in consensus:
            if token['symbol'] == symbol:
                msg = f"📈 Token {token['name']} (${token['symbol']})\n"
                msg += f"Price: ${token['price']}\n"
                msg += f"24h Volume: ${token['volume']:,}\n"
                msg += f"Change: {token['change']}%\n"
                msg += f"Consensus: {token['consensus_recommendation']} (score: {token['avg_score']:.1f})"
                await update.message.reply_text(msg)
                return
    
    # Если не нашли
    await update.message.reply_text(f"Token {symbol} not found in current analysis")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("best_token", best_token))
    app.add_handler(CommandHandler("analyze", analyze))
    app.add_handler(CommandHandler("agents", agents))
    app.add_handler(CommandHandler("token", token_info))
    print("🐝 Swarm Analyst Bot started! 3 agents are analyzing...")
    app.run_polling()

if __name__ == "__main__":
    main()
