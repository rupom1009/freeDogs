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
    result = do_click('https://app.freedogs.bot/#tgWebAppData=query_id%3DAAEijwdXAgAAACKPB1fw7SvJ%26user%3D%257B%2522id%2522%253A5755080482%252C%2522first_name%2522%253A%2522As%25CA%2580%25E1%25B4%2580%25CA%2580%2522%252C%2522last_name%2522%253A%2522R%25E1%25B4%2580%25CA%259C%25E1%25B4%258D%25E1%25B4%2580%25C9%25B4%2522%252C%2522username%2522%253A%2522Mr_Noobboy%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1729921889%26hash%3Dccd406ef8bd7fcdadfab9ac10bdreuh487a99ce6c3110cc616fc69c2666b1babd6f&tgWebAppVersion=7.10&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%231e1e1e%22%2C%22section_bg_color%22%3A%22%23181819%22%2C%22secondary_bg_color%22%3A%22%23000000%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%237d7d7d%22%2C%22link_color%22%3A%22%2357a7e0%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23232326%22%2C%22accent_text_color%22%3A%22%2364b5ef%22%2C%22section_header_text_color%22%3A%22%236cb6f8%22%2C%22subtitle_text_color%22%3A%22%237e7e7f%22%2C%22destructive_text_color%22%3A%22%23ee686f%22%2C%22section_separator_color%22%3A%22%23000000%22%2C%22bottom_bar_bg_color%22%3A%22%23000000%22%7D')
    print(result)
