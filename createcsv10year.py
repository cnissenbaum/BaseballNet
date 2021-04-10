import pandas as pd
import csv
import math
import re
import numpy as np
import unidecode

def create_csv():

    write = []

    for i in range(10,21):
        print("Year 20" + str(i))
        f = open("Data/LineupData/GL20"+str(i)+".TXT","r")
        g = open("Data/PitchingData/20"+str(i)+"PitchingData.csv")
        h = open("Data/BattingData/20"+str(i)+"BattingData.csv")

        pitchingData = g.read().split('\n')

        for i in range(len(pitchingData)):
            pitchingData[i] = pitchingData[i].split(',')

        pitchingData = pitchingData[0:-1]
        
        battingData = h.read().split('\n')

        for i in range(len(battingData)):
            battingData[i] = battingData[i].split(',')

        battingData = battingData[0:-1]

        

        lineupData = f.read().replace('"',"").split('\n')
        lineupData = lineupData[0:-1]
        for line in lineupData:
            gamePitchingData = []
            gameBattingData = []

            line = line.split(',')
            for i in [102,104]:
                gamePitchingData += get_game_pitching_data(line[i], pitchingData)
            for i in range(106,160,3):
                gameBattingData  += get_game_batting_data(line[i], battingData)

            if (line[9] < line[10]):
                result = [1]
            else:
                result = [-1]

            write += [gamePitchingData + gameBattingData + result]
    
    p = open("LongGameData.csv",'w')
    w = csv.writer(p)
    for row in write:
        w.writerow(row)
    f.close()


def get_game_pitching_data(name, data):

    stats = []

    for line in data:
        if(name == line[1]):
            stats += [line[9]]
            for i in range(28,34):
                stats += [line[i]]
            return stats

    # Pitching Stats
    print("P: " + name)
    return [data[-1][9]] + data[-1][28:34]


def get_game_batting_data(name, data):


    for line in data:
        if(name == line[1]):
            return [line[21]]
    
    print("H: " + name)
    # ops
    return [data[-1][21]]

create_csv()