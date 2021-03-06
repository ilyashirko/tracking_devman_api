# Отслеживание прогресса обучения в [DEVMAN](https://dvmn.org)
Телеграм бот проверяющий в режиме реального времени прогресс ученика Devman и присылающий уведомление в телеграм в случае проверки очередного урока.
## Запуск бота
Для запуска бота необходимо клонировать репозиторий:
```
git clone https://github.com/ilyashirko/tracking_devman_api
```
Переместиться в корневую папку проекта и создать виртуальное окружение:
```
cd tracking_devman_api
python3 -m venv env
```
Активировать виртуальное окружение и установить зависимости:
```
source env/bin/activate
pip3 install -r requirements.txt
```
Поместить чувствительные данные в `.env` файл. Вам потребуются:  
1. Токен вашего телеграм бота. Создать бота и получить токен можно [здесь](BotFather)  
2. Токен вашей учетной записи в [DEVMAN](https://dvmn.org/api/docs/)  
3. Ваш Chat_id. получить его можно [здесь](https://t.me/userinfobot)  

Оформите ваши личные данные в файле `.env`:
```
DEVMAN_TOKEN=dgsdfs87dfg8ds7f8g7sd8f7g98s7df78
TELEGRAM_TOKEN=23423423423:AKJJHjkbjHbkbjkbKjbkjbkjbKjbKJbkJbkJb
TELEGRAM_USER_ID=123456789
```
Для запуска бота введите в командной строке:
```
python3 tracking_devman_api.py
```
В случае получение вами результата проверки, он будет отправлен в бот.