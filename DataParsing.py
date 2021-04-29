# Data Parsing is a set of functions that helps move the data into a csv with the desired statistics

import pandas as pd
import csv
import math
import re
import numpy as np
import unidecode
# Data from Retrosheet Game Logs 
# Global variable for reading the Lineup Data
# df = pd.read_csv('LineupData.csv')

# Data from Baseball reference
# Global variable for reading pitcher's stats
# pitcher_stats = pd.read_csv('PitchingData.csv', encoding = 'ISO-8859-1') #encoding using ISO-8859-1
# pitcher_names = pitcher_stats.iloc[:,1].values

# Data from Baseball reference
# Global variable for reading batter's stats
# batter_stats = pd.read_csv('BattingData.csv', encoding = 'ISO-8859-1') #encoding using ISO-8859-1
# batter_names = batter_stats.iloc[:,1].values # lists all batter names  



def get_winner(i, frame):
    """
    Returns 1 if home team won game, -1 if visiting team won.
    i is the row of the game examined
    """
    scores = frame.iloc[i,9:11].values.tolist()  #gets the total runs of each tea (V,H)
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



def get_pitcher_stats(pitcher, frame, frame2):
    """ 
    Gets the pitching stats given the name of a pitcher (no error checking)
    input: name of player
    output: their season statistics (ERA, FIP, WHIP, H9, HR9, BB9, SO9)
    """

    pitcher_names = frame
    pitcher_stats = frame2

    
    for i in range(len(pitcher_names)):
        if (pitcher_names[i] == pitcher or pitcher_names[i] == pitcher + " Jr."):
            statsdf = pitcher_stats.iloc[i,28:34]
            stats = statsdf.values.tolist()
            stats += [pitcher_stats.iloc[i,8]]
            return stats
    
    # If we don't find the pitcher's name
    # We use the league average stats
    statsdf = pitcher_stats.iloc[-1,28:34]
    stats = statsdf.values.tolist()
    stats += [pitcher_stats.iloc[-1,8]]
    print(pitcher + " not found, using league average")
    return stats


  
def get_batter_stats(batter, frame, frame2):
    """ 
    Gets the pitching stats given the name of a batter (no error checking)
    input: name of player
    output: their season statistics (OPS)
    
    Commented is code to get more stats (deemed unecessary as of now)
    """

    batter_names = frame
    batter_stats = frame2
    # print(batter_names)
    # input("Stopped")

    for i in range(len(batter_names)):
        if (batter_names[i] == batter or batter_names[i] == batter + " Jr."):
            
            #statsdf = batter_stats.iloc[i,21:26]
            stats = [batter_stats.iloc[i,21]]
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




def create_csv(year):
    """
    This makes a scv file with the appropiate data in the appropriate order:
    Each row is an MLB game,
    the first 7 columns are the Visiting starting pitchers's stats
    the second 7 columns are the Home starting pitcher's stats
    the next nine are the Visiting lineup's OPS, in batting order
    the next nine are the Home lineup's OPS, in batting order
    the last column is the result of the game (1) or (-1)
    """
    df = pd.read_csv("Data/LineupData/GL20" + year + ".TXT")
        
    batter_stats1 = pd.read_csv('Data/BattingData/20' + year + 'BattingData.csv', encoding = 'ISO-8859-1') #encoding using ISO-8859-1
    batter_names1 = batter_stats1.iloc[:,0].values # lists all batter names  

    pitcher_stats1 = pd.read_csv('Data/PitchingData/20' + year + 'PitchingData.csv', encoding = 'ISO-8859-1') #encoding using ISO-8859-1
    pitcher_names1 = pitcher_stats1.iloc[:,0].values




    stats = []
    for i in range(df.shape[0]):
        # each row of the new csv
        row = []
        # find the starting pitchers
        pitcher_names = df.iloc[i,102:105:2].values.tolist()
        # for each pitcher
        for j in pitcher_names:
            try:
                row += get_pitcher_stats(j,pitcher_names1, pitcher_stats1)
            # If the pitcher's name results in an error, print
            except:
                print(year + " Pitcher: " + j + " has caused an error")
        
        # find the starting lineups
        batter_names = df.iloc[i,106:160:3].values.tolist()
        # for each batter
        for k in batter_names:
            try:
                row += get_batter_stats(k,batter_names1, batter_stats1)
            # If the batter's name results in an error, print
            except:
                print(year + " Batter:" + k + " has caused an error")
        # lastly, we ass the winner of the game
        row += get_winner(i,df)
        # add each row to the potential csv
        stats += [row]
    return stats

# def create_csv10():
#     years = ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
#     ret = []
#     for i in years:
#         df10 = pd.read_csv("Data/LineupData/GL20" + i + ".TXT")
#         pitcher_names = df10.iloc[i,102:105:2].values.tolist()
#         batter_names = df10.iloc[i,106:160:3].values.tolist()






def write_csv(filename, year):
    """
    Takes the data and puts it into a workable csv file
    input: filename: a csv file
    """ 
    f = open(filename, "w", newline='')
    w = csv.writer(f)
    stats = create_csv(year)
    for row in stats:
        w.writerow(row)
    f.close()

def prepare_data(filename):
    f = open("Data/PitchingData/" + filename + ".txt", "r")
    data = f.read()
    data = data.replace("*", "")
    data = data.replace("#", "")
    data = data.replace("\\", ",")
    data = unidecode.unidecode(data)
    #w = csv.writer(f)
    nf = open("Data/PitchingData/" + filename + ".csv", "w")
    nf.write(data)
    #print(data)
    f.close()


if True:
    """
    Main function for tests
    """

write_csv("2010TotalData.throw", "10")