# BaseballNet

This is meant to be a Classification Neural Network for predicting the outcomes
of MLB games. The data is supplied in the github repository, and is from the
years 2010-2020.

The file "createcsv10year.py" formulates the data into tthe right format for the
Neural Net. The file "scikitlearn.py" trains, runs and saves the Neural Net, using
the underlying skeleton code from SciKitLearn.

In general, we get about a 53-57% accuracy in the training data, with best results
coming from a four layer (46-32-16-8), Neural Net from 0.03 initial learning rate. 

This project is for CS189 course at Harvey Mudd College. 