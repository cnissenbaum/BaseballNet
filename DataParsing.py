import pandas as pd
import csv
import math
import re
import numpy as np
# Data from Retrosheet Game Logs 
# Global variable for reading the Lineup Data
df = pd.read_csv('LineupData.csv')

# Data from Baseball reference
# Global variable for reading pitcher's stats
pitcher_stats = pd.read_csv('PitchingData.csv', encoding = 'ISO-8859-1') #encoding using ISO-8859-1
pitcher_names = pitcher_stats.iloc[:,3].values

# Data from Baseball reference
# Global variable for reading batter's stats
batter_stats = pd.read_csv('BattingData.csv', encoding = 'ISO-8859-1') #encoding using ISO-8859-1
batter_names = batter_stats.iloc[:,3].values # lists all batter names  



def get_winner(i):
    """
    Returns 1 if home team won game, -1 if visiting team won.
    i is the row of the game examined
    """
    scores = df.iloc[i,9:11].values.tolist()  #gets the total runs of each tea (V,H)
    if (scores[0] > scores[1]):
        return [1]
    else:
        return [-1]



def get_pitcher_names(i):
    """
    Returns an array of the starting pitchers,
    for the given game (row)
    """
    pitcher_names = df.iloc[i:,102:105:2].values #gets the names of the starting pitchers (V,H)
    pitcher_names = pitcher_names.tolist()
    return pitcher_names



def get_batter_names(i):
    """
    Returns an array of the starting batters,
    for the given game (row)
    """
    batter_names = df.iloc[i:,106:160:3].values #gets the name of the starting batters (V,H)
    batter_names = batter_names.tolist()
    return batter_names



def get_pitcher_stats(pitcher):
    """ 
    Gets the pitching stats given the name of a pitcher (no error checking)
    input: name of player
    output: their season statistics (ERA, FIP, WHIP, H9, HR9, BB9, SO9)
    """
    
    for i in range(len(pitcher_names)):
        if (pitcher_names[i] == pitcher or pitcher_names[i] == pitcher + " Jr."):
            statsdf = pitcher_stats.iloc[i,31:37]
            stats = statsdf.values.tolist()
            stats += [pitcher_stats.iloc[i,11]]
            return stats
    
    # If we don't find the pitcher's name
    # We use the league average stats
    statsdf = pitcher_stats.iloc[-1,31:37]
    stats = statsdf.values.tolist()
    stats += [pitcher_stats.iloc[-1,11]]
    print(pitcher + " not found, using league average")
    return stats


  
def get_batter_stats(batter):
    """ 
    Gets the pitching stats given the name of a batter (no error checking)
    input: name of player
    output: their season statistics (OPS)
    
    Commented is code to get more stats (deemed unecessary as of now)
    """
    for i in range(len(batter_names)):
        if (batter_names[i] == batter or batter_names[i] == batter + " Jr."):
            
            #statsdf = batter_stats.iloc[i,21:26]
            stats = [batter_stats.iloc[i,24]]
            #stats = statsdf.values.tolist()

            # If there are no batting stats for the found player
            if (math.isnan(stats[0])):
                print(batter + " sucks - All zeros")
                # We use a 0 OPS because they are probably not very good
                return [0] #[0,0,0,0,-100]
            return stats
    
    #statsdf1 = batter_stats.iloc[-1,21:26]

    # If we don't find the pitcher's name
    # We use the league average stats
    stats1 = [batter_stats.iloc[-1,24]]

    #stats1 = statsdf1.values.tolist()

    print(batter + " not found, using average league data")
    return stats1




def create_csv():
    """
    This makes a scv file with the appropiate data in the appropriate order:
    Each row is an MLB game,
    the first 7 columns are the Visiting starting pitchers's stats
    the second 7 columns are the Home starting pitcher's stats
    the next nine are the Visiting lineup's OPS, in batting order
    the next nine are the Home lineup's OPS, in batting order
    the last column is the result of the game (1) or (-1)
    """

    stats = []
    for i in range(df.shape[0]):
        # each row of the new csv
        row = []
        # find the starting pitchers
        pitcher_names = df.iloc[i,102:105:2].values.tolist()
        # for each pitcher
        for j in pitcher_names:
            try:
                row += get_pitcher_stats(j)
            # If the pitcher's name results in an error, print
            except:
                print("Picher: " + j + " has caused an error")
        
        # find the starting lineups
        batter_names = df.iloc[i,106:160:3].values.tolist()
        # for each batter
        for k in batter_names:
            try:
                row += get_batter_stats(k)
            # If the batter's name results in an error, print
            except:
                print("Batter:" + k + " has caused an error")
        # lastly, we ass the winner of the game
        row += get_winner(i)
        # add each row to the potential csv
        stats += [row]
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



if True:
    """
    Main function for tests
    """
    write_csv("gameData2.csv")