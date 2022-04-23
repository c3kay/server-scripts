import requests
from os import environ


def load_cookies(cookies):
    cookie_dict = {}
    for cookie_data in cookies.split(";"):
        key, val = cookie_data.split("=")
        cookie_dict[key] = val
    return cookie_dict


def claim_reward(url, act_id, cookies):
    headers = {
        'Origin': 'https://webstatic-sea.hoyolab.com',
        'Referer': 'https://webstatic-sea.hoyolab.com/'
    }

    params = {
        'lang': 'en-us'
    }

    data = {
        'act_id': act_id
    }

    with requests.post(url, headers=headers, params=params, json=data, cookies=cookies) as res:
        res.raise_for_status()
        json_res = res.json()

    if json_res['message'] != 'OK':
        raise RuntimeError(json_res['message'])


def claim_genshin(cookies):
    act_id = 'e202102251931481'
    url = 'https://sg-hk4e-api.hoyolab.com/event/sol/sign'
    claim_reward(url, act_id, cookies)


def claim_honkai(cookies):
    act_id = 'e202110291205111'
    url = 'https://sg-public-api.hoyolab.com/event/mani/sign'
    claim_reward(url, act_id, cookies)


def main():
    try:
        cookie_str = environ['CLAIM_COOKIE_STR']
    except KeyError as err:
        raise RuntimeError('Could not load environment variables!') from err

    cookies = load_cookies(cookie_str)
    claim_genshin(cookies)
    claim_honkai(cookies)


if __name__ == '__main__':
    main()
