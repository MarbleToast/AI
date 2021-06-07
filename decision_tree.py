# %%
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif
from sklearn.tree import DecisionTreeClassifier, plot_tree
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from sklearn import metrics
import os

# Load data from csv
data = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "weekend.txt"))

# Split the data into training and testing sets
features = data.drop(
    [
        "Outcome",
    ],
    axis=1,
)
prediction_classes = data["Outcome"]
feature_train, feature_test, prediction_train, prediction_test = train_test_split(
    features, prediction_classes, test_size=0.3, random_state=0
)

classes = [
    "Liked",
    "Not liked",
]

# plot confusion matrix on predictions
dtc = DecisionTreeClassifier(criterion="entropy", max_depth=4)
clf = dtc.fit(feature_train, prediction_train)
prediction = clf.predict(feature_test)
plt.figure()
plot_tree(clf, feature_names=feature_train.columns, class_names=classes)


# %%
