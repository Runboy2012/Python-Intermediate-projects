import speech_recognition as sr
import pyttsx3
import pyaudio
import random

try:
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    if not voices:
        print("Ошибка: нет доступных голосов для синтеза речи")
        exit()

        def main():
    try:
        speak("Привет! Я голосовой ассистент. Спроси что-нибудь.")
        while True:
            command = listen_command()
            if command is None:
                continue
            if "шутка" in command:
                tell_joke()
            elif "ютуб" in command or "youtube" in command:
                open_youtube()
            elif "ватсап" in command or "whatsapp" in command:
                run_app("whatsapp")
            elif "калькулятор" in command:
                run_app("калькулятор")
            elif "выход" in command or "пока" in command:
                speak("До свидания!")
                break
            else:
                speak("Извините, я не поняла команду.")
    except KeyboardInterrupt:
        speak("Работа завершена по запросу пользователя.")
    except Exception as e:
        print(f"Критическая ошибка: {e}")

    ru_voice = None
    for voice in voices:
        # В некоторых системах voice.languages содержит список байтов, в других строку
        langs = [
            lang.decode("utf-8").lower() if isinstance(lang, bytes) else lang.lower()
            for lang in voice.languages
        ]
        if any("ru" in lang for lang in langs):
            ru_voice = voice
            break

    if ru_voice:
        engine.setProperty("voice", ru_voice.id)
    else:
        engine.setProperty("voice", voices[0].id)  # первый голос

except Exception as e:
    print(f"Ошибка инициализации TTS: {e}")
    engine = None


def speak(text):
    try:
        local_engine = pyttsx3.init()
        voices = local_engine.getProperty("voices")
        ru_voice = next(
            (
                v
                for v in voices
                if any(
                    "ru"
                    in (
                        lang.decode("utf-8")
                        if isinstance(lang, bytes)
                        else lang.lower()
                    )
                    for lang in v.languages
                )
            ),
            voices[0],
        )
        local_engine.setProperty("voice", ru_voice.id)
        print(text)
        local_engine.say(text)
        local_engine.runAndWait()
    except Exception as e:
        print(f"Ошибка TTS: {e}")


def listen_command():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            speak("Говорите, я вас слушаю...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio, language="ru-RU")
                print(f"Вы сказали: {command}")
                return command.lower()
            except sr.WaitTimeoutError:
                speak("Время ожидания закончилось, попробуйте ещё раз.")
                return None
            except sr.UnknownValueError:
                speak("Не удалось распознать речь")
                return None
            except sr.RequestError:
                speak("Ошибка при обращении к сервису Google")
                return None
            except Exception as e:
                speak(f"Ошибка распознавания: {e}")
                return None
    except sr.PortAudioError:
        speak("Ошибка микрофона. Проверьте подключение.")
        return None


def tell_joke():
    jokes = [
        "Почему программисты не любят природу? Там слишком много багов!",
        "Что говорит ноль восьмерке? Классный пояс!",
        "Как программист называет свою работу? Debugging!",
        "Сколько нужно программистов, чтобы заменить лампочку? Ни одного — это аппаратная проблема!",
    ]
    speak(random.choice(jokes))


def run_app(app_name):
    try:
        if app_name == "whatsapp":
            # Укажите правильный путь к WhatsApp
            whatsapp_path = r"C:\Users\YourUserName\AppData\Local\WhatsApp\WhatsApp.exe"
            subprocess.Popen(whatsapp_path)
            speak("Открываю WhatsApp.")
        elif app_name == "калькулятор":
            subprocess.Popen("calc.exe")
            speak("Открываю калькулятор.")
        else:
            speak("Приложение не найдено.")
    except FileNotFoundError:
        speak("Не удалось найти приложение. Проверьте путь.")
    except Exception as e:
        speak(f"Ошибка при запуске приложения: {e}")


def open_youtube():
    try:
        speak("Открываю YouTube.")
        webbrowser.open("https://www.youtube.com")
    except Exception as e:
        speak(f"Ошибка при открытии YouTube: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ошибка при запуске: {e}")
