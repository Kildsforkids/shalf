import pickle
from sklearn.ensemble import RandomForestClassifier

file_name = 'finalized_model.sav'

with open(file_name, 'rb') as file:
    rand_forest = pickle.load(file)


def predict(x):
    return int(rand_forest.predict([x])[0])