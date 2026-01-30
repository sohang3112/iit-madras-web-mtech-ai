--
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

# DA5400W (Foundations of Machine Learning) Assignment 1

Submitted by Sohang Chopra &lt;DA25M622&gt;

## Problem 1

The following probability distribution function can describe the growth rate of finance:

$$f(x) = \frac{1}{\alpha^2} x e^{x / \alpha}$$

with $\alpha \in (0, \infty)$ and $x \in [0, \infty]$. 
Find an estimate of the parameter $\alpha$ using the maximum likelihood
estimators and the method of moments given the datasets $x_1, x_2, \cdots x_n$ .

### Solution

TODO

## Problem 2

Consider a process for which a random sample $X_1, X_2, \cdots X_9$ is collected to understand the population properties. 
The population mean and variance are $\mu$ and $\sigma^2$. 
Mr and Mrs. Stat have proposed two estimators as follows:

$$\theta_{Mr} = \frac{X_1 + X_3 + 4 X_5}{6} , \quad \theta_{Mrs} = \frac{X_2 - X_6 + 2 X_7 + 3 X_4}{5}$$

Which is the best estimator and why?

### Solution

Using $E[aX \pm bY] = a E[X] \pm a E[Y], Var(aX \pm bY) = a^2 Var(X) + b^2 Var(Y)$:

$$
E[\theta_{Mr}] =  \frac{\mu + \mu + 4 \mu}{6} = \mu,         \quad Var{\theta_{Mr}}  = \frac{\sigma^2 + \sigma^2 + 4^2 \sigma^2}{6^2} = 0.5 \sigma^2
E[\theta_{Mrs}] = \frac{\mu - \mu + 2 \mu + 3 \mu}{5} = \mu, \quad Var(\theta_{Mrs}) = \frac{\sigma^2 + \sigma^2 + 2^2 \sigma^2 + 3^2 \sigma^2}{5^2} = 0.6 \sigma^2
$$

Both estimators have same expected value, but $\theta_{Mr}$ has less variance so it's better.

## Problem 3

The probability distribution functions of the Weibull distribution and the Rayleigh distribution are given below:

* Weibull distribution: $f(x; k, \lambda) = \frac{k}{\lambda} (\frac{x}{\lambda})^{k1} e^{(x / \lambda)^k}, \quad x \ge 0$
* Rayleigh distribution: $f(x; ) = \frac{x}{\sigma^2} e^{x^2 / (2 \sigma^2)}, \quad x \ge 0$

Use the dataset [Weibull.csv](https://drive.google.com/file/d/1SNFkOio5wzENCsfCCsamSXxAOSjyaXna/view) provided to estimate the parameter $\lambda$ in Weibull distribution 
using maximum likelihood estimation (MLE) (assume $k = 2$). 
Use the property of invariance of MLE to estimate the parameter  of Rayleigh distribution.

### Solution

TODO

## Problem 4

Find the maximum likelihood estimate of the parameter $\theta$ of the following probability distribution function:

$$f(y; \theta) = \frac{3 y^2}{\theta^3}$$

with $\theta \in (0,\infty)$ and $y \in [0,\infty]$ using the data $y_1, y_2, \cdots y_n$ .

### Solution

TODO

## Problem 5

Dr. AAA collects samples of cancer patients to estimate the mean expression levels of an oncogene.
Due to technical limitations, (s)he can collect only 20 samples per day and measure the expression levels of the oncogene. 
It has been known that the gene expression levels follow normal distribution with standard deviation $8 (\sim \mathcal{N} (\mu, \sigma = 8))$. 
Help him/her in estimating the mean gene-expression value using recursive Bayesian estimation. 
The dataset [Gene_expression.csv](https://drive.google.com/file/d/17EgR8B-3nte1GEQkSytL0StuDZiuL81d/view) provided has gene expression levels
of the oncogene collected for 10 days. 
Do the following:

1. Assume the prior distribution of $\mu$ to be a normal distribution. You can take the sample mean of Day 1 samples and variance as prior parameters.
2. Estimate the posterior distribution of $\mu$ using samples from Day 1.
3. Update the priors and repeat step 2 using data from each of the days.
4. Plot the probability distribution of the mean of gene expression level each time after the update.

### Solution

TODO

## Problem 6

Consider a random variable $C$ with mean $\mu$ and standard deviation $\sigma$. 
Two experiments are performed to collect two random samples with $n_1$ and $n_2$ sample sizes. 
The sample means for these experiments are $C_1$ and $C_2$ . 
Then, show that an estimator for the sample mean:

$$\bar{C} = a \bar{C_1} + (1 - a) \bar{C_2}$$

is an unbiased estimator for the mean $\mu$.

### Solution 

$E[a \bar{C_1} + (1 - a) \bar{C_2}] = a \mu + (1 - a) \mu = \mu = \bar{C}$ : So the given estimator for mean is unbiased, as expected value of estimator equals mean.

## Problem 7

Find the local extrema of the following functions and classify the points as minimum or maximum:

1. $f(x) = 4 x^3 - 3 x^2 + 2 x - 1$
2. $f(x) = sin(x) + cos(x)$
3. $f(x) = \frac{x^2 - 1}{x}$

### Solution

1. $\nabla f = 12 x^2 - 6 x + 2 = 0$ : No real solutions exist for $x$ so no stationary points / extrema exist.

2. 
$$
\nabla f = cos(x) - sin(x) = 0 \implies x = \frac{sin^{-1}(1)}{2} \\
\nabla^2 f = -sin(x) - cos(x) \implies \nabla^2 f(\frac{sin^{-1}(1)}{2}) = - \sqrt{1 + sin(2 x)} = - \sqrt{2}
$$
So one extrema exists: $\frac{sin^{-1}(1)}{2}$ (maxima since $\nabla^2 f > 0$).

3. $f(x) = x - x^{-1}, \quad \nabla f = 1 + x^{-2} = 0$ : No real solutions exist for $x$ so no stationary points / extrema exist.

## Problem 8

Show that the function $f(x_1, x_2) = 8 x_1 + 12 x_2 + x_1^2 - 2 x_2^2$ has only one stationary point and that it is neither a maximum nor a minimum, but a saddle point. 
Sketch the contour line of $f$.

### Solution

$$
\nabla f = \begin{pmatrix} 8 + 2 x_1 \\ 12 - 4 x_2 \end{pmatrix} = 0 \implies (x_1, x_2) = (-4, 3) \\
\nabla^2 f = \begin{pmatrix} 2 & 0 \\ 0 & -4 \end{pmatrix}
$$

Hessian $\nabla^2 f$ is a diagonal matrix so eigenvalues are from diagonal: 2, -4. As one positive and one negative eigenvalue is there, it's an indeterminate matrix.
So stationary point $(-4,3)$ is a saddle point.

## Problem 9

Determine the stationary points and classify their nature for the function $f(x,y) = x^4 + y^4 - 36 x y$ .

### Solution

$$
\nabla f   = \begin{pmatrix} 4 x^3 - 36 y \\ 4 y^3 - 36 x \end{pmatrix} = 0 \implies 4 x^3 = 30 y, 4 y^3 = 30 x \implies (x,y) = (0,0), (3,3), (-3,-3) \\
\nabla^2 f = \begin{pmatrix} 12 x^2 & -36 \\ -36 & 12 y^2 \end{pmatrix} \\
\nabla^2 f(0,0) = \begin{pmatrix} 0 & -36 \\ -36 & 0 \end{pmatrix} \implies det(\nabla^2 f(0,0)) = -  36^2 < 0 \implies \text{Saddle Point}
\nabla^2 f(\pm 3, \pm 3) = \begin{pmatrix} 108 & -36 \\ -36 & 108 \end{pmatrix} \implies det(\nabla^2 f(\pm 3, \pm 3)) = 108^2 - 36^2 > 0, f_{xx} = 108 > 0 \implies \text{Saddle Point}
$$

So stationary points are (0,0) (saddle point) and (3,3), (-3,-3) (both local minima).

This works because for 2x2 Hessian Matrix:
* determinant $D < 0$ implies eigen values $\lambda_1$, $\lambda_2$ are of opposite signs (as $D = \lambda_1 \lambda_2$), so point is saddle point.
* determinant $D > 0$ and $f_{xx} > 0$ implies positive eigen values, so Hessian is Positive Definite and point is local minima.

## Problem 10

Solve the following optimization problems by hand(s) and also draw the feasible regions:

1. Find the maximum of the following functions:
    * $f(x) = 1 - 8 x + 2 x^2 - \frac{10}{3} x^3 + \frac{1}{4} x^4 + \frac{4}{5} x^5 - \frac{1}{6} x^6$
    * $f(x_1, x_2) = x_1 + x_2 \quad \text{subject to} \quad x_1^2 + x_2^2 - 1 = 0$

2. Verify the KKT conditions and find the Lagrange multipliers for the following function at $x = (1,0)$ :

$$
(x_1 - \frac{3}{2})^2 + (x_2 - \frac{1}{8})^2 \\
\text{subject to} \quad \begin{pmatrix}1 - x_1 - x_2 \\ 1 - x_1 + x_2 \\ 1 + x_1 - x_2 \\ 1 + x_1 + x_2 \end{pmatrix} \ge 0
$$

3. Find the minimum of the function $f(x) = (x_1 - 1)^2 + x_2^2, \quad \text{subject to} \quad x_1 - x_2^2 \le 0$

### Solution

1. 
*
$$
\nabla f = -8 + 4 x - 10 x^2 + x^3 + 4 x^4 - x^5 = 0 \\ 
\nabla^2 f = 4 - 20 x + 16 x^3 - 5 x^4
$$
