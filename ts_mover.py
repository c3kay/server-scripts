import requests
from os import environ

API_KEY = environ['TS_API_KEY']
URL = 'http://localhost:10080/'
IDLE_MIN = 30


def get_client_list(session):
    headers = {'X-Api-Key': API_KEY}
    params = {'-times': ''}

    with session.get(URL + 'clientlist', headers=headers, params=params) as res:
        res.raise_for_status()
        res_json = res.json()

    if res_json['status']['code'] != 0:
        raise RuntimeError('TeamSpeak Error: {}'.format(res_json['status']['message']))

    return res_json['body']


def move_clients(session, clients):
    for c in clients:
        # cid=22 -> poke, cid=23 -> afk
        if c['cid'] != '22' and c['cid'] != '23' and c['client_type'] != '1' and \
                int(c['client_idle_time']) >= IDLE_MIN * 60000:
            headers = {'X-Api-Key': API_KEY}
            params = {'clid': c['clid'], 'cid': '23'}

            with session.get(URL + 'clientmove', headers=headers, params=params) as res:
                res.raise_for_status()


def main():
    with requests.Session() as session:
        clients = get_client_list(session)
        move_clients(session, clients)


if __name__ == '__main__':
    main()
