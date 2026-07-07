# CH54402 - Multi Variate Analysis

Suggested Book: *Kutner, M. H., C. J. Nachtschiem, J. Netner, Applied Linear Regression Models. 4th ed. New Delhi: McGraw Hill, 2004*

## Day 1: Linear Regression

$Y$ is ground truth, $\beta$ is weights.

Error $\epsilon = Y - X \beta$, so (mean-squared error aka Sum of Squared Errors (SSE)) loss $L = \epsilon^T \epsilon = Y^T Y - Y^T X \beta + \beta^T X^T X \beta$ -- optimal weights satisfy $\frac{\partial L}{\partial \beta} = 0$.

Regression to the Mean

$Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \epsilon$, where $\beta_0$ is intercept and $\beta_1, \beta_2$ are **partial regression coefficients** (partial because beta 1,2 correspond to change in X1, X2 only when other variable is kept constant).

$Y = X \beta + \epsilon$ -- matrix form

least squares solution: $\beta = (X^T X)^{-1} X^T y$

NEW --> covariance matrix of weights $C = Cov(\beta, \beta) = (X^T X)^{-1} \sigma^2$ where $\sigma^2$ is noise aka variance of error in matrix equation $Var(\epsilon)$
* covariance matrix of weights $C$ is *symmetric matrix* since $X^T X$ is symmetric
* true $\sigma^2$ is unknown, so we must estimate it: $hat{\sigma}^2 = SSE / (n-p)$ where $n$ is no. of samples/rows, $p$ is no. of parameters/weights (size of covariance matrix of weights)
* **Estimated Standard Error** (after using this estimate of error variance) is $SE[\hat{\beta_j}] = \sqrt{\hat{\sigma}^2 C_jj}$. Small errors for good precision.

TODO

## Lecture 2

TODO

## Lecture 3

TODO

## Lecture 4

TODO

## Lecture 5

SUM[(y - y_{pred})^2] = TODO 

sum of all deviations (from mean) = 0 [for linear regression solution line]

TODO

## Lecture NOT_SURE_NUMBER -- Chi Square Distribution and Mahalanobis Distance

$$(x - \mu)^T \Sigma^{-1} (x - \mu) \le \chi^2 (\alpha) \quad \text{with probability} 1-\alpha$$

- In chi-squared distribution with $p$ degrees of freedom, standard $100 (1 - \alpha)$ 'th percentile means area of $1 - \alpha$ lies to left (below) the $\chi^2 (\alpha)$ curve.
- value of $d^2$ at $100 (1 - \alpha)$ 'th percentile represents all multivariate observations of X such that $100 (1 - \alpha) %$ lie below cuve and each obsevation has squared distance less than or equal: $d^2 \le \chi^2 (\alpha)$ .

TODO