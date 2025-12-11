---
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

# DA5000 Probability Assignment 2

*Roll No. DA5000, Name: Sohang Chopra*

## Problem 1

Two random samples are drawn from two normal populations.
Their values are:

- A: 65,66,73,80,82,84,88,90,92
- B: 64,66,74,78,82,85,87,92,93,95,97

Test whether the two populations have the same variance at the 5% level of significance.

### Solution 1

Sample Variance formula is: $s^2 = \frac{\sum (x - \bar{x})^2}{n-1}$ (denominator is $n-1$ due to **Bessel's Correction** as this is sample variance).

Count, Mean & Variance of Samples A, B:

$$
n_A = 9, n_B = 11
\bar{x_A} = (65 + 66 + 73 + 80 + 82 + 84 + 88 + 90 + 92) / 9 = 80
s_A = (15^2 + 14^2 + 7^2 + 0^2 + 2^2 + 4^2 + 8^2 + 10^2 + 12^2) / (9-1) = 99.75
\bar{x_B} = (64 + 66 + 74 + 78 + 82 + 85 + 87 + 92 + 93 + 95 + 97) / 11 = 83
s_B = (19^2 + 17^2 + 9^2 + 5^2 + 1^2 + 2^2 + 4^2 + 9^2 + 10^2 + 14^2) / (11-1) = 115.4
$$

<!-- ANOVA is NOT right test - it compares population means not variances! -->

<!-- https://www.cuemath.com/data/f-test/ -->

Using **F-Test** (as variances are being compared) of type **2-tailed** (as we're checking for equality of variances):

* Null Hypothesis (population variances are equal): $H_0 : \sigma_1^2 = \sigma_2^2$
* Alternate Hypothesis (population variances are not equal): $H_A : \sigma_1^2 \ne \sigma_2^2$
* Decision Criteria: If the f test statistic > f test critical value then the null hypothesis is rejected.

F Statistic (for small samples) = $s_1^2 / s_2^2$ where $s_1^2$, $s_2^2$ are sample variances ($s_1^2$ is greater variance).

Here B has greater variance, so $F = 115.4 / 99.75 = 1.16$ (approx).

Degrees of Freedom are: $d_B = n_B-1 = 11-1 = 10$, $d_A = n_A-1 = 9-1 = 8$, .

Significance Level $\alpha=0.05$ is given, so 2-tailed test significance level = $\alpha / 2 = 0.05 / 2 = 0.025$.

In F Table for significance $0.025$, lookup degrees of freedom $10$ in X axis, $8$ in Y axis gives critical value $4.30$.

Here F (1.6) < Critical Value (4.30), so we fail to reject null hypothesis. 
**Therefore the 2 populations have same variance at 5% significance level.**

---------------

## Solution 2

TODO 

----------------

## Solution 3

TODO

-----------------

## Solution 4

TODO
