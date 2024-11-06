import requests
from urllib.parse import urlparse, parse_qs
import hashlib

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'authorization': '',
    'x-requested-with': 'org.telegram.messenger',
}
def compute_md5(amount ,seq):
    prefix = str(amount) + str(seq) + "7be2a16a82054ee58398c5edb7ac4a5a"
    return hashlib.md5(prefix.encode()).hexdigest()
  
def auth(url:str ) -> dict:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.fragment)
    init = query_params.get('tgWebAppData', [None])[0]
    params = {'invitationCode': '',  'initData':init}
    data = {'invitationCode': '', 'initData':init,}
    response = requests.post('https://api.freedogs.bot/miniapps/api/user/telegram_auth', params=params, headers=headers, data=data)
    return response.json()


def do_click(init):
    headers['authorization'] = 'Bearer ' + auth(init)['data']['token']
    params = ''
    response = requests.get('https://api.freedogs.bot/miniapps/api/user_game_level/GetGameInfo', params=params, headers=headers)
    Seq = response.json()['data']['collectSeqNo']
    hsh = compute_md5('100000',Seq)
    params = {
        'collectAmount':'100000' ,
        'hashCode': hsh,
        'collectSeqNo': str(Seq),
    }
    response = requests.post('https://api.freedogs.bot/miniapps/api/user_game/collectCoin', params=params, headers=headers, data=params)
    return response.json()  

if __name__== '__main__':   
    #replace it with your own tgwebappdata
    result = do_click('query_id=AAFRLpVMAgAAAFEulUyproi0&user=%7B%22id%22%3A5579812433%2C%22first_name%22%3A%22%E2%95%BF%F0%9D%91%AE%F0%9D%92%89%F0%9D%92%90%F0%9D%92%94%F0%9D%92%95%22%2C%22last_name%22%3A%22%F0%9D%91%B4%F0%9D%92%82%F0%9D%92%8F%E2%95%BD%22%2C%22username%22%3A%22GH0ST_MAN%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1730885752&hash=ef2a5fd72936d5307234bd05523f6bff7247b3ef134647f5a218e280df8e604a')
    print(result)
