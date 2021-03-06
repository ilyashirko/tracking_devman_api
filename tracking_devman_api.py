import json
from textwrap import dedent
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
                params=params,
                timeout=100
            )
            response.raise_for_status()

            review_results = response.json()

            if review_results["status"] == 'found':
                message = ''
                for attempt in review_results["new_attempts"]:
                    lesson_title = attempt['lesson_title']
                    if attempt["is_negative"]:
                        message += (
                            f"""
                            The lesson "{attempt["lesson_title"]}" has been sent for revision.
                            {attempt["lesson_url"]}
                            """
                        )
                    else:
                        message += (
                            f"""
                            Congratulations!
                            Lesson "{attempt["lesson_title"]}" passed!
                            """
                        )
                    bot.send_message(
                        chat_id=env.str('TELEGRAM_USER_ID'),
                        text=dedent(message)
                    )

                params.update(
                    {
                        "timestamp": review_results["last_attempt_timestamp"]
                    }
                )
            else:
                params.update(
                    {
                        "timestamp": review_results["timestamp_to_request"]
                    }
                )
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                json.decoder.JSONDecodeError) as error:
            print(f'{error}\nRepeate request...')
            time.sleep(5)
        except requests.exceptions.ReadTimeout:
            pass
