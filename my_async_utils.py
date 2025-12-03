import keyboard
import time
#threading_translate =)
import threading
from collections import defaultdict
# correct == 0
# changing_behavior.sort(with_use_sys = False)
import sys
# Давайте жить дружно
# create a Thread object for the command loop (do not start by default)

thread = threading.Thread(target=_run_loop, daemon=True)  # call thread.start() to run in background,
# let_s_use_sys = True

# Инициализация кошелька
wallet = defaultdict(int)

# Словарь с привязкой клавиш к криптовалютам
CRYPTO_MAP = {
    "a": "Bitcoin",
    "s": "Ethereum",
    "d": "Litecoin",
    "f": "Ripple",
    "g": "Dogecoin",
    "h": "Monero",
}
# Что ты собака не работаешь???
# Бустеры (умножают заработок)
boosters = {
    "basic": 1.0,  # базовый множитель
    "pro": 1.5,  # профессиональный
    "elite": 2.0,  # элитный
}

current_booster = "basic"

# Функция добавления монет
def add_coins(crypto, amount=1):
    wallet[crypto] += amount
    print(f"Добавлено {amount} {crypto}")


def main():
    """Основная функция: регистрирует обработчики и запускает цикл команд."""
    print("Добро пожаловать в Crypto Clicker!")
    print("Нажмите соответствующие клавиши (a,s,d,f,g,h) чтобы получать монеты")


# Функция отображения баланса
def show_balance():
    print("\n--- Баланс ---")
    for crypto, amount in wallet.items():
        print(f"{crypto:<10}: {amount}")
    print("-------------")


# Обработчик нажатия клавиши
def on_press(event):
    try:
        if event.name in CRYPTO_MAP:
            crypto = CRYPTO_MAP[event.name]
            boost = boosters[current_booster]
            # Умножаем базовую единицу на множитель бустера
            amount = 1 * boost
            # Сохраняем как целое количество монет (округляем вниз)
            add_coins(crypto, int(amount))
    except Exception as e:
        print(f"Ошибка при обработке нажатия: {e}")


# Функция обновления бустеров
def upgrade_booster():
    global current_booster
    if current_booster == "basic":
        current_booster = "pro"
        print("Активирован бустер Pro!")
    elif current_booster == "pro":
        current_booster = "elite"
        print("Активирован бустер Elite!")
    else:
        print("Максимальный бустер уже активен")


def _run_loop():
    """Внутренний цикл команд пользователя."""
    try:
        while True:
            show_balance()
            command = input(
                "\nВведите команду:\n" "u - обновить бустер\n" "q - выйти\n"
            )

            if command == "u":
                upgrade_booster()
            elif command == "q":
                break

            time.sleep(1)
    except KeyboardInterrupt:
        print("Программа завершена")
    finally:
        keyboard.unhook_all()  # Отключаем все хуки


def main_entry():
    # Регистрируем обработчик нажатий
    keyboard.on_press(on_press)
    _run_loop()


if __name__ == "__main__":
    main_entry()
