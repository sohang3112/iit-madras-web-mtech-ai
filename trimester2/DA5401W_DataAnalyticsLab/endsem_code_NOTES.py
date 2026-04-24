import numpy as np
import scipy
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.multiclass import OneVsRestClassifier
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