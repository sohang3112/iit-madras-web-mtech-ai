---
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

# CH5440W Multi-Variate Analysis - Assignment 1 Part 1

## Question 1

A new washing machine prototype is developed by a Company. It’s unique design enables efficient removal of dirt but at the same time it is felt that the color of the cloth also gets removed during the washing. Hence the washing machine is subject to some trials wherein the color in the wash liquid (C) is analyzed using a photometer. The variables considered while washing with good quality water are listed as follows. 

1. Temperature of the water $X_1$
2. Amount of detergent powder $X_2$

The washing time is set for a standard 10-minute cycle. 

It is assumed that the addition of powder does not induce additional heating or cooling of the water.  The data collected are given below.  The model to be considered is NOT known.  Since the two variables are of different magnitudes it is better to code the variables as shown in Table 1. Consider a linear regression model involving the main effects X1 and X2 only. 

| S. No. | $T_c$ | $P_c$ | $C$ (ppm) |
| ------ | ----- | ----- | --------- |
| 1      | -1    | -1    | 234       |
| 2      | 0     | -1    | 257.5     |
| 3      | 1     | -1    | 282       |
| 4      | -1    | 0     | 193.5     |
| 5      | 0     | 0     | 187       |
| 6      | 1     | 0     | 181.5     |
| 7      | -1    | 1     | 153       |
| 8      | 0     | 1     | 116.5     |
| 9      | 1     | 1     | 81        |
| 10     | 0.5   | -0.5  | 226.9     |
| 11     | -0.5  | -0.5  | 217.9     |
| 12     | 0.5   | 0.5   | 141.4     |
| 13     | -0.5  | 0.5   | 162.4     |

$$T_c = \frac{T - 40}{50 - 40}, \quad P_c = \frac{P - 6}{9 - 6}$$

Find:

1. The $(X^T X)^{-1}$ matrix
2. The least squares estimates of the parameters including intercept 
3. Compare actual values with model predicted values 
4. the degrees of freedom for residual sum of squares 
5. the estimated standard error of the least square estimators 
6. the SSTotal, SSResidual, and SSRegression all corrected for the intercept 
7. $R^2$
8. adjusted $R^2$
9. PRESS 
10. $R^2_{PRESS}$

### Solution 1

TODO


## Question 2

In a regression analysis, data was fitted in different ways to give different regression equations (Table 2). Find:
1. $R^2$ 
2. adjusted $R^2$ 
3. PRESS 
4. R[2] based on PRESS. 

**Table 2.** Regression Fits for a single independent variable x 

| Runs | x   | y    | Runs included to find regression fit | Regression Equation           |
| ---- | --- | ---- | ------------------------------------ | ----------------------------- |
| A    | -1  | -5.1 | Only B & C                           | $\hat{y} = -3.10 + 3.5 x$     |
| B    | 2   | 3.9  | Only A & C                           | $\hat{y} = -1.975 + 3.125 x$  |
| C    | 3   | 7.4  | Only A & B                           | $\hat{y} = -2.1 + 3 x$        |
| _    | _   | _    | All (1, 2 and 3)                     | $\hat{y} = -2.062 + 3.0962 x$ |

Do you find $R^2$ and adjusted $R^2$ only for the full model including points A, B, and C or find them for models based on B&C only, A&C only and A&B only as well? 

### Solution 2

TODO


## Question 3

1. Find the inverse of the following matrix $A$ (use Python / Matlab):

$$A = \begin{pmatrix} 1 & -1 & 2 \\ 2 & 2 & 4 \\ 3 & 4 & 6 \end{pmatrix}$$

If you had difficulties in inverting this matrix, what is the reason? 

2. Is the following matrix $B$ positive definite? If yes, show that it satisfies all the required properties including sign of eigenvalues. 

$$B = \begin{pmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{pmatrix}$$

3. What are idempotent matrices? Is the following matrix idempotent? 

$$C = \begin{pmatrix} 2 & -2 & -4 \\ -1 & 3 & 4 \\ 1 & -2 & -3 \end{pmatrix}$$

4. Show that the matrix $x$ obtained as follows is both orthogonal and orthonormal. Also show that $x x^T = I$.

$$x = \begin{pmatrix} 0.2534 & -0.9674 \\ 0.9674 & 0.2534 \end{pmatrix}$$

### Solution 2

TODO


## Question 4

The Cholesky decomposition factorizes a Hermitian, positive-definite matrix $A$ into the product of a lower triangular matrix $L$ and its conjugate transpose $L^*$ (or $L^T$ for real matrices), such that $A = L L^*$ or $L L^T$ . It is roughly twice as fast as LU decomposition and requires half the storage.

1. For the matrix given below can you do Cholesky Decomposition? If yes, what are the required criteria and the outcomes of the decomposition? 

$$A = \begin{pmatrix} 4 & 12 & -16 \\ 12 & 37 & -43 \\ -16 & -43 & 98 \end{pmatrix}$$

Please do the calculations by hand and confirm with Python/Matlab  .

2. For the matrix (same as in previous part) do the LU Decomposition. Is the result same as that of the Cholesky Decomposition? 

Please do the calculations by hand and confirm with Python/Matlab.

### Solution 4

TODO


## Question 5

*Reference: Kutner, M. H., C. J. Nachtschiem, J. Netner, Applied Linear Regression Models. 4th ed. New Delhi: McGraw Hill, 2004.*

A researcher studied the effects of the charge rate and temperature on the life of a new type of power cell in a preliminary small-scale experiment. The charge rate $X_1$ was controlled at three levels (0.6, 1.0, and 1.4 amperes) and the ambient temperature $X_2$ was controlled at three levels (10, 20, 30°C). Factors pertaining to the discharge of the power cell were held at fixed levels. The life of the power cell $Y$ was measured in terms of the number of discharge-charge cycles that a power cell underwent before it failed. The data obtained in the study are given below: 

| Lifecycle $Y$ | Charge Rate $X_1$ | Temperature $X_2$ |
| ------------- | ----------------- | ----------------- |
| 144           | 0.6               | 10                |
| 89            | 1.0               | 10                |
| 59            | 1.4               | 10                |
| 278           | 0.6               | 20                |
| 167           | 1.0               | 20                |
| 141           | 1.0               | 20                |
| 164           | 1.0               | 20                |
| 129           | 1.4               | 20                |
| 259           | 0.6               | 30                |
| 245           | 1.0               | 30                |
| 214           | 1.4               | 30                |

The researcher was not sure about the nature of the response function in the range of the factors studied. Hence, the researcher decided to fit the second-order polynomial regression model as follows: 

$$Y_i = \beta_0 + \beta_1 x_{i,1} + \beta_2 x_{i,2} + \beta_{1,1} x_{i,1}^2 + \beta_{2,2} x_{i,2}^2 + \beta_{1,2} x_{i,1} x_{i,2} + \epsilon_i$$ 

So we have to find the six estimated parameters of the above model. 

**Write a code (using R/Python/MATLAB) to find the following:** 

1. Create a matrix $X$ for raw data.
2. Create a matric $z$ such that $z = \frac{X - \mu}{max(X) - min(X)}$ .
3. Find regression coefficients for the two different cases ($X$ and $z$). 
4. Find residual sum of squares, regression sum of squares, total sum of squares. Use both Matrix and summation approaches and compare them. Do the values change depending upon the transformation? 
5. Find the variance-covariance matrix in both cases and compare the matrices for the transformed $z$ and non-transformed $X$ cases. Which is better in terms of precision of the regression coefficient estimates? 
6. Find $R^2$ , adj. $R^2$ , PRESS, $R^2_{PRESS}$ for both the cases. 

