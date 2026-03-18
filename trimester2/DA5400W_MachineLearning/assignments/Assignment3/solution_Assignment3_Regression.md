---
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

# FML Assignment 3 (Regression)

Submitted by: Sohang Chopra &lt;DA25M622&gt;

## Problem 1

Which of the following equations can be reformulated as linear regression models, treating ( _x, y_ )
as variables and ( _a, b_ ) as parameters? For each valid case, show the algebraic transformation that
converts the equation into linear regression form.

1. $y = a e^{b x}$
2. $y = \frac{a x}{b + x}$
3. $y = \frac{a}{x + b}$
4. $y = a (1 - e^{-b x})$

### Solution 1

1. Can be transformed into linear form: $\hat{y} = b x + \ln(a)$ where transformed $\hat{y} = \ln(y)$
2. Can be transformed into linear form: $\hat{y} = \frac{b}{a} \hat{x} + \frac{1}{a}$ where transformed $\hat{x} = \frac{1}{x}, \hat{y} = \frac{1}{y}$
3. Can be transformed into linear form: $\hat{y} = \frac{1}{a} \hat{x} + \frac{b}{a}$ where transformed $\hat{x} = \frac{1}{x}, \hat{y} = \frac{1}{y}$
4. Cannot be transformed into a linear form such that transformed x, y are independent of a, b


## Problem 2

Data on the monthly sales (y) in rupees and advertising spend (x) in rupees for 25 retail stores were collected. 
The mean and covariance matrix (about the mean) computed from the data is given:

$$z = \begin{pmatrix} y \\ x \end{pmatrix}, \quad \bar{z} = \begin{pmatrix} 200 \\ 400 \end{pmatrix}, \quad S_z = \begin{pmatrix} 1800 & 900 \\ 900 & 500 \end{pmatrix}$$

Assume a linear relation $y = a x + b$ exists between monthly sales $y$ and advertising spend $x$.
Compute the model parameters using OLS approach.

### Solution 2

Standard Deviations of x, y are $s_x = \sqrt{1800} = 90, s_y = \sqrt{500}$ and covariance is $cov(x,y) = 900$

$$
r = cov(x,y) / s_x s_y \quad (\text{Regression Coefficient}) \\
a = r s_y / s_x = cov(x,y) / s_x^2 = 900 / 1800 = 0.5 \\
b = \bar{y} - b \bar{x} = 400 - 0.5 * 200 = 300 \\
$$

So linear relationship is $y = 0.5 x + 300$


## Problem 3

We need to find a relationship between the saturated pressure $P_{sat}$ and the saturated temperature $T$ (boiling point) of a substance called n-hexane. 
The data provided in the linked file *vpdata.csv* contains measurements of saturated pressure and corresponding temperature for n-hexane, where the first column represents the temperature (in $K$) and the second column represents the pressure (in $kPa$). 
Theoretically, there is an equation called Clausius-Clapeyron equation which models the relationship between $P_{sat}$ and $T$, and is given by

$$\ln(P_{sat}) = A - \frac{B}{T}$$

Assuming that temperature measurements are noise-free and pressure measurements are noisy, do the following:

1. Use regression to obtain estimates of parameters $A$, $B$ .
2. Find maximum absolute error in predicting pressure in $kPa$ ?
3. What is $R^2$ score for the regression model?

### Solution 3

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

df = pd.read_csv('vpdata.csv')

# fit model
xtransformed = (-1 / df['Temp']).to_frame()
ytransformed = np.log(df['Psat']).to_frame()
linreg = LinearRegression().fit(xtransformed, ytransformed)
print(linreg.coef_, linreg.intercept_)     # A, B

# evaluate
ypred = np.squeeze(linreg.predict(xtransformed))
ypred = np.exp(ypred)      # transformed space -> original space
print('Max Absolute Error:', np.max(np.abs(ypred - df['Temp'])))
print('R^2 Score:', r2_score(df['Temp'], ypred))
```

1. $A = 30.16773335$, $B = 4.53017516$
2. Max Absolute Error in predicting pressure = $7.849209255771072$ kPa
3. $R^2 = 0.9450108107197727$

## Problem 4

Consider the following data-generating process:

_x_ 1 _,_ true _∼N_ (0 _,_ 1) _,_ _x_ 2 _,_ true _∼N_ (0 _,_ 1) _,_

_y_ true = 3 _x_ 1 _,_ true _−_ 2 _x_ 2 _,_ true

However, the observed variables are corrupted with measurement noise:

_x_ 1 = _x_ 1 _,_ true + _ϵ_ 1 _,_ _x_ 2 = _x_ 2 _,_ true + _ϵ_ 2 _,_ _y_ = _y_ true + _ϵy_

where

_ϵ_ 1 _, ϵ_ 2 _∼N_ (0 _,_ 0 _._ 5 [2] ) _,_ _ϵy ∼N_ (0 _,_ 0 _._ 2 [2] ) _._

Generate _N_ = 200 samples.


(a) Fit a multiple linear regression model using Ordinary Least Squares (OLS). Report the estimated coefficients.


(b) Implement Total Least Squares (TLS) using Singular Value Decomposition (SVD) and report
the TLS coefficient estimates.


(c) Compare OLS and TLS estimates with the true parameters (3 _, −_ 2). Which method is closer
to the true parameters? Explain.

### Solution 4

TODO


## Problem 5

You are given a dataset of](https://drive.google.com/file/d/1VZy0HNLmtSPQiLIKlW7Gfi3S0vbIzcCk/view?usp=sharing) _N_ = 300 observations ( _xi, yi_ ) where the response _y_ is generated from a
nonlinear function with noise:

_y_ = _f_ ( _x_ ) + _ϵ,_ _ϵ ∼N_ (0 _, σ_ [2] ) _,_

but the form of _f_ ( _·_ ) is unknown.

(a) Split the dataset into a training set (70%) and a validation set (30%).


(b) For polynomial degrees _d ∈{_ 1 _,_ 2 _,_ 3 _,_ 4 _,_ 5 _,_ 6 _,_ 7 _,_ 8 _,_ 9 _,_ 10 _}_, fit a polynomial regression model (without regularization) using the training data. For each _d_, compute the Mean Squared Error
(MSE) on both the training and validation sets. Plot the training and validation MSE as
functions of _d_, and use the plot to select an appropriate degree _d_ _[∗]_ that balances underfitting
and overfitting.

(c) For the chosen degree _d_ _[∗]_, fit the following regularized polynomial models using the training
data:

i. Ridge regression with _λ ∈{_ 10 _[−]_ [4] _,_ 10 _[−]_ [3] _,_ 10 _[−]_ [2] _,_ 10 _[−]_ [1] _,_ 1 _,_ 10 _}_
ii. Lasso regression with _λ ∈{_ 10 _[−]_ [4] _,_ 10 _[−]_ [3] _,_ 10 _[−]_ [2] _,_ 10 _[−]_ [1] _,_ 1 _,_ 10 _}_


Use _K_ -fold cross-validation on the training set to select the best _λ_ for each method.


(d) For each method above (Ridge, Lasso), report:


     - The selected _λ_

     - Training MSE and cross-validation MSE

     - Validation set MSE using the final model

     - Estimated model coefficients


(e) Based on your results:


i. Which regularization method performs best on the validation set? Explain why.

ii. Does regularization improve generalization relative to the unregularized polynomial model?
Justify using the plots and error values.

iii. Discuss how the chosen regularizer affects model complexity and coefficient estimates.

### Solution 5

TODO


## Problem 6

**Note:** Solve this problem manually using a calculator but do not use code. You submission should
include manual calculations. Feel free to approximate the values to 2 or 3 decimals.

A company is studying how _monthly online sales S_ (in units) change with _monthly ad spend A_ (in
lakhs of rupees). Management believes that the effect of ad spend is best described in terms of
_percentage change in sales_ rather than absolute change.

For the last 5 months, the data are:


_A_ (lakhs) 1 2 3 4 5
_S_ (units) 200 270 330 390 440


(a) Using the above data, estimate a model that makes the relationship between _A_ and _S approx-_
_imately linear_ when the output is expressed in _percentage terms_ .


(b) Using your fitted model, estimate the _approximate percentage increase in sales_ when ad spend
increases from
_A_ = 2 lakhs to _A_ = 3 lakhs _._


(c) Is the model implying a _constant percentage gain per lakh_ or a _diminishing percentage gain per_
_lakh_ ? Justify your answer.

### Solution 6

TODO


## Problem 7

Consider the simple linear regression model:


_y_ = _w_ 0 + _w_ 1 _x,_



Given _N_ samples of data, the Ordinary Least Squares (OLS) estimator minimizes the sum of squared
residuals:



_SSR_ =



_N_





- ( _yi −_ _w_ 0 _−_ _w_ 1 _xi_ ) [2] _._


_i_ =1



to estimate the parameters.


(a) Derive the first-order conditions by differentiating _SSR_ with respect to _w_ 0 and _w_ 1 and setting
the derivatives equal to zero.


(b) Using the result from part (a), show that the OLS estimator of the slope is


         - _n_
_β_ ˆ1 = _i_ =1 ~~�~~ [(] ~~_n_~~ _[x][i][ −]_ _[x]_ [¯][)(] _[y][i][ −]_ _[y]_ [¯][)] _._
_i_ =1 [(] _[x][i][ −]_ _[x]_ [¯][)][2]

### Solution 7

TODO


