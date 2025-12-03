# Инициализация переменных
wallet = {
    "USD": 100,
    "EUR": 50,
    "JPY": 10000
}

# Функция добавления 100 единиц к каждой валюте
def add_hundred_to_all(wallet):
    for currency in wallet:
        wallet[currency] += 100
    print("Добавлено по 100 единиц к каждой валюте!")

# Функция форматированного вывода кошелька
def formatted_print(wallet):
    print("\nКошелек:")
    print("--------")
    for currency, amount in wallet.items():
        print(f"{currency:<5} - {amount:>10}")
    print("--------")

# Бесконечный цикл с автоматическим добавлением
import time

try:
    print("Автоматическое накопление запущено!")
    print("Нажмите Ctrl+C для остановки.")
    
    while True:
        add_hundred_to_all(wallet)
        formatted_print(wallet)
        time.sleep(2)  # пауза в 2 секунды между добавлениями

except KeyboardInterrupt:
    print("\nРабота прервана пользователем.")

finally:
    print("\nФинальное состояние кошелька:")
    formatted_print(wallet)
