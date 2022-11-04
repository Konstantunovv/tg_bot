### Telegram-bot

```
Телеграм-бот для отслеживания статуса проверки домашней работы на Яндекс.Практикум.
Присылает сообщения, когда статус изменен - взято в проверку, есть замечания, зачтено.
```

### Технологии:
```
- pytest==6.2.5
- python-dotenv==0.19.0
- python-telegram-bot==13.7
- requests==2.26.0
```
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
SSH
git clone git@github.com:PashkaVRN/homework_bot.git
```
```
HTTP
https://github.com/Konstantunovv/homework_bot.git
```

```
cd homework_bot
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```
```
Windows
source env/bin/activate
```
```
macOS или Linux:
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Записать в переменные окружения (файл .env) необходимые ключи:
- токен профиля на Яндекс.Практикуме
- токен телеграм-бота
- свой ID в телеграме


Запустить проект:

```
python homework.py
```