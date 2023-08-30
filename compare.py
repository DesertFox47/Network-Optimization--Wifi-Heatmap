from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC, NuSVC, SVC
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression, SGDClassifier
from sklearn.ensemble import BaggingClassifier, ExtraTreesClassifier, RandomForestClassifier
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
import glob
import os
all_files = glob.glob(os.path.join("./traindataset", "*.csv"))
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
    print("Loaded -- "+filename)
frame = pd.concat(li, axis=0, ignore_index=True)
print("Concatinated")
data = frame.values
X = data[:,2:8]
y = data[:,9]
models = [
    SVC(),
    SGDClassifier(n_jobs=-1), 
    KNeighborsClassifier(n_jobs=-1),
    BaggingClassifier(n_jobs=-1), 
    ExtraTreesClassifier(n_jobs=-1),
    RandomForestClassifier(n_jobs=-1)
]
print("Loaded models")
modelname=[]
accuracy=[]
traintime=[]
f, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 5), sharex=True)
def score_model(X, y, estimator):
    print("Training -- "+model.__class__.__name__)
    X_train, X_test, y_train, y_test = train_test_split(
             X, y, test_size = 0.2, random_state=42)
    start = time.time()
    model.fit(X_train, y_train)
    stop = time.time()
    modelname.append(model.__class__.__name__)
    accuracy.append(model.score(X_test, y_test))
    traintime.append(stop - start)

for model in models:
    score_model(X, y, model)

print(modelname)
print(traintime)
print(accuracy)
sns.barplot(x=modelname, y=accuracy, palette="rocket",ax=ax1)
ax1.axhline(0, color="k", clip_on=False)
ax1.set_ylabel("Accuracy")
sns.barplot(x=modelname, y=traintime, palette="rocket",ax=ax2)
ax2.axhline(0, color="k", clip_on=False)
ax2.set_ylabel("Time Taken to train")
plt.show()