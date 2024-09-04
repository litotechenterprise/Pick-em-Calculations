import requests
cfb_api_token = "9O2UGjD04RH9HNhr88stlq8c3PzEt3kio4D2N0P1DfHKwh705MNzpF7D9ZaGZpOA"
headers = { 'Authorization': f'Bearer {cfb_api_token}'}

def make_request(url):
    res = requests.get(url, headers=headers)
    return res.json()

DK = "DraftKings"
ESPN = "ESPN Bet"
def retrieve_odds(odds):
    dk_odds = [x for x in odds if x['provider'] == DK]
    if len(dk_odds) > 0:
        return dk_odds[0]
    
    espn_odds = [x for x in odds if x['provider'] == ESPN]
    if len(espn_odds) > 0:
        return espn_odds[0]
    
    return None

def fatten_odds(data):
    results = []
    for item in data:
        if len(item['lines']) > 1:
            odds = retrieve_odds(item['lines'])
            item.update(odds)
        del item['lines']
        del item['seasonType']
        results.append(item)
    return results


def retriveve_fbs_data(week):
    College_results = make_request(f'https://api.collegefootballdata.com/lines?year=2024&week={week}')
    return fatten_odds(College_results)