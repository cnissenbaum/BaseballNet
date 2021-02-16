import pandas as pd


df = pd.read_csv('LineupData.csv')


def get_scores():
    """
    Gets the scores for the visit
    """
    scores = df.iloc[:,9:11].values #gets scores of the visiting and home teams
    return scores

def get_game_rd(i):
    scores = df.iloc[i,9:11].values.tolist()
    return [scores[0] - scores[1]]

def get_pitcher_names():
    """
    Gets the pitcher names for both teams
    output: a list of pitcher names
    """
    pitcher_names = df.iloc[:,102:105:2].values #gets the names of the starting pitchers (V,H)
    return pitcher_names

def get_batter_names():
    """
    Gets the batter names for both teams
    output: a list of batter names
    """
    batter_names = df.iloc[:,106:160:3].values #gets the name of the starting batters (V,H)
    batter_names = batter_names.tolist()
    return batter_names

def get_pitcher_stats(pitcher):
    """ gets the pitching stats given a name
    input: name of player
    output: their season statistics (ERA, FIP, WHIP, H9, HR9, BB9, SO9)
    """
    pitcher_stats = pd.read_csv('PitchingData.csv', encoding = 'ISO-8859-1') #encoding using ISO-8859-1
    names = pitcher_stats.iloc[:,3].values
    #print(pitcher_stats)
    for i in range(len(names)):
        if (names[i] == pitcher or names[i] == pitcher + " Jr."):
            statsdf = pitcher_stats.iloc[i,31:37]
            stats = statsdf.values.tolist()
            stats += [pitcher_stats.iloc[i,11]]
            return stats
    
def get_batter_stats(batter):
    batter_stats = pd.read_csv('BattingData.csv', encoding = 'ISO-8859-1') #encoding using ISO-8859-1
    names = batter_stats.iloc[:,3].values
    for i in range(len(names)):
        if (names[i] == batter or names[i] == batter + " Jr."):
            statsdf = batter_stats.iloc[i,21:26]
            stats = statsdf.values.tolist()
            #print(stats)
            return stats

def create_csv():
    """
    """
    stats = []
    for i in range(df.shape[0]):
        row = []
        pitcher_names = df.iloc[i,102:105:2].values.tolist()
        for j in pitcher_names:
            try:
                row += get_pitcher_stats(j)
            except:
                print("Perror")
                print(j)
            
        batter_names = df.iloc[i,106:160:3].values.tolist()
        for k in batter_names:

            try:
                row += get_batter_stats(k)
            except:
                print("error")
                print(k)

        row += get_game_rd(i)
        #print(row)
        stats += [row]
    #print(stats)
    return stats

create_csv()

# if True:
#     """
#     Main function for tests
#     """
#     #get_pitcher_stats('Jhoulys Chacin') #test get_stats function on a player
#     #get_batter_stats('Charlie Blackmon')
#     #batter = get_batter_names()[423][12]
#     #print(batter)
#     #print(get_batter_stats(batter))
#     pitcher = get_pitcher_names()[34][1]
#     print(pitcher)
#     print(get_pitcher_stats(pitcher))

