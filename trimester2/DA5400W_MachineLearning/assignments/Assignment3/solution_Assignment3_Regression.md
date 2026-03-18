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

$$
x_{1,true}, x_{2,true} \sim \mathcal{N}(0,1^2) \\
y_{true} = 3 x_{1,true} - 2 x_{2,true}
$$

However, the observed variables are corrupted with measurement noise:

$$x_1 = x_{1,true} + \epsilon_1, \quad x_2 = x_{2,true} + \epsilon_2, \quad y = y_{true} + \epsilon_y$$

where $\epsilon_1, \epsilon_2 \sim \mathcal{N}(0, 0.5^2), \quad \epsilon_y \sim \mathcal{N}(0, 0.2^2)$

Generate $N = 200$ samples.

1. Fit a multiple linear regression model using Ordinary Least Squares (OLS). Report the estimated coefficients.
2. Implement Total Least Squares (TLS) using Singular Value Decomposition (SVD) and report the TLS coefficient estimates.
3. Compare OLS and TLS estimates with the true parameters $(3,-2)$. Which method is closer to the true parameters? Explain.

### Solution 4

TODO: WIP code in notebook (to copy here)


## Problem 5

You are given a dataset *polynomial_regression_dataset.csv* of $N = 300$ observations $(x_i, y_i)$ where the response $y$ is generated from a nonlinear function with noise:

$$y = f(x) + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2)$$

but the form of $f(.)$ is unknown.

1. Split the dataset into a training set (70%) and a validation set (30%).
2. For polynomial degrees $d \in 1,2..10$, fit a polynomial regression model (without regularization) using the training data. 
   For each $d$, compute the Mean Squared Error (MSE) on both the training and validation sets. 
   Plot the training and validation MSE as functions of $d$, and use the plot to select an appropriate degree $d^*$ that balances underfitting and overfitting.
3. For the chosen degree $d^*$, fit the following regularized polynomial models using the training data 
   (Use K-fold cross-validation on the training set to select the best $\lambda$ for each method.):
    * Ridge regression with $\lambda \in \{10^{-4}, 10^{-3}, 10^{-2}, 10^{-1}, 1, 10\}$
    * Lasso regression with $\lambda \in \{10^{-4}, 10^{-3}, 10^{-2}, 10^{-1}, 1, 10\}$
4. For each method above (Ridge, Lasso), report:
    - The selected $\lambda$
    - Training MSE and cross-validation MSE
    - Validation set MSE using the final model
    - Estimated model coefficients
5. Based on your results:
    * Which regularization method performs best on the validation set? Explain why.
    * Does regularization improve generalization relative to the unregularized polynomial model? Justify using the plots and error values.
    * Discuss how the chosen regularizer affects model complexity and coefficient estimates.

### Solution 5

TODO


## Problem 6

**Note:** Solve this problem manually using a calculator but do not use code. 
          Your submission should include manual calculations.
          Feel free to approximate the values to 2 or 3 decimals.

A company is studying how *monthly online sales* $S$ (in units) change with *monthly ad spend* $A$ (in lakhs of rupees). 
Management believes that the effect of ad spend is best described in terms of *percentage change in sales* rather than absolute change.

For the last 5 months, the data are:

$A$ (lakhs) | 1   | 2   | 3   | 4   | 5
----------- | --- | --- | --- | --- | ---
$S$ (units) | 200 | 270 | 330 | 390 | 440

1. Using the above data, estimate a model that makes the relationship between $A$ and $S$ *approximately linear* when the output is expressed in *percentage terms* .
2. Using your fitted model, estimate the *approximate percentage increase in sales* when ad spend increases $A$ from 2 lakhs to 3 lakhs .
3. Is the model implying a *constant percentage gain per lakh* or a *diminishing percentage gain per lakh* ? Justify your answer.

### Solution 6

TODO


## Problem 7

Consider the simple linear regression model:

$$y = w_0 + w_1 x$$

Given $N$ samples of data, the Ordinary Least Squares (OLS) estimator minimizes the sum of squared residuals:

$$ SSR = \sum_{i=1}^N (y_i - w_0 - w_1 x_i)^2 $$

to estimate the parameters.

1. Derive the first-order conditions by differentiating $SSR$ with respect to $w_0$ and $w_1$ and setting the derivatives equal to zero.
2. Using the result from part 1, show that the OLS estimator of the slope is

$$ \beta_1 = \frac{\sum_{i=1}^N (x_i - \bar{x}) (y_i - \bar{y})}{\sum_{i=1}^N (x_i - \bar{x})^2} $$

### Solution 7

TODO


