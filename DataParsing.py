import pandas as pd


df = pd.read_csv('LineupData.csv')

#print(df)

# scores = df.iloc[:,9:11].values #gets scores of the visiting and home teams
# pitcher_names = df.iloc[:,102:105:2].values #gets the names of the starting pitchers (V,H)
# batter_names = df.iloc[:,106:160:3].values #gets the name of the starting batters (V,H)
# print(pitcher_names)



def get_stats(pitcher):
    """ gets the pitching stats given a name
    input: name of player
    output: their season statistics (ERA, FIP, WHIP, H9, HR9, BB9, SO9)
    """
    pitcher_stats = pd.read_csv('PitchingData.csv', encoding = 'ISO-8859-1') #encoding using ISO-8859-1
    names = pitcher_stats.iloc[:,3].values
    #print(pitcher_stats)
    for i in range(len(names)):
        if names[i] == pitcher:
            statsdf = pitcher_stats.iloc[i,31:37]
            stats = statsdf.values.tolist()
            stats += [pitcher_stats.iloc[i,11]]
            print(stats)
            return stats
    
if True:
    get_stats('Jhoulys Chacin') #test get_stats function on a player
    
