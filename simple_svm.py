import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
from sklearn.datasets import load_digits, fetch_openml, load_boston
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler
from numpy import zeros
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from numpy.random import rand
import numpy as np
from numpy import linspace
from math import sqrt


# playing around with the toy digits dataset
digits = load_digits()
digits.images[0]
plt.gray()
plt.cla()
plt.matshow(digits.images[4])
digits.data

X2 = sm.add_constant(X) # what intercept as well
model = sm.OLS(y, X2)
model2 = model.fit()
print(model2.summary())
#
#    :Attribute Information (in order):
#        - x1 CRIM     per capita crime rate by town
#        - x2 ZN       proportion of residential land zoned for lots over 25,000 sq.ft.
#        - x3 INDUS    proportion of non-retail business acres per town
#        - CHAS     Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
#        - NOX      nitric oxides concentration (parts per 10 million)
#        - RM       average number of rooms per dwelling
#        - AGE      proportion of owner-occupied units built prior to 1940
#        - DIS      weighted distances to five Boston employment centres
#        - RAD      index of accessibility to radial highways
#        - TAX      full-value property-tax rate per $10,000
#        - PTRATIO  pupil-teacher ratio by town
#        - B        1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
#        - LSTAT    % lower status of the population
#        - MEDV     Median value of owner-occupied homes in $1000's

X,y = load_boston(return_X_y=True)
X.shape
y
model = LinearRegression()

model.fit(X, y)
100*model.coef_
# so we have ten classes. each pixel is a feature so 28^2 = 784 features. for each class, we have a parameter vector \beta 
# we think of each image as a sample of 784 random variables (one random variable for each feature). Thus \beta . X where X is nx28^2 matrix of samples. The \beta for each class is thus itself an image that is "orthogonal" to the images in its class?
# in terms of matrices, how do we write the dot product (thinking of semidefinite optimization here from the summer)? Should be equivalent to vectorizing and then tating the dot product.
# how can we see logistic regression as doing SVM but with a different cutoff function?
X,y = fetch_openml('mnist_784', version=1, return_X_y=True)
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=.20)
# why do they standardize things? and do we standardize within class or across whole data set?


plt.matshow(X[0].reshape(28,28))
y[0]
X = zeros((20, 2))

X[:10, :] = rand(10, 2) * 4 + 1 
X[10:, :] = (rand(10, 2) * 4 + 1 )
X[10:, 1] = -X[10:, 1]
Y = zeros(20)
Y[:10] = 1
Y[10:] = 0
colors = ["red" ]* 10 + ["blue"] * 10

model = LinearSVC(C=50.0/60000, tol=.1)
model.fit(Xtrain, ytrain)

Xtrain.shape
# try the same model but with logistic classifier
# where did they get that it should be proportional to 1/# of training samples?
# what does the intercept mean here?
model = LogisticRegression(C = 50.0/60000, solver='saga', tol=.1, penalty='l1')
model.fit(Xtrain,ytrain)

# now we render the coefficient images that we found
plt.cla()
coeffs = model.coef_.copy()
for i in range(coeffs.shape[0]):
	p = plt.subplot(2,5, i + 1)
	p.matshow(coeffs[i].reshape(28, 28))
	p.set_xticks(())
	p.set_yticks(())
	p.set_xlabel('Class %i' % i)
plt.show()
X.shape
# why do they standardize the test data and not the train data? does logistic regression need standardization?

# or do it their way by scaling 
# it seems that scaling decreases the score of the model. weird
scalar = StandardScaler()
Xtrain = scalar.fit_transform(Xtrain)
Xtest = scalar.transform(Xtest)

model.score(Xtest, ytest)
model.predict_proba(np.array([[1, -1]]))

plt.cla()
# here we plot the decision hyperplane
xx, yy = np.meshgrid(linspace(0, 6, 100), linspace(-4, 4, 200))
xy = np.vstack([xx.ravel(), yy.ravel()]).T
# what does the decision function mean for logistic regression?
zz = model.decision_function(xy).reshape(xx.shape)
np.linalg.norm(beta)
# why are these levels important?
plt.cla()
plt.contour(xx,yy,zz, levels = [-np.linalg.norm(beta), 0,np.linalg.norm(beta)])
plt.scatter(X[:, 0], X[:, 1], c=Y)

# we could use this I suppose, but easier to just call decision_function
# so how do we compute the margin? is |beta| with the intercept or without?
# almost looks like that from the graph. but not quite. what does the zero level set correspond to?  the mean? can we recover linear regression through some limit?
# what is the hyperplane in logistic regression? 

# In 2D, I have to imagine the smoothed 2D step function from 0 to 1 (so we are smoothly interpolating between classes). SVM is the hard cutoff (nonsmooth). Can you recover svm as limiting of logistic regression? SVM cannot recover logistic regression I think.

# new goal: classify digits using first logistic and then SVM

# when we view regression in terms of weighted averages, what is the weighting function?
beta = np.hstack([model.coef_[0], model.intercept_[0]])

model.predict(np.array([[1, 4]]))

plt.cla()
