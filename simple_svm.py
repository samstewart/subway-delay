import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
from numpy import zeros
from numpy.random import rand
import numpy as np
from numpy import linspace

X = zeros((20, 2))
X[:10, :] = rand(10, 2) * 4 + 1 
X[10:, :] = (rand(10, 2) * 4 + 1 )
X[10:, 1] = -X[10:, 1]
Y = zeros(20)
Y[:10] = 1
Y[10:] = 0
colors = ["red" ]* 10 + ["blue"] * 10

model = LinearSVC(C=1000)
X
Y.shape
model.fit(X, Y)

plt.cla()
# here we plot the decision hyperplane
xx, yy = np.meshgrid(linspace(0, 6, 100), linspace(-4, 4, 200))
xy = np.vstack([xx.ravel(), yy.ravel()]).T
zz = model.decision_function(xy).reshape(xx.shape)
# why are these levels important?
plt.contour(xx,yy,zz, levels = [-1, 0, 1])
plt.scatter(X[:, 0], X[:, 1], c=colors)

# we could use this I suppose, but easier to just call decision_function
model.coef_[0]
model.intercept_[0]


model.predict(np.array([[1, 4]]))

plt.cla()
