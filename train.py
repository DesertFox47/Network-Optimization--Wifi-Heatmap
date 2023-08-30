from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle
import glob
import os
all_files = glob.glob(os.path.join("./traindataset", "*.csv"))
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
frame = pd.concat(li, axis=0, ignore_index=True)

data = frame.values
X = data[:,2:8]
y = data[:,9]
X_train, X_test, y_train, y_test = train_test_split(
             X, y, test_size = 0.2, random_state=42)


knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(X_train, y_train)
print(knn.score(X_test, y_test))
knnPickle = open('./model/model.pickle', 'wb') 
pickle.dump(knn, knnPickle)

# neighbors = np.arange(1, 100)
# train_accuracy = np.empty(len(neighbors))
# test_accuracy = np.empty(len(neighbors))
# for i, k in enumerate(neighbors):
#     knn = KNeighborsClassifier(n_neighbors=k)
#     knn.fit(X_train, y_train)
#     train_accuracy[i] = knn.score(X_train, y_train)
#     test_accuracy[i] = knn.score(X_test, y_test)
# plt.plot(neighbors, test_accuracy, label = 'Testing dataset Accuracy')
# plt.plot(neighbors, train_accuracy, label = 'Training dataset Accuracy')
# plt.legend()
# plt.xlabel('n_neighbors')
# plt.ylabel('Accuracy')
# plt.show()