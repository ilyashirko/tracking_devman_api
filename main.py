from environs import Env
import requests
import json
import time

USER_REVIEWS_URL = 'https://dvmn.org/api/user_reviews/'

LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'



if __name__ == '__main__':
    env = Env()
    env.read_env()

    headers = {
        "Authorization": f"Token {env.str('token')}"
    }
    params = {}
    while True:
        try:
            response = requests.get(LONG_POLLING_URL, headers=headers, params=params)
            response_info = response.json()
            params.update(
                {
                    "timestamp": int(response_info["timestamp_to_request"])
                }
            )
            print(json.dumps(response_info, indent=4, ensure_ascii=False))
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as error:
            print(f'{error}\nRepeate request...')
            time.sleep(5)
        




    """
    'status' in ['timeout', 'found'],
    'new_attempts: [
        'is_negative': true / false
    ]
    """