import pandas as pd
from api import retriveve_fbs_data
from util import col_names, split_string, return_values
import os
results = []
week = int(input("Please enter week (of fbs): \n"))
fbs_data = retriveve_fbs_data(week)
ncaa_df = pd.DataFrame(fbs_data)

picks = pd.read_csv('week-1.csv')
picks.columns.values[1] = col_names["NAME"]
picks.columns.values[2] = col_names["CFB_OVER"]
picks.columns.values[3] = col_names["CFB_UNDER"]
picks.columns.values[4] = col_names["CFB_FAV"]
picks.columns.values[5] = col_names["CFB_DOG"]

def retrieve_game(df:pd.DataFrame, game:str):
    obj = split_string(game)
    game1 = df.loc[(df["awayTeam"] == obj['awayTeam'])]
    if not game1.empty:
        return {"game": game1, "odds": obj["odds"],"home":obj["homeTeam"],"away":obj["awayTeam"], "found": True}
    game2 = df.loc[df["homeTeam"] == obj["homeTeam"]]

    if not game2.empty:
        return {"game": game2, "odds": obj["odds"],"home":obj["homeTeam"],"away":obj["awayTeam"], "found": True}
    
    game3 = df.loc[df["homeTeam"] == obj["awayTeam"]]
    if not game3.empty:
        return {"game": game3, "odds": obj["odds"],"home":obj["homeTeam"],"away":obj["awayTeam"], "found": True}
    
    game4 = df.loc[df["awayTeam"] == obj["homeTeam"]] 
    if not game4.empty:
        return {"game": game4, "odds": obj["odds"],"home":obj["homeTeam"],"away":obj["awayTeam"], "found": True}

    return {"found": False}
    



def calculate_under_results(df:pd.DataFrame, str:str):
    results = retrieve_game(df, str)
    game = results["game"]
    odds = results["odds"]
    has_odds = bool(game.get("provider").values[0])
    if has_odds:
        scores = return_values(game, ["overUnder", 'homeScore','awayScore'])
        return scores[0] >= scores[1] + scores[2]
    else:
        print(f"No odds for this game {str}")
        print(f"User odds {odds}")
        return False

def calculate_over_results(df:pd.DataFrame, str:str):
    results = retrieve_game(df, str)
    game = results["game"]
    odds = results["odds"]
    has_odds = bool(game.get("provider").values[0])
    if has_odds:
        scores = return_values(game, ["overUnder", 'homeScore','awayScore'])
        return scores[0] <= scores[1] + scores[2]
    else:
        print(f"No odds for this game {str}")
        print(f"User odds {odds}")
        return False


def calculate_favorite_results(df:pd.DataFrame, str:str):
    results = retrieve_game(df, str)
    if not results['found']:
        print(f"Not able to verify game: {str}")
    game = results["game"]
    odds = results["odds"]
    home = results["home"]
    away = results['away']
    scores = return_values(game, ['homeScore','awayScore'])
    number = odds[1:-1].split(" ")[-1]
    handicap = float(number)
    if home in odds:
        return  scores[1] <= scores[0] + handicap
    if away in odds:
        return  scores[0] <= scores[1] + handicap
    


def calculate_underdawg_results(df:pd.DataFrame, str:str):
    results = retrieve_game(df, str)
    if not results['found']:
        print(f"Not able to verify game: {str}")
    game = results["game"]
    odds = results["odds"]
    home = results["home"]
    away = results['away']
    scores = return_values(game, ['homeScore','awayScore'])
    number = odds[1:-1].split(" ")[-1]
    handicap = float(number)

    if home in odds:
        return  scores[1] <= scores[0] + handicap

    if away in odds:
        return  scores[0] <= scores[1] + handicap
    


def calculate_points(row):
     points = 0
     ncaa_over = calculate_over_results(ncaa_df, row.get(col_names["CFB_OVER"]))
     ncaa_under = calculate_under_results(ncaa_df, row.get(col_names["CFB_UNDER"]))
     ncaa_fav = calculate_favorite_results(ncaa_df, row.get(col_names["CFB_FAV"]))
     ncaa_dog = calculate_underdawg_results(ncaa_df, row.get(col_names["CFB_DOG"]))

     if ncaa_over:
        points +=1 
     if ncaa_under:
         points +=1
     if ncaa_fav:
         points +=1
     if ncaa_dog:
         points +=1
         
     results.append([row.get(col_names["NAME"]),ncaa_over, ncaa_under, ncaa_fav, ncaa_dog, points ])
     return points


points = []
for index, row in picks.iterrows():
    points.append(calculate_points(row))

picks[col_names["POINTS"]] = points
results_df = pd.DataFrame(results)

if not os.path.exists(f"output/week_{week}"):
    os.makedirs(f"output/week_{week}")

ncaa_df.to_csv(f"output/week_{week}/fbs_data.csv")
results_df.to_csv(f"output/week_{week}/results.csv")
picks.to_csv(f"output/week_{week}/output.csv")

