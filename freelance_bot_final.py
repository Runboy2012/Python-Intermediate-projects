from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import json
import os

TOKEN = "7639593664:AAEEhJEy5BTOt827KRUsKh2LsmXBacOEY-E"
SAVE_FILE = "save.json"

ORDERS = [
    ("5 промптов MidJourney", 1500, 15, "prompt", 5),
    ("Парсер Excel", 5000, 40, "python", 10),
    ("10 Shorts", 12000, 80, "video", 18),
    ("Текст 3000 зн.", 3500, 25, "copy", 7),
    ("Баннер Canva", 2500, 20, "design", 6),
    ("Telegram-бот", 15000, 70, "python", 15),
]

def load():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    data = load()
    if uid not in data:
        data[uid] = {"day":1,"money":8000,"energy":100,"skills":{"prompt":10,"python":10,"video":5,"copy":10,"design":5},"order":None}
        save(data)
    context.user_data.update(data[uid])
    await menu(update, context)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = context.user_data
    if u["day"] > 30:
        await end(update, context); return

    text = f"День {u['day']}/30\nДенег: {u['money']} ₸\nЭнергия: {u['energy']}/100"
    if u["order"]:
        text += f"\n\nРаботаю: {u['order'][0]}"

    kb = [[InlineKeyboardButton("Биржа", callback_data="birzha")]]
    kb += [[InlineKeyboardButton("Готово!" if u["order"] else "Спать 8 ч", callback_data="finish" if u["order"] else "sleep")]]

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

async def btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    u = context.user_data

    if q.data == "birzha":
        orders = random.sample(ORDERS, 4)
        context.user_data["ords"] = orders
        kb = [[InlineKeyboardButton(f"{n} — {p}₸", callback_data=f"take_{i}")] for i,(n,p,_,_,_) in enumerate(orders)]
        kb += [[InlineKeyboardButton("Назад", callback_data="back")]]
        await q.edit_message_text("Заказы:", reply_markup=InlineKeyboardMarkup(kb))

    elif q.data.startswith("take_"):
        i = int(q.data.split("_")[1])
        u["order"] = context.user_data["ords"][i]
        save(load())
        await menu(update, context)

    elif q.data == "finish":
        o = u["order"]
        u["energy"] -= o[2]
        if random.randint(1,100) <= o[4]:
            res = "Кинули"
        else:
            u["money"] += o[1]
            u["skills"][o[3]] += random.randint(15,30)
            res = f"+{o[1]} ₸"
        u["order"] = None
        save(load())
        await q.edit_message_text(res)
        await menu(update, context)

    elif q.data == "sleep":
        u["day"] += 1
        u["energy"] = min(100, u["energy"] + random.randint(70,90))
        save(load())
        await menu(update, context)

    elif q.data == "back":
        await menu(update, context)

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = context.user_data["money"]
    txt = "ПОБЕДА!" if m >= 50000 else f"Поражение… {m} ₸"
    await update.callback_query.edit_message_text(txt)

if __name__ == "__main__":
    print("Фриланс-выживалка запущена! Играй в Telegram → /start")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(btn))
    app.run_polling()