import json
import time

import requests
import telegram

from environs import Env

LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'


if __name__ == '__main__':
    env = Env()
    env.read_env()

    bot = telegram.Bot(token=env.str('TELEGRAM_TOKEN'))

    headers = {"Authorization": f"Token {env.str('DEVMAN_TOKEN')}"}
    params = {}

    while True:
        try:
            response = requests.get(
                LONG_POLLING_URL,
                headers=headers,
                params=params
            ).json()
            if response["status"] == 'found':
                message = ''
                for attempt in response["new_attempts"]:
                    lesson_title = attempt['lesson_title']
                    if attempt["is_negative"]:
                        message += (
                            f'The lesson "{attempt["lesson_title"]}" '
                            f'has been sent for revision.\n\n'
                            f'{attempt["lesson_url"]}'
                        )
                    else:
                        message += (
                            f'Congratulations! '
                            f'Lesson "{attempt["lesson_title"]}" passed!'
                        )
                    bot.send_message(
                        chat_id=env.str('USER_ID'),
                        text=message
                    )

                params.update(
                    {
                        "timestamp": int(
                            response["last_attempt_timestamp"] + 1
                        )
                    }
                )
            else:
                params.update(
                    {
                        "timestamp": int(response["timestamp_to_request"])
                    }
                )
        except (requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError,
                json.decoder.JSONDecodeError) as error:
            print(f'{error}\nRepeate request...')
            time.sleep(5)
