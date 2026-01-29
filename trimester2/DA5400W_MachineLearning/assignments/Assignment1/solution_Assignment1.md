--
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

# DA5400W (Foundations of Machine Learning) Assignment 1

Submitted by Sohang Chopra &lt;DA25M622&gt;

-----

## Problem 1

The following probability distribution function can describe the growth rate of finance:

$$f(x) = \frac{1}{\alpha^2} x e^{x / \alpha}$$

with $\alpha \in (0, \infty)$ and $x \in [0, \infty]$. 
Find an estimate of the parameter $\alpha$ using the maximum likelihood
estimators and the method of moments given the datasets $x_1, x_2, \cdots x_n$ .

### Solution

TODO

------

## Problem 2

Consider a process for which a random sample $X_1, X_2, \cdots X_9$ is collected to understand the population properties. 
The population mean and variance are $\mu$ and $\sigma^2$. 
Mr and Mrs. Stat have proposed two estimators as follows:

$$\theta_{Mr} = \frac{X_1 + X_3 + 4 X_5}{6} , \quad \theta_{Mrs} = \frac{X_2  X_6 + 2 X_7 + 3 X_4}{5}$$

### Solution

TODO

------ 

## Problem 3

The probability distribution functions of the Weibull distribution and the Rayleigh distribution are given below:

* Weibull distribution: $f(x; k, \lambda) = \frac{k}{\lambda} (\frac{x}{\lambda})^{k1} e^{(x / \lambda)^k}, \quad x \ge 0$
* Rayleigh distribution: $f(x; ) = \frac{x}{\sigma^2} e^{x^2 / (2 \sigma^2)}, \quad x \ge 0$

Use the dataset [Weibull.csv](https://drive.google.com/file/d/1SNFkOio5wzENCsfCCsamSXxAOSjyaXna/view) provided to estimate the parameter $\lambda$ in Weibull distribution 
using maximum likelihood estimation (MLE) (assume $k = 2$). 
Use the property of invariance of MLE to estimate the parameter  of Rayleigh distribution.

### Solution

TODO

------

## Problem 4

Find the maximum likelihood estimate of the parameter $\theta$ of the following probability distribution function:

$$f(y; \theta) = \frac{3 y^2}{\theta^3}$$

with $\theta \in (0,\infty)$ and $y \in [0,\infty]$ using the data $y_1, y_2, \cdots y_n$ .

### Solution

TODO

--------

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

----------

## Problem 6

Consider a random variable $C$ with mean $\mu$ and standard deviation $\sigma$. 
Two experiments are performed to collect two random samples with $n_1$ and $n_2$ sample sizes. 
The sample means for these experiments are $C_1$ and $C_2$ . 
Then, show that an estimator for the sample mean:

$$\bar{C} = a \bar{C_1} + (1  a) \bar{C_2}$$

is an unbiased estimator for the mean $\mu$.

### Solution 

TODO

---------

## Problem 7

Find the local extrema of the following functions and classify the points as minimum or maximum:

1. $f(x) = 4 x^3  3 x^2 + 2 x  1$
2. $f(x) = sin(x) + cos(x)$
3. $f(x) = \frac{x^2 - 1}{x}$

### Solution

TODO

----------

## Problem 8

Show that the function $f(x_1, x_2) = 8 x_1 + 12 x_2 + x_1^2  2 x_2^2$ has only one stationary point and that it is neither a maximum nor a minimum, but a saddle point. 
Sketch the contour line of $f$.

### Solution

TODO

-----------

## Problem 9

Determine the stationary points and classify their nature for the function $f(x) = x^4 + y^4 - 36 x y$ .

### Solution

TODO

-----------

10. Solve the following optimization problems by hand(s) and also draw the feasible regions:

* Find the maximum of the following function:
$$
f(x) = 1  8 x + 2 x^2 - \frac{10}{3} x^3 + \frac{1}{4} x^4 + \frac{4}{5} x^5 - \frac{1}{6} x^6 \\
f(x_1, x_2) = x_1 + x_2 \quad \text{subject to} \quad x_1^2 + x_2^2 - 1 = 0
$$

* Verify the KKT conditions and find the Lagrange multipliers for the following function at $x = (1,0)$ :

$$(x_1 - \frac{3}{2})^2 + (x_2 - \frac{1}{8})^2$$

subject to

$$\begin{pmatrix}1  x_1  x_2 \\ 1  x_1 + x_2 \\ 1 + x_1 x_2 \\ 1 + x_1 + x_2 \end{pmatrix} \ge 0$$

* Find the minimum of the following function:

$$f(x) = (x_1 - 1)^2 + x_2^2$$

subject to

$$x_1 - x_2^2 \le 0$$

### Solution

TODO
