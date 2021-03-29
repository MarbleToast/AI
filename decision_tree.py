# %%
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from sklearn import metrics

# Load data from csv
data = pd.read_csv("data.csv")
data = data.groupby('most_present_age')
data = pd.DataFrame(data.apply(lambda x: x.sample(data.size().min()).reset_index(drop=True)))

# Split the data into training and testing sets
features = data.drop(
    [
        "cell_id",
        "Buildings:total",
        "LandUse:Mix",
        "ThirdPlaces:cv_count",
        "most_present_age",
    ],
    axis=1,
)
prediction_classes = data["most_present_age"]
feature_train, feature_test, prediction_train, prediction_test = train_test_split(
    features, prediction_classes, test_size=0.3, random_state=0
)

# calculate accuracy for varying depth of the tree and see how it changes
scores = []
for d in range(1, 100):
    dtc = DecisionTreeClassifier(max_depth=d)
    clf = dtc.fit(feature_train, prediction_train)
    scores.append([d, clf.score(feature_test, prediction_test)])

scores = np.array(scores)
fig1 = plt.figure()
ax = fig1.add_subplot(1, 1, 1)

plt.plot(scores[:, 1], color="red")
plt.title("Classifier accuracy score with respect to the maximum node depth")
plt.xlabel("Max depth")
plt.ylabel("Accuracy score %")
plt.xticks(range(0, 110, 10))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

classes = [
    "age_under_18",
    "age_20_30",
    "age_30_40",
    "age_40_50",
    "age_50_60",
    "age_over_60",
]

# plot confusion matrix on predictions
dtc = DecisionTreeClassifier(max_depth=4)
clf = dtc.fit(feature_train, prediction_train)
prediction = clf.predict(feature_test)
plt.figure()
plot_tree(clf, feature_names=feature_train.columns, class_names=classes)

confusion = metrics.confusion_matrix(prediction_test, prediction, normalize="true")

plt.figure(figsize=(9, 9))
sns.heatmap(
    confusion,
    annot=True,
    yticklabels=classes,
    xticklabels=classes,
    fmt=".3f",
    linewidths=0.5,
    square=True,
    cmap="rainbow",
    vmin=0,
    vmax=1,
)
plt.ylabel("Actual age class")
plt.xlabel("Predicted age class")

plt.title(
    f"Accuracy: {clf.score(feature_test, prediction_test)*100}%", size=15
)

for importance, name in sorted(
    zip(clf.feature_importances_, feature_train.columns), reverse=True
):
    print(f"'{name}': {importance*100}%")

# %%
