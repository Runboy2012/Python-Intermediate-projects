# Q.py — ФИНАЛЬНАЯ РАБОЧАЯ ВЕРСИЯ (проверено 01.12.2025)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import json
import os

# ←←←←← ТВОЙ ТОКЕН ←←←←←
TOKEN = ""

DATA_FILE = "players.json"

ORDERS_POOL = [
    ("5 промптов MidJourney", 1500, 2, "prompt", 5),
    ("Парсер цен → Excel", 5000, 8, "python", 10),
    ("10 Shorts про финграмотность", 12000, 24, "video", 15),
    ("Текст 3000 зн.", 3500, 4, "copy", 8),
    ("Баннер в Canva", 2500, 3, "design", 7),
    ("Telegram-бот на Python", 15000, 20, "python", 12),
]

# ——— загрузка/сохранение прогресса ———
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ——— старт ———
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()

    if user_id not in data:
        data[user_id] = {
            "day": 1,
            "money": 8000,
            "energy": 100,
            "skills": {"prompt": 10, "python": 10, "video": 5, "copy": 10, "design": 5},
            "order": None
        }
        save_data(data)

    context.user_data.update(data[user_id])
    await main_menu(update, context)

# ——— главное меню ———
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = context.user_data
    if user["day"] > 30:
        await game_over(update, context)
        return

    text = f"🏠 Квартира грузчика\n📅 День {user['day']}/30\n💰 {user['money']} тг\n⚡ Энергия: {user['energy']}/100"
    if user["order"]:
        text += f"\n\n🔨 Работаю: {user['order'][0]}"

    kb = [[InlineKeyboardButton("🛒 Биржа заказов", callback_data="orders")]]
    if not user["order"]:
        kb += [[InlineKeyboardButton("⏭ Пропустить день", callback_data="skip")]]
    else:
        kb += [[InlineKeyboardButton("✅ Готово!", callback_data="finish")]]

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

# ——— обработка всех кнопок ———
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = context.user_data

    if query.data == "orders":
        orders = random.sample(ORDERS_POOL, 4)
        context.user_data["today_orders"] = orders
        kb = []
        for i, (name, price, _, _, _) in enumerate(orders):
            kb.append([InlineKeyboardButton(f"{name} — {price}тг", callback_data=f"view_{i}")])
        kb.append([InlineKeyboardButton("⬅ Назад", callback_data="back")])
        await query.edit_message_text("🛒 Доступные заказы:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("view_"):
        idx = int(query.data.split("_")[1])
        o = context.user_data["today_orders"][idx]
        name, price, hours, skill, scam = o
        text = f"{name}\n💰 {price} тг • ⏰ {hours} ч\nНавык {skill}: {user['skills'][skill]}"
        kb = [
            [InlineKeyboardButton("✅ Взять заказ", callback_data=f"take_{idx}")],
            [InlineKeyboardButton("⬅ Назад", callback_data="orders")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("take_"):
        idx = int(query.data.split("_")[1])
        user["order"] = context.user_data["today_orders"][idx]
        save_data(load_data())
        await main_menu(update, context)

    elif query.data == "finish":
        if not user.get("order"):
            await query.edit_message_text("Нет активного заказа!")
            return
        name, price, _, skill, scam = user["order"]
        user["energy"] = max(0, user["energy"] - random.randint(25, 45))
        if random.randint(1, 100) <= scam:
            result = "😭 Заказчик кинул! 0 тг"
        else:
            user["money"] += price
            user["skills"][skill] += random.randint(15, 30)
            result = f"🎉 Готово! +{price} тг"
        user["order"] = None
        save_data(load_data())
        await query.edit_message_text(result)
        await main_menu(update, context)

    elif query.data == "skip":
        user["day"] += 1
        user["energy"] = min(100, user["energy"] + 35)
