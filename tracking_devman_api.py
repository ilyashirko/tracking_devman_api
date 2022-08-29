import json
import logging
import time
from textwrap import dedent

import requests
import telegram
from environs import Env

LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    bot = telegram.Bot(token=env.str('TELEGRAM_TOKEN'))
    
    logging.basicConfig(
        filename=env.str('LOG_FILENAME'),
        level=logging.INFO,
        format="[%(asctime)s][%(levelname)s] %(message)s"
    )
    bot.logger.addHandler(TelegramLogsHandler(bot, env.str('TELEGRAM_USER_ID')))
    bot.logger.info('Start bot')

    headers = {"Authorization": f"Token {env.str('DEVMAN_TOKEN')}"}
    params = dict()

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
                    bot.logger.info(f'GOT REVIEW for lesson \"{attempt["lesson_title"]}\"')

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
                json.decoder.JSONDecodeError,
                requests.exceptions.ReadTimeout,
                KeyError) as error:
            bot.logger.error(f'{error}\nRepeate request...', exc_info=True)
            time.sleep(5)
