# Event Planner

Сайт для планирования событий с возможностью управления уведомлениями, настройками темы и языка.

## Требования

- Python 3.10+  
- Django 4.x  
- Любой браузер для работы с веб-интерфейсом

## Установка

1. Клонируем репозиторий:
git clone https://github.com/andrey980765/second-project.git
cd eventplanner

2. Создать и активировать виртуальное окружение:
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

3. Установить зависимостии:
pip install -r requirements.txt

4. Применить миграции базы данных:
python manage.py migrate

5. Запустить сервер:
python manage.py runserver

6. Открыть в браузере:
http://127.0.0.1:8000/
