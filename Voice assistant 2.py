import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import pyjokes
import random
import openai
# Библиотека для интеграции нейросети в голосового ассистента (openai)

# Функция для воспроизведения речи
def speak(text):
    print(f"Ассистент: {text}")
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        print("Ошибка воспроизведения речи")

# Приветствие пользователя
def wish_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Доброе утро!")
    elif hour < 18:
        speak("Добрый день!")
    else:
        speak("Добрый вечер!")
    speak("Я ваш голосовой ассистент. Чем могу помочь?")

# Функция распознавания речи
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio, language='ru-RU')
            print(f"Вы: {query}")
            return query.lower()
        except:
            speak("Не удалось распознать речь. Повторите, пожалуйста.")
            return ""

# Основная функция ассистента
def run_assistant():
    wish_user()
    while True:
        query = take_command()
        if 'википедия' in query:
            try:
                speak("Поиск в Википедии...")
                result = wikipedia.summary(query, sentences=2)
                speak("По данным Википедии:")
                speak(result)
            except:
                speak("Не удалось найти информацию")
        elif 'открой ютуб' in query:
            speak("Открываю YouTube...")
            webbrowser.open("https://www.youtube.com/")
        elif 'открой гугл' in query:
            speak("Открываю Google...")
            webbrowser.open("https://www.google.com/")
        elif 'время' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Текущее время: {strTime}")
        elif 'анекдот' in query:
            joke = pyjokes.get_joke(language='ru')
            speak(joke)
        elif 'пока' in query or 'выход' in query:
            speak("До свидания! Хорошего дня!")
            break
        else:
            speak("Не совсем поняла. Повторите, пожалуйста.")

# Запуск ассистента
if __name__ == "__main__":
    run_assistant()
