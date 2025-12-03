# Переименованный файл, например my_app.py
import asyncio

async def main():
    print("Запуск асинхронной задачи")
    # Ваш код здесь
    await asyncio.sleep(1)
    print("Задача завершена")

if __name__ == "__main__":
    asyncio.run(main())
