import pandas as pd


col_names = {
    "NAME" : "Name",
"CFB_OVER" : "CFB Over",
"CFB_UNDER" : "CFB Under",
"CFB_FAV" : "CFB Favorite",
"CFB_DOG" : "CFB Underdog",
"NFL_OVER": "NFL Over",
"NFL_UNDER" : "NFL Under",
"NFL_FAV" : "NFL Favorite",
"NFL_DOG" : "NFL Underdog",
"POINTS" : "POINTS",
}

def split_string(str:str):
    split = str.split(" ")
    v_index = None
    odds_index = -1
    verse_array = ["v",'v.',"vs","vs."]
    
    for i in range(len(split)):
        word = split[i]
        if word.lower() in verse_array:
            v_index = i

        if any(char == "(" for char in word):
            odds_index = i
          
        if any((char.isdigit() or char == "(") for char in word):
            d_index = i
    away_team = " ".join(split[0:v_index])
    home_team = " ".join(split[v_index+1:odds_index])
    odds = " ".join(split[odds_index:])
    return {"awayTeam": away_team, "homeTeam":home_team, "odds": odds}


def return_values(df:pd.DataFrame,values):
    results = []
    for key in values:
        results.append(float(df.get(key).values[0]))
    return results