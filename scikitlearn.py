# scikitlearn.py uses the scikit learn library to create a machine learning model
# This program uses the mlp function to build a neural network to predict the results of baseball games using training data from 2010-2020



import numpy as np
from sklearn.neural_network import MLPClassifier
import pandas as pd
import pickle

# load data from csv
df = pd.read_csv('LongGameData.csv')

# make the first 32 columns the input data
# these columns are the statistics
X_data = df.iloc[:,:32].values # 104

# make the last column the output data
# uses supervised machine learning
# output data is the result from the last game
y_data = df.iloc[:,32].values
print('Data Done')

print('Start testing')
# mix up data so we don't always use the same testing and training data
KNOWN_SIZE = len(y_data)
indices = np.random.permutation(KNOWN_SIZE)
X_known = X_data[indices]
y_known = y_data[indices]


# use most of the data as training data and the rest as test data


TRAIN_FRACTION = 0.90

TRAIN_SIZE = int(TRAIN_FRACTION*KNOWN_SIZE)
TEST_SIZE = KNOWN_SIZE - TRAIN_SIZE  

# make training and testing sets
X_train = X_known[:TRAIN_SIZE]
y_train = y_known[:TRAIN_SIZE]

X_test = X_known[TRAIN_SIZE:]
y_test = y_known[TRAIN_SIZE:]

USE_SCALER = True
if USE_SCALER == True:
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaler.fit(X_known)   # Fit only to the training dataframe
    
    # rescale inputs
    X_known = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    

# We have found that (64, 32, 16, 8) is generally the best case in terms of layer sizes
# Also an initial learning rate of 0.03 works betteer than any other
mlp = MLPClassifier(hidden_layer_sizes=(64,8,8,8), max_iter=400, alpha=1e-6, activation = "relu",
                        solver='adam', verbose=True, shuffle=True, early_stopping = False, tol=1e-6, 
                        random_state=None, # reproduceability
                        learning_rate_init=.03, learning_rate = 'constant') #invscaling, adaptive, constant
print("\n\n++++++++++  TRAINING  +++++++++++++++\n\n")
mlp.fit(X_train, y_train)

# We generally average arounf 53-57% accuracy which I would consider a win.


"""
# trying k nearest neighbors
from sklearn.neighbors import KNeighborsClassifier
neigh = KNeighborsClassifier(n_neighbors=25)
neigh.fit(X_train, y_train)
"""

print("\n\n++++++++++++  TESTING  +++++++++++++\n\n")
print("Training set score: %f" % mlp.score(X_train, y_train))
print("Test set score: %f" % mlp.score(X_test, y_test))



predictions = mlp.predict(X_test)
print(predictions)

filename = 'finalized_model.sav'
pickle.dump(mlp, open(filename, 'wb'))
 
# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, y_test)
print(result)


from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test, predictions))