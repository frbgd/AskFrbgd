# Кучерявенко Алексей АПО-11

Telegram: [@frbgd](https://t.me/frbgd)

На текущий момент реализованы ДЗ1, ДЗ2, ДЗ3, ДЗ4, ДЗ5, ДЗ6 (кроме ab) в ветке master.

База данных: [db.sqlite3](https://yadi.sk/d/DG82mhz-o01Tzg). Положить в директорию ```db```.

# Структура репозитория/приложения

Приложение работает через docker-compose. Создаётся 3 контейнера: wsgi_app, nginx и django.

В репозитории 4 основных директории:

 - ```wsgi_app``` - здесь хранится код WSGI-скрипта для задания из ДЗ6
 - ```db``` - здесь хранится база данных SQLite, данная директория монтируется к контейнеру django
 - ```nginx``` - здесь хранятся конфиги nginx и статика, директории и файлы отсюда монитруются к контейнерам nginx и django
 - ```django_app``` - здесь хранится код приложения на Django, а также конфиг gunicorn (```django_app/Ask_Frbgd/gunicorn.conf.py```)

# Запуск приложения

Загруженный файл базы данных скопировать в папку ```db```.

Освободить на хосте порты 80, 8000 и 8001.

Установить докер (если не установлен)

Запустить приложение: ```docker-compose up -d```

# Локальный запуск django

Установить Python3 (если не установлен)

Установить зависимости ```pip3 install -r django_app/requirements.txt```

Переопределить переменные окружения:

 - ```DATABASE_PATH=<путь к проекту>/db/db.sqlite3```
 - ```STATIC_ROOT=<путь к проекту>/nginx/static```
 - ```MEDIA_ROOT=<путь к проекту>/nginx/uploads```
 - ```DJANGO_DEBUG=true```

Установить рабочую директорию ```django_app```

Применить миграции (на всякий случай) ```python3 manage.py migrate```

Запустить командой ```python3 manage.py runserver 0.0.0.0:8000```

# Локальный запуск wsgi_app

Установить Python3 (если не установлен)

Установить зависимости ```pip3 install -r wsgi_app/requirements.txt```

Устновить рабочую директорию ```wsgi_app```

Запустить командой ```gunicorn app:app -c wsgi_app.conf.py```
