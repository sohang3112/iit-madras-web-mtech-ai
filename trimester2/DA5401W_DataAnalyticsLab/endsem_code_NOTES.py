import numpy as np
import scipy
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB

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