# Функция для демонстрации поведения дома (EN)
def behavior_at_home():
    meditation = False  # Флаг медитации
    work = True  # Флаг работы (должен быть определен)
    

    while work or meditation:
        nice = True  # Настроение
        if nice:
            print("I am nice")  # Если настроение хорошее
        elif meditation:
            print("I am meditating")  # Если медитируем
        else:
            print("I am angry")  # Если плохое настроение
        break  # Выход после одной итерации

# Функция для демонстрации поведения дома (RU)
def behavior_at_home_ru():
    god_mode_stable = True  # Режим бога
    
    # Перебираем виды деятельности
    for activity in ["общение", "звонки", "знакомства"]:
        if god_mode_stable:
            print(f"Я в режиме бога, когда занимаюсь {activity}")
        else:
            print(f"Я в обычном режиме, когда занимаюсь {activity}")

# Основная логика работы с источником
source = "AIR"

def materialize(source):
    return f"Материализованный объект из {source}"

# Логические проверки
need_for_cleaning_before_upgrade = source == "AIR"
some_source = "WATER"
need_for_protect_source = some_source == "WATER"

# Создание кошелька
wallet = {
    "USD": 100,
    "EUR": 50,
    "JPY": 10000
}

# Функция для работы с накоплениями
def work_on_wallet(wallet, multiplier=1.05):
    """
    Увеличивает все накопления в кошельке на заданный множитель
    :param wallet: словарь с накоплениями
    :param multiplier: множитель увеличения (по умолчанию 5%)
    """
    for currency in wallet:
        wallet[currency] = int(wallet[currency] * multiplier)
    print("Накопления увеличены!")

# Функция форматированного вывода кошелька
def formatted_print(wallet):
    print("\nКошелек:")
    print("--------")
    for currency, amount in wallet.items():
        print(f"{currency:<5} - {amount:>10}")
    print("--------")

# Основной цикл работы
work = True

try:
    while work:
        print("\n--- Новый рабочий цикл ---")
        formatted_print(wallet)
        work_on_wallet(wallet)
        
        # Добавляем паузу для наглядности
        import time
        time.sleep(2)  # пауза в 2 секунды
        
        # Возможность выхода из цикла
        user_input = input("\nНажмите 'q' для выхода или Enter для продолжения: ")
        if user_input.lower() == 'q':
            work = False
            print("Работа завершена.")
            
except KeyboardInterrupt:
    print("\nРабота прервана пользователем.")

finally:
    print("\nФинальное состояние кошелька:")
    formatted_print(wallet)
# 