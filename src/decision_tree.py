from sklearn import tree
from sklearn.datasets import load_iris
import numpy as np
import matplotlib.pyplot as plt

X, y = load_iris(return_X_y=True)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y)

petal_and_sepal = X[:, [0, 1]]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(petal_and_sepal, y)
x_min, x_max = petal_and_sepal[:, 0].min() - 1, petal_and_sepal[:, 0].max() + 1
y_min, y_max = petal_and_sepal[:, 1].min() - 1, petal_and_sepal[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, .02), np.arange(y_min, y_max, .02))
zz = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
plt.cla()
plt.contourf(xx,yy, zz, cmap=plt.cm.RdYlBu)

iris = load_iris()
clf.predict_proba([[2,1,0,2]])
X.shape
tree.plot_tree(clf)
X[0]
iris.target_names
plot_colors = "ryb"
petal_and_sepal[0]
for i, color in enumerate(plot_colors):
	idx = np.where(y == i)
	plt.scatter(petal_and_sepal[idx, 0], petal_and_sepal[idx, 1], c=color, cmap=plt.cm.RdYlBu, s=15)
