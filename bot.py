import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from swarm_analyst import SwarmAnalyst

BOT_TOKEN = "8766320286:AAEqCdfpHSgmHgyzesDjkgSJghZBp777370"

analyst = SwarmAnalyst()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bags Swarm Analyst\n\n"
        "Commands:\n"
        "/best_token - show best token to buy\n"
        "/analyze - analyze all tokens\n"
        "/token <symbol> - info about specific token"
    )

async def best_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    best = analyst.get_best_opportunity()
    if best:
        msg = f"🏆 Best token:\n"
        msg += f"Name: {best['name']} (${best['symbol']})\n"
        msg += f"Price: ${best['price']}\n"
        msg += f"24h Volume: ${best['volume_24h']:,}\n"
        msg += f"Change: {best['price_change_24h']}%"
    else:
        msg = "No data"
    await update.message.reply_text(msg)

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tokens = analyst.analyze()
    msg = "📊 Top 3 tokens by volume:\n\n"
    for t in tokens:
        msg += f"• {t['name']} (${t['symbol']}): ${t['price']} | Δ{t['price_change_24h']}% | Vol: ${t['volume_24h']:,}\n"
    await update.message.reply_text(msg)

async def token_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /token <symbol> (e.g., /token AITR)")
        return
    symbol = context.args[0].upper()
    token = analyst.get_token_info(symbol)
    if token:
        msg = f"📈 Token {token['name']} (${token['symbol']})\n"
        msg += f"Price: ${token['price']}\n"
        msg += f"24h Volume: ${token['volume_24h']:,}\n"
        msg += f"Change: {token['price_change_24h']}%"
    else:
        msg = f"Token {symbol} not found"
    await update.message.reply_text(msg)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("best_token", best_token))
    app.add_handler(CommandHandler("analyze", analyze))
    app.add_handler(CommandHandler("token", token_info))
    app.run_polling()

if __name__ == "__main__":
    main()
