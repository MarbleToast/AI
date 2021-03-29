# %%

from sklearn.datasets import load_digits
from sklearn.metrics import pairwise_distances_argmin
from sklearn.decomposition import PCA
from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np

digits = load_digits()

data_pca = PCA(n_components=2).fit_transform(digits.data)


def k_means(data, n, random_state=1):
    rand = np.random.RandomState(random_state)
    centres = data[rand.permutation(data.shape[0])[:n]]

    while True:
        updated_centres = np.array(
            [data[digits.target == cluster].mean(axis=0) for cluster in range(n)]
        )
        if np.all(centres == updated_centres):
            break
        centres = updated_centres

    return centres, labels


centres, labels = k_means(data_pca, 10)

plt.figure(figsize=(9, 9))

for i in range(data_pca.shape[0]):
    plt.text(
        data_pca[i, 0],
        data_pca[i, 1],
        str(labels[i]),
        color=plt.cm.jet(labels[i] / 10),
    )


plt.scatter(
    centres[:, 0], centres[:, 1], s=100, linewidths=3, marker="o", color="black"
)

accurate = 0
for i in range(len(labels)):
    if digits.target[i] == labels[i]:
        accurate += 1
print(f"{(accurate/len(labels))*100}% correct.")

plt.title(
    "$\it{k}$-means clustering on PCA-reduced digits dataset\nCentres are denoted by black circle",
    y=1.2,
)
plt.xticks([])
plt.yticks([])
plt.axis("off")
plt.show()
