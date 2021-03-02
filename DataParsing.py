import pandas as pd
import csv
import math
import re
import numpy as np

df = pd.read_csv('LineupData.csv')


def get_scores():
    """
    Gets the scores for the teams
    """
    scores = df.iloc[:,9:11].values #gets scores of the visiting and home teams
    return scores

def get_game_rd(i):
    """
    Gets the game differential of a given game
    input: an int i for the game number that we will find
    """
    scores = df.iloc[i,9:11].values.tolist()
    if (scores[0] > scores[1]):
        return [1]
    else:
        return [-1]

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

pitcher_stats = pd.read_csv('PitchingData.csv', encoding = 'ISO-8859-1') #encoding using ISO-8859-1
names = pitcher_stats.iloc[:,3].values
def get_pitcher_stats(pitcher):
    """ gets the pitching stats given a name
    input: name of player
    output: their season statistics (ERA, FIP, WHIP, H9, HR9, BB9, SO9)
    """
    #print(pitcher_stats)
    
    for i in range(len(names)):
        if (names[i] == pitcher or names[i] == pitcher + " Jr."):
            statsdf = pitcher_stats.iloc[i,31:37]
            stats = statsdf.values.tolist()
            stats += [pitcher_stats.iloc[i,11]]
            return stats
    statsdf = pitcher_stats.iloc[-1,31:37]
    stats = statsdf.values.tolist()
    stats += [pitcher_stats.iloc[-1,11]]
    print(pitcher + " not found, using league average")
    return stats


batter_stats = pd.read_csv('BattingData.csv', encoding = 'ISO-8859-1') #encoding using ISO-8859-1
batter_names = batter_stats.iloc[:,3].values # lists all batter names    
def get_batter_stats(batter):
    """ gets the stats of a given batter
    input: name of player
    output: their season statistics (BA, OBP, SLG, OPS, OPS+)
    """
    for i in range(len(batter_names)):
        if (batter_names[i] == batter or batter_names[i] == batter + " Jr."):
            #statsdf = batter_stats.iloc[i,21:26]
            stats = [batter_stats.iloc[i,24]]
            #stats = statsdf.values.tolist()
            if (math.isnan(stats[0])):
                print(batter + " sucks - All zeros")
                return [0] #[0,0,0,0,-100]
            return stats      
    #statsdf1 = batter_stats.iloc[-1,21:26]
    stats1 = [batter_stats.iloc[-1,24]]
    #stats1 = statsdf1.values.tolist()
    print(batter + " not found, using average league data")
    return stats1

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
            b = get_batter_stats(k)
            try:
                row += b
            except:
                print("error")
                print(k)

        row += get_game_rd(i)
        #print(row)
        stats += [row]
    #print(stats)
    return stats
def write_csv(filename):
    """
    Takes the data and puts it into a workable csv file
    input: filename: a csv file
    """
    f = open(filename, "w", newline='')
    w = csv.writer(f)
    stats = create_csv()
    for row in stats:
        w.writerow(row)
    f.close()

#create_csv()
write_csv('gameData1.csv')
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

def goop():
    fs = open("gameData.csv", "r")
    fs = fs.read()
    fs = re.split(",|\n",fs)

    for i in fs:
        
        np.any(np.isnan(f))
        try:
            
            np.isnan(f)
        except:
            print("p" + i + "p")
    return 0



def goop2():
    dfr = pd.read_csv('gameData.csv')
    for i in dfr:
        if(not(type(i) == float)):
            #if(np.isnan(i)):
                print(i)
                #print('found nan')
print(get_pitcher_stats('Rogelio Armenteros'))
print(get_batter_stats('Rogelio Armenteros'))