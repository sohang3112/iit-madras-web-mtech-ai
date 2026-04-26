import numpy as np
import scipy
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, MinMaxScaler, RobustScaler
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso, RidgeCV, LassoCV, SGDRegressor # linear model fitted with sgd gradient descent
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedGroupKFold, GridSearchCV
from sklearn.svm import SVC
from matplotlib import pyplot as plt

#region NaiveBayes

scipy.stats.norm.pdf(x, loc=mean, scale=stddev)     # x is numpy array; get probability density function
1/np.sqrt(2 * np.pi * stddev^2) * np.exp(-1/2 * ((x-mean)/stddev)**2)      # or manually calc using PDF formula

# StandardScaler() is NOT necessary before Naive Bayes, Logistic Regression
# NaiveBayes fast training, text classification, interpretable probabilities ; AVOID for highly correlated features
# for large data, worse accuracy usually than logistic regression

# NOTE: it doesn't have .fit_predict() method, so use .fit() and .predict()
GaussianNB().fit(X_train, y_train)           # continous input
# varsmoothing is a small fraction of largest variance to add to each variance for numerical stability (avoid divide by 0)
# GaussianNB(priors=list_of_prior_class_probabilities, varsmoothing=0.01)      
MultinomialNB().fit(X_train, y_train)        # multiple categories input  
BernoulliNB().fit(X_train, y_train)          # binary categories input feautres (yes/no)
# for input with multiple feature types, do .predict_proba() on each feature using appropriate model, then multiply .predict_proba() of each model to get likelihoods
# normalize likelihoods to get probabilities

#endregion NaiveBayes

#region Regression_I_Instructor
ypred = LinearRegression().fit_predict(X, y)  # linear regression: w = (X^T X)^-1 X^T y
plt.plot(ypred, ypred - y)    # Residual Plot: errors vs predicted outputs - the 2 should NOT be correlated
make_pipeline(PolynomialFeatures(degrees=5, include_bias=False), LinearRegression())     # polynomial regressions model

# Gradient Descent: no func in sklearn so code yourself: w -= lr * gradient
# for convex cost function (eg. as in linear regression), initialization doesn't matter all lead to same point. But matters for non-convex.
#endregion Regression_I_Instructor

#region LogisticRegression
# for imbalanced classes, prefer F1 score and ROC-AUC over accuracy
# tune classify threshold based on problems' cost of FP vs FN
# TODO: check for multi-collinearity using correlation matrices
# Use L1 regularization for feature selection (it promotes sparse weights, ie pushes some weights to 0), L2 for stability
# inspect learning rate curves to diagonise under-fitting vs over-fitting
regularization_strength = 2       # select optimal via cross-validation
make_pipeline(StandardScaler(), LogisticRegression(C=1/regularization_strength, max_iter=100, random_state=42))
# TODO: ROC-AUC plot
#endregion LogisticRegression

#region LogReg_Tutorial_Solutions
# l1_ratio: 0 (full L2) - 0.5 (mix) - 1 (full L1)
LogisticRegression(penalty='l1' | 'l2' | 'elasticnet', solver='lbfgs' | 'liblinear' | 'saga' | 'sag' | 'newton-cg', l1_ratio=0 to 1,
                   class_weight=None (default) | 'balanced' | {0: w0, 1: w1} (manually list class index weights),     # handle class imbalance
                   multi_class='auto' | 'ovr' (one vs rest) | 'multinomial' (softmax),   # it's binary classifier by default, can optionally give multi-class strategy
                        # ovr is fast, simple; multinomial preferred when classes not well seperated
                   C=1/regularization_strength, max_iter=1000, random_state=42) 

# cross-validation ensuring proportions of classes preserved
skf = StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf, scoring='accuracy' | 'precision_macro' | 'recall_macro' | 'f1_macro' | etc.)

grid_search = GridSearchCV(model, param_grid={'param1': [...]}).fit(X, y)
best_model = grid_search.best_estimator_
print('best params:', grid_search.best_params_)
#endregion

#region Gradient_Descent_Feature_Scaling
# gradient descent (batch | sgd | min-batch), lr schedule (momentum | rmsprop | adam) - no sklearn method, manually impl
# scaling techniques: z-standardize ((x-mu)/sigma), min-max normalize ((x-max)/(max-min)), mean normalize ((x-mu)/(max-min)), robust scaling ((x-Q2)/(Q3-Q1)) [Q=quartiles], log (log(x))
#endregion

#region Ridge_Lasso_Tutorial_Solution
Ridge(alpha=alpha, # alpha is regularization strength: any +ve float ; more alpha means weights more pushed towards 0
      fit_intercept=True, max_iter=None, tol=0.001,   # convergence tolerance)   
      solver='auto' | 'svd' | 'cholesky' | 'lsqr' | 'sag' | 'saga')

Lasso(alpha=alpha, max_iter=50, tol=0.001, selection='cyclic' | 'random', 
      warm_start=False, # reuse previous solution as starting point?
      positive=True)    # force coefficients to be positive?

RidgeCV(alphas=np.logspace(-3,4,100), cv=5).fit(X,y)   # LassoCV   # cross-validation to choose alpha
# unlike ridge, lasso tends to select some arbitary features and set rest's weights to 0; so Lasso excels in sparse feature settings
#endregion

#region SVM_Classification
#SVM needs balanced training data, standardized
#SVM maximizes Margin: distance between HyperPlane and Support Vectors (nearest data points). Kernel Trick maps data to a higher dimensional space to make it linearly seperable.
Xscaled = StandardScaler().fit_transform(X)
SVC().fit(Xscaled, y)

# Kernels (note: here x,y --> x, y are feature vectors; assuming single input single output model)
# * linear K(x,y) = x^T y
# * RBF (Radial Basis Function): default: exp(-gamma |x-y|^2) [gamma is hyperparam, can pass in SVC(gamma=gamma)]
# * Polynomial: (gamma x^T y + r)^d  [gamma, degree are hyperparams]
# * Sigmoid (gamma, r are hyperparams -- LEAST USED)
#endregion