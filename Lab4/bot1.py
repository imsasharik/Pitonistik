import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

users_stats = {}

CHOICES = ["камень", "ножницы", "бумага"]

EMOJIS = {
    "камень": "🪨",
    "ножницы": "✂️",
    "бумага": "📜"
}

WINNING_COMBINATIONS = {
    "камень": "ножницы",
    "бумага": "камень",
    "ножницы": "бумага"
}


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    message = f"Привет, {user.first_name}! Я бот для игры \"Камень, ножницы, бумага\"."
    keyboard = [
        [InlineKeyboardButton("Играть 🎲", callback_data="play")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)


def play_game(update: Update, context: CallbackContext) -> None:
    chat_id = update.callback_query.from_user.id
    buttons = [
        [InlineKeyboardButton(choice, callback_data=f"choice:{choice}") for choice in CHOICES]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(
        text="Выберите ваш ход:",
        reply_markup=reply_markup
    )


def process_choice(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_choice = query.data.split(":")[1]
    bot_choice = random.choice(CHOICES)
    chat_id = query.from_user.id

    if WINNING_COMBINATIONS[user_choice] == bot_choice:
        result = "Вы победили!"
        outcome = "win"
    elif WINNING_COMBINATIONS[bot_choice] == user_choice:
        result = "Вы проиграли..."
        outcome = "loss"
    else:
        result = "Ничья!"
        outcome = "draw"

    response = (
        f"Ваш ход: {user_choice} {EMOJIS.get(user_choice)}\n"
        f"Мой ход: {bot_choice} {EMOJIS.get(bot_choice)}\n\n"
        f"{result}"
    )

    stats = users_stats.setdefault(chat_id, {"wins": 0, "losses": 0, "draws": 0})
    if outcome == "win":
        stats["wins"] += 1
    elif outcome == "loss":
        stats["losses"] += 1
    else:
        stats["draws"] += 1

    query.answer()
    query.edit_message_text(response)


def show_stats(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    stats = users_stats.get(user_id, {"wins": 0, "losses": 0, "draws": 0})
    wins = stats["wins"]
    losses = stats["losses"]
    draws = stats["draws"]

    response = (
        f"Ваша статистика:\n"
        f"Побед: {wins}\n"
        f"Поражений: {losses}\n"
        f"Ничьих: {draws}"
    )
    update.message.reply_text(response)


def main(token):
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(play_game, pattern=r'^play'))
    dispatcher.add_handler(CallbackQueryHandler(process_choice, pattern=r'^choice:.+$'))
    dispatcher.add_handler(CommandHandler("stats", show_stats))

    updater.start_polling()
    updater.idle()


TOKEN = "7911426244:AAGHVZR9l1pbGvSZXzQLF0GfcNyn8x1cQyE"

if __name__ == '__main__':
    main(TOKEN)