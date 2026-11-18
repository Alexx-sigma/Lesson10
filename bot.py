"""Telegram entry point. Requires BOT_TOKEN in local .env."""
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import ai
import db
from parser import parse_item_line

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def start_text() -> str:
    return "Привет! Я бот-список покупок с бюджетом. Напиши /help, чтобы узнать команды."


def help_text() -> str:
    return (
        "Команды: /start — приветствие; /help — справка; "
        "/add Название Цена — добавить товар (например: /add Чай 100); "
        "/list — показать список; /total — сумма; /clear — очистить список; "
        "/ask вопрос — демо-ответ ИИ."
    )


def fmt_price(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:.2f}"


def format_list(items: list[dict]) -> str:
    if not items:
        return "Список пуст. Добавьте товар: /add Чай 100"
    lines = [f"{i}. {it['name']} — {fmt_price(it['price'])}" for i, it in enumerate(items, 1)]
    return "\n".join(lines)


def format_total(total: float) -> str:
    return f"Итого: {fmt_price(total)}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(start_text())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(help_text())


def _user_id(update: Update) -> int | None:
    return update.effective_user.id if update.effective_user else None


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid, msg = _user_id(update), update.effective_message
    if uid is None or msg is None:
        return
    item = parse_item_line(" ".join(context.args or []))
    if item is None:
        await msg.reply_text("Формат: /add Название Цена, например /add Чай 100")
        return
    db.add_item(uid, item["name"], item["price"])
    await msg.reply_text(f"Добавлено: {item['name']} — {fmt_price(item['price'])}")


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid, msg = _user_id(update), update.effective_message
    if uid is not None and msg is not None:
        await msg.reply_text(format_list(db.list_items(uid)))


async def total_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid, msg = _user_id(update), update.effective_message
    if uid is not None and msg is not None:
        await msg.reply_text(format_total(db.total_price(uid)))


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid, msg = _user_id(update), update.effective_message
    if uid is not None and msg is not None:
        removed = db.clear_items(uid)
        await msg.reply_text(f"Список очищен (удалено: {removed}).")


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    if msg is None:
        return
    try:
        await msg.reply_text(ai.generate_reply(" ".join(context.args or [])))
    except ValueError:
        await msg.reply_text("Напишите вопрос после команды: /ask что купить к чаю?")


def main() -> None:
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token or token == "PASTE_YOUR_TOKEN_HERE":
        raise RuntimeError("Укажите настоящий BOT_TOKEN в локальном файле .env (не коммитьте его)")
    db.init_db()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add_command))
    app.add_handler(CommandHandler("list", list_command))
    app.add_handler(CommandHandler("total", total_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("ask", ask_command))
    logger.info("Starting Telegram bot")
    app.run_polling()


if __name__ == "__main__":
    main()
