# ML Syllabus

## Module 1: Unsupervised Learning
* Estimation: Review of MLE, Bayesian optimization
* Dimensionality Reduction
* Clustering - K-means, Heirachical clustering, Spectral clustering

## Module 2: Supervised Learning
* Functional Approximations and regression
* Regression
* Linear Regression: Ordinary Least Squares, PCR (Principal Components Regression = PCA before LinearRegression)
* Non-Linear Regression (bias functions)
* Ridge Regression, LASSO

## Module 3: Binary Classification
* k-Nearest Neighbours
* Decision trees, CART
* Bias-Variance dichotomy, Model validation - Cross validation
* Bayesian Decision theory -- superset (theory) of Naive Bayes (practical); whereas Naive Bayes assumes all features are conditionally independent, Bayes Nets (not in syllabus) allow to specify which features are conditionally independent with each other
* Generative vs Discriminate Modeling for classification -- TODO: both meanings? i assume it's prior assumption made
    * Generative
        * Naive Bayes, Gaussian Discriminant analysis
        * Hidden Markov model -- TODO: NOT TAUGHT, is it coming??
    * Discriminative -- which ones exactly? is it just everything besides naive bayes
* Logistic Regression

## Module 4: Advanced Methods of Classification
* Support Vector Machines - Kernels
* Ensemble methods
    * Bagging - Random Forest
    * Boosting - Adaboost / GBDT / XgBoost
    * Artificial Neural Networks
    * multi-class classification - one vs all vs one vs one

## Module 5: Sequential Decision making - TODO: NOT TAUGHT, is it coming??
* Online learning
* Bandit problem
* Reinforcement learning

-----------

Quiz 1 Topics:

- [x] MLE
- [x] MOM
- [x] PCA Dimensionality Reduction
- [x] Covariance
- [x] K-means clustering
- [x] DBSCAN clustering
- [x] Heirachical: Agglomerative clustering
- [ ] Spectral clustering

------------

Quiz 2 Topics:

- [x] Supervised Learning Workflow: Identify X, y, metric > Collect data > Pre-process > Choose Model type > Feature Engineering > Training > Validate > Select Best Model > Deploy
- Classification:
    - [x] KNN
    - [x] Naive Bayes
    - [x] Logistic Regression
    - [x] Classification metrics: 
        * accuracy, 
        * precision = TP / (TP + FP) (what % of predicted + are correct?)
        * recall / sensitivity / true positive rate (TPR) = TP / (TP + FN) (what % of actual + are correct pred?)
        * 2/f1 = 1/precision + 1/recall
        * specificity = TN / (TN + FP) (what % of actual - are correct?)
        * balanced accuracy = (specificity + sensitivity) / 2
        * ROC (Reciever Operating Characterstic) curve: plot TPR vs FPR (1-TPR) while varying threshold between 0-1 -- AUC = area under this curve, best threshold can be to maximize **J = TPR - FPR = Sensitivity + Specificity - 1** (choose closest point to top left (FPR=0, TPR=1))
- Regression
    - [x] Ordinary Least Squares $w = (X^T X)^{-1} X^T y$ ; Assumptions: $E[error] = 0$, error is Normal, $CovarianceMatrix[x,y] = \sigma^2 I$ i.e. error is *homoscedatic* (same variance for all observations), features are independent
    - [x] Total Least Squares: z-standardize > augmented [ X | y] > SVD U S V^T > [ vX | vy ] = right vec of smallest eigenval > w = - vX / vy ;
            corrected train [ X | y ] = *low-rank approx till $D$ (rank = no. of eigenvals)* = $\sum_{i=1}^D u_i \sigma_i v_i^T$
    - [x] Logarithmic $\ln(x)$, Exponential $\ln(y)$, Polynomial Regression
    - [x] Multi-variate regression (2 cases: outputs $y$ are independent or dependent among each other)
    - [x] Regression Metrics: Mean Squared Error, Mean Absolute Error, R^2
    - Weighted Linear Regression (when error variance differs across observations):
        - [x] Weighted OLS: objective $\min_w \sum_i (y_i - \hat{y_i})^2 / \sigma$, weights $w = (X^T \Sigma^{-1} X)^{-1} X^T \Sigma^{-1} X y$ 
              where $\Sigma = diag([\sigma_1^2, \sigma_2^2 ...])$ is covariance matrix (non-diagonal 0 of course because features are independent so no covariance)

              Iterative Re-weighting: when true variances not known, we first find standard OLS solution, then estimate $\sigma_i^2 = (y_i - \hat{y_i})^2$, estimate weights using weighted OLS formula, repeat
        - [x] Weighted TLS (initial $X_{aug} = \Sigma^{-1/2} [ X | y ]$, final corrected reverse by multiply with $\Sigma^{1/2}$) where $\Sigma = diag([(y_i - \hat{y_i}^2)])$
    - [x] Regression with Gradient Descent (gradient descent update, with derivative of loss (MSE))
    - Regression with Regularization: 
      - [x] Ridge (L2, direct formula)
      - [ ] Lasso (L1) -- solve iteratively by Coordinate Descent
      ~~ - [ ] Bayesian Linear Regression -- SKIP: NOT COMING IN QUIZ 2 ~~
    - [x] Non-Linear Regression -- no manual way, use a non-linear least-squares solver like those in Scipy to minimize objective (MSE)
- [x] Bias-Variance calculation, esp in various Regression models $MSE = Bias^2 + Variance + IrreducibleError$ where $Bias = E[\hat{y}] - y_{true}$
- [x] Validation: Hold-out, K-Fold Cross Validation, Leave-one-out Cross Validation
- [x] Feature Selection: Recursive (start with all, rm least important), Sequential (start with subsets, merge in iterations) -- *expensive but better than LASSO*

Quiz 2 Tutorials:

- [x] Tutorial 5 - Linear Regression
- [x] Tutorial 6 - Classification
- [x] Tutorial 7 - Linear Regression
- [x] Tutorial 9 - Naive Bayes

-----------

Topics after Quiz 2:

- [ ] Neural Networks: Gradient Descent: Batch, SGD, Mini-Batch
- [ ] Hyperparam tuning, Batch Norm, Regularization
- [ ] Decision Tree, Random Forest
- [ ] Boosting: AdaBoost, XGB, LGBM, CAt Boost
- [ ] Caliberation

**NOTE**: SVM, Reinforcement Learning lecture slides were shared but they are NOT coming in exam.

TODO derivations:
- [ ] Adaboost
- [ ] PCA 
- [ ] Derivative of sigmoid
- [ ] Tanh to sigmoid and back
- [ ] Derivation of ols estimator for simple linear regression

TODO: FML Quiz 1, Quiz 2 -- practice questions where I got wrong answers