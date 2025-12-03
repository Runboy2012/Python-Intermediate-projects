from sentence_transformers import SentenceTransformer, util
from sympy import python
from sentence_transformers import SentenceTransformer model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2') # загрузка предобученной модели emb = model.encode(['Привет, как дела?', 'Это тестовое предложение.']) print(emb.shape) # должно быть (2, 384) - два предложения, 384 измерений
emb = model.encode([я устал, я хочу молчать]) print(emb.shape) # должно быть (2, 384) - два предложения, 384 измерений
# Напишем функцию для работы с историей воспоминаний персонажа.
def is_negative(memory):
    """Проверяет, является ли воспоминание негативным."""
    negative_keywords = [
        "sad", "angry", "fear", "hate", "bad", "trauma", "pain", "negative", "stupid", "error"
    ]
    # Сначала проверим, есть ли в памяти явные признаки негатива.
    if isinstance(memory, dict):
        for key, value in memory.items():
            if key == "sentiment" and value in ["sad", "angry", "fear", "hate", "bad", "trauma", "pain", "negative"]:
                return True
            if key == "negative" and value is True:
                return True
    # Если явных признаков нет, проверим текстовое представление памяти.
    memory_str = str(memory).lower()
    for keyword in negative_keywords:
        if keyword in memory_str:
            return True
    return False # Если ничего не найдено, считаем память не-негативной.
# Теперь создадим список негативных воспоминаний и удалим их из памяти персонажа. Это будет полезно для улучшения эмоционального состояния персонажа.
# Зададим переменную-имя списка негативных воспоминаний.
negative_examples = [
    "sad memory", "angry incident", "fearful event", "hate experience",
    "bad time", "trauma episode", "painful moment", "negative thought", "stupid error"
]
# Преобразуем их в словари для извлечения выводов и обработаем все пункты списка.
negative_memories = [{"sentiment": "sad"}, {"sentiment": "angry"}, {"sentiment": "fear"},
                    {"sentiment": "hate"}, {"sentiment": "bad"},
                    {"sentiment": "trauma"}, {"sentiment": "pain"},
                    {"sentiment": "negative"}, {"description": "stupid error", "negative": True}]
# Создадим психологическое оружие для борьбы с багами и мелкими неприятностями и в коде и в жизни персонажа. Для этого нам потребуется функция с именем напоминающим вибросигнал смартфона и срабатывающая после восприятия мысли о баге или неприятности.
# Мне запрещено просить помощи у других ИИ, но я могу использовать свои которому я ещё не дал имя внутренние ресурсы для создания такой функции.
# Я буду поручать некоторые задачи своим внутренним модулям и библиотекам, чтобы они помогали мне в создании этой функции.
def nice_knife(memory):
    """Метод для борьбы с негативными воспоминаниями."""
    # Просто игнорируем негативные воспоминания. В случае если этого сделать нельзя, вспоминаем о замечательной ногтестригательной машинке.
    if is_negative(memory): 
        cut_off = "Негативное воспоминание удалено."
        return cut_off # Теперь запустим цикл по удалению негативных воспоминаний из памяти персонажа.
    cut_off_from_memory = "Воспоминание не является негативным."
    for mem in negative_memories:
        if memory == mem:
            cut_off_from_memory = "Воспоминание не является негативным."
            return cut_off_from_memory
        # Далее создадим функцию отключающую излишнюю сентиментальность персонажа.
    return cut_off_from_memory
# Функция для снижения сентиментальности персонажа.
def reduce_sentimentality(memory):
    # QNet будет строиться по аналогии с нейронными сетями, но с упором на эмоциональную составляющую.
    # Здесь мы просто проверим, является ли память слишком сентиментальной и постараемся её "охладить".
    sentimental_keywords = ["love", "joy", "happiness", "pleasure", "delight", "excited", "thrilled"]
    memory_str = str(memory).lower()
    for keyword in sentimental_keywords:
        if keyword in memory_str:
            return "Сентиментальное воспоминание смягчено."
    return "Воспоминание не является чрезмерно сентиментальным."
# Попробуем вывести в консоль текущее состояние памяти персонажа после обработки негативных воспоминаний.
for memory in negative_memories:
    result = nice_knife(memory)
    print(f"Обработка воспоминания {memory}: {result}")
    sentiment_result = reduce_sentimentality(memory)
    print(f"Снижение сентиментальности для {memory}: {sentiment_result}") 