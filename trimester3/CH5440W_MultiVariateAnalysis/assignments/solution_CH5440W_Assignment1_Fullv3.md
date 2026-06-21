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

It is assumed that the addition of powder does not induce additional heating or cooling of the water. The data collected are given below. The model to be considered is NOT known. Since the two variables are of different magnitudes it is better to code the variables as shown in Table 1. Consider a linear regression model involving the main effects X1 and X2 only. 

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

$X$ matrix is (first 2 columns for $X_1$, $X_2$ and an extra column of 1s to handle intercept), and $y$ vector is::

$$
X = \begin{pmatrix}
-1 & -1 & 1 \\
 0 & -1 & 1 \\
 1 & -1 & 1 \\
-1 &  0 & 1 \\
 0 &  0 & 1 \\
 1 &  0 & 1 \\
-1 &  1 & 1 \\
 0 &  1 & 1 \\
 1 &  1 & 1 \\
0.5 & -0.5 & 1 \\
-0.5 & -0.5 & 1 \\
0.5 & 0.5 & 1 \\
-0.5 & 0.5 & 1
\end{pmatrix},
\quad y = \begin{pmatrix} 234 \\ 257.5 \\ 282 \\ 193.5 \\ 187 \\ 181.5 \\ 153 \\ 116.5 \\ 81 \\ 226.9 \\ 217.9 \\ 141.4 \\ 162.4 \end{pmatrix}
$$

1. $(X^T X)^{-1}$ is actually a scalar (aka 1x1 matrix) whose value is $1 / ((-1)(-1) + 0(-1) + 1(-1) + (-1)(0) + 0(0) + 1(0) + (-1)(1) + 0(1) + 1(1) + 0.5 (-0.5) - 0.5(-0.5) + 0.5(0.5) + (-0.5)(0.5)) = 1 / 0.5 = 2$
   
2. Least square parameter estimates are $w = (X^T X)^{-1} X^T y = 2 (-234 + 282 - 193.5 + 181.5 - 153 + 81 + 0.5 * 226.9 - 0.5 * 217.9 + 0.5 * 141.4 - 0.5 * 162.4, -234 - 257.5 - 282 + 153 + 116.5 + 81 - 0.5 * 226.9 - 0.5 * 217.9 + 0.5 * 141.4 + 0.5 * 162.4, 234 + 257.5 + 282 + 193.5 + 187 + 181.5 + 153 + 116.5 + 81 + 226.9 + 217.9 + 141.4 + 162.4) = (-84, -987, 4869.2)$. So fitted model is:

$$y = - 84 x_1 - 987 x_2 + 4869.2$$

3. Actual $y$ vs Predicted values $\hat{y}$:

| S. No. | $x_1$ | $x_2$ | $y$       | $\hat{y}$
| ------ | ----- | ----- | --------- | ----------
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

## **Question 6** 

## **[2+3+2+5+2]** 

Take any dataset pertaining to your discipline that involves numerical and categorical predictors (at least one each) and one numerical response variable.  If you are unable to find an example/exercise, invent one on your own. 

Do a linear regression problem involving both numerical and categorical predictors using two methods 

- a) Using one hot encoding (OHE) with intercept removed and present the X matrix 

- b) Run the regression based on OHE and present the results (estimated parameters, comparison with predicted values) 

- c) Show the dummy variable trap if you had retained the intercept 

- d) Using dummy variables where intercept is allowed carry out the regression and present the results 

e) Show how you created dummy variables from OHE variables 

**NOTE:** Give all formulae and matrices.  Also provide code 

## **Question 7** 

![](trimester3/CH5440W_MultiVariateAnalysis/assignments/CH5440W_Assignment1_Fullv3_images/CH5440W_Assignment1_Fullv3.pdf-0007-03.png)

The following sample (n= 12) is collected from a population. Obtain its first quartile, second quartile (median) and the third quartile values.  Also obtain the mean, standard deviation and variance. 

10, 12, 11, 9, 9, 10, 11, 12, 11, 10, 11, 12 

## **Question 8** 

**[5]** 

Experiments  labelled  E1  to  E6  were  performed  on  plant  species  A  and  B.   The experiments comprised of adding saltwater (0-250 mg/L).  The initial plant heights were noted and their growth in terms of increase in height was monitored.  The wilting of the plant was monitored using a scale between 0 and 10.  The plants that survived was denoted 1 and those which died was denoted 0. 

Make a schematic table based on the above information including Experiment ID, plant species, concentration of salt, initial height, growth, wilting and survival. 

Identify the types of variables in this table. 

## **Question 9** 

**[8]** 

Let us say that you come across the following data set.  You want to identify the outliers in this data set. 

Identify the outlier(s) using the following means 

- a) Visual inspection 

- b) Drawing figures – for e.g. box plot 

- c) Using interquartile range 

- d) Assume a normal distribution and find z-scores. An z score >3 or <-3 indicates the presence of an outlier 

## **Question 10** 

## **[9]** 

For the data presented in Table below, find the missing values and provide justification for the methods you used to estimate them.  Compare your method(s) with moving mean technique (5 point window about each of the missing values) 

## **Table Q10.** Handling Missing Data 

|**Sl. No.**|**X**|**Y**|**Z**|
|---|---|---|---|
|1|0|3|0|
|2|1|5|1|
|3|3|**?**|9|
|4|6|15|**?**|
|5|8|19|64|
|6|9|**?**|81|
|7|10|23|100|
|8|12|27|144|

**Question 11** 

**[10]** 

Match the following in the table given below (more than one pair up is possible) 

|**Variable type**|**Examples**|
|---|---|
|(A) Nominal|(I)<br><50,000; 50000-100000; >100000 (in<br>Rs.)|
|(B) Ordinal|(II)<br>pH|
|(C)Interval|(III)<br>Reaction rate|
|(D)Ratio|(IV)<br>PIN code|
||(V)<br>Genotype|
||(VI)<br>Temperature scale in Rankine (oR)|
||(VII)<br>scale of years AD (Anno Domini)|
||(VIII)<br>Calendar dates|
||(IX)<br>Shoe size|
||(X)<br>Pulse rate|
||(XI)<br>F1 race car speed|
||(XII)<br>Education : BSc, MSc, MPhil|

---+---
