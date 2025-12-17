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

Sample Variance formula is: $s^2 = frac{sum (x - bar{x})^2}{n-1}$ (denominator is $n-1$ due to **Bessel's Correction** as this is sample variance).

Count, Mean & Variance of Samples A, B (**Bessel's Correction** (divide by $n-1$) is used to make sample variances unbiased estimators of population variances):

$$
n_A = 9, n_B = 11
bar{x_A} = (65 + 66 + 73 + 80 + 82 + 84 + 88 + 90 + 92) / 9 = 80
s_A = (15^2 + 14^2 + 7^2 + 0^2 + 2^2 + 4^2 + 8^2 + 10^2 + 12^2) / (9-1) = 100.25
bar{x_B} = (64 + 66 + 74 + 78 + 82 + 85 + 87 + 92 + 93 + 95 + 97) / 11 = 83
s_B = (19^2 + 17^2 + 9^2 + 5^2 + 1^2 + 2^2 + 4^2 + 9^2 + 10^2 + 14^2) / (11-1) = 115.4
$$

<!-- ANOVA is NOT right test - it compares population means not variances! -->

<!-- https://www.cuemath.com/data/f-test/ -->

Using **F-Test** (as variances are being compared) of type **2-tailed** (as we're checking for equality of variances):

* Null Hypothesis (population variances are equal): $H_0 : sigma_1^2 = sigma_2^2$
* Alternate Hypothesis (population variances are not equal): $H_A : sigma_1^2 ne sigma_2^2$
* Decision Criteria: If the f test statistic > f test critical value then the null hypothesis is rejected.

F Statistic (for small samples) = $s_1^2 / s_2^2 = 1.151$ where $s_1^2$, $s_2^2$ are sample variances ($s_1^2$ is greater variance).

Here B has greater variance, so $F = 115.4 / 99.75 = 1.16$ (approx).

Degrees of Freedom are: $d_B = n_B-1 = 11-1 = 10$, $d_A = n_A-1 = 9-1 = 8$, .

Significance Level $alpha=0.05$ is given, so 2-tailed test significance level = $alpha / 2 = 0.05 / 2 = 0.025$.

In F Table for significance $0.025$, lookup degrees of freedom $10$ in X axis, $8$ in Y axis gives critical value $4.30$.

Here F (1.151) < Critical Value (4.30), so we fail to reject null hypothesis. 
**Therefore the 2 populations have same variance at 5% significance level.**

---------------

## Problem 2

A county environmental agency suspects that the fish in a particular polluted lake have elevated mercury level. To confirm that suspicion, six striped bass in that lake were caught and their tissues were tested for mercury. For the purpose of comparison, five striped bass in an unpolluted lake were also caught and tested. The fish tissue mercury levels in mg/kg are given below.

Sample 1 (from polluted lake)     | Sample 2 (from unpolluted lake)
-----------------------------     | -----------------------
0.610                             | 0.429
0.703                             | 0.391
0.582                             | 0.570
0.591                             | 0.573
0.621                             | 0.497
0.551                             | _

(a) Construct the 95% confidence interval for the difference in the population means based on these data.

(b) Test, at the 5% level of significance, whether the data provide sufficient evidence to conclude that fish in the polluted lake have elevated levels of mercury in their tissue.


### Solution 2

Calculating Mean, Variance of samples (**Bessel's Correction** (divide by $n-1$) is used to make sample variances unbiased estimators of population variances):

$$
n_1 = 6, n_2 = 5
\bar{x_1} = (0.610+0.703+0.582+0.591+0.621+0.551) / 6 = 0.610 (approx) \\
s_1^2 = (0^2 + 0.007^2 + (0.610-0.582)^2 + (0.610-0.591)^2 + 0.011^2 + (0.610-0.551)^2) / (6-1) = 0.0009 (approx) \\
\bar{x_2} = (0.429+0.391+0.570+0.573+0.497)/5 = 0.492 \\
s_2^2 = (0.063^2 + 0.101^2 + 0.078^2 + 0.081^2 + 0.005^2) / (5-1) = 0.0067 (approx) \\
$$

(a) Difference in population means and its Standard Error is:

<!-- 95% confidence interval of difference in population means: https://courses.lumenlearning.com/wm-concepts-statistics/chapter/estimating-the-difference-in-two-population-means/ -->

$$
\bar{x_1} - \bar{x_2} = 0.610 - 0.492 = 0.118
SE[\bar{x_1} - \bar{x_2}] = \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}} = \sqrt{0.0009^2 / 6 + 0.0067^2 / 5} = 0.0386
$$

In normal curve 95% corresponds to 2 standard deviations.
So 95% confidence interval is $(\bar{x_1} - \bar{x_2}) \pm 2 SE[\bar{x_1} - \bar{x_2}] = 0.118 \pm 0.077$.

(b) Here **Welsch T Test (independent, unequal variances)** will be used (as fish in both lakes are unrelated). 

* Null Hypothesis is $H_0 : \bar{x_1} \leq \bar{x_2}$
* Alternate Hypotheis is $H_1 : \bar{x_1} > \bar{x_2}$

Welsch Test T score formula is:

$$t = \frac{(\bar{x_1} - \bar{x_2}) - d_0}{SE[\bar{x_1} - \bar{x_2}]} = 3.057$$

* Assuming difference in population means $d_0 = \mu_1 - \mu_2$ is 0 in above formula t calculation.
* Since sample sizes are similar, degrees of fredom is $n_1 + n_2 - 2 = 6 + 5 - 2 = 9$.
* Looking up $df=9, \alpha=1-0.95=0.05$ in one-tailed T Table, critical p-value is $1.833$ .

Since $t (3.057) > critical (1.833)$, Null Hypothesis is Rejected and so there is sufficient evidence to conclude that fish in the polluted lake have elevated levels of mercury in their tissue.

----------------

## Problem 3

We intend to compare several methods for predicting the shear strength for steel items. 
Data for two of these methods, the M1 and M2, when applied to nine specific items, are shown in Table 1.

Determine if there is a significant difference in shear strength predictions between methods M1 and M2 
at a significance level of $\alpha = 0.05$. 
Address the following while arriving at the conclusion:

(a) Formulate the Null and Alternate Hypothesis
(b) Calculate the test statistic and compare with the critical value
(c) Also compute the p value corresponding to the test statistic

Item  | Method 1  | Method 2
----  | --------  | ---------
1     | 1.186     | 1.061 
2     | 1.151     | 0.992 
3     | 1.322     | 1.063 
4     | 1.339     | 1.062 
5     | 1.200     | 1.065 
6     | 1.402     | 1.178 
7     | 1.365     | 1.037 
8     | 1.537     | 1.086 
9     | 1.559     | 1.052 

*Table 1: Comparison of predictions of Method 1 and Method 2 for 9 items*

### Solution 3

Assuming methods M1 and M2 sheer strength predictions have different means but equal variance.

(a) Null Hypothesis $H_0: \bar{M_1} = \bar{M_2}$, Alternate Hypothesis $H_0: \bar{M_1} \neq \bar{M_2}$
(b) Here we use **Paired T Test** as the 2 sample values are NOT independent (ie values for same 9 items):

Differences $d = x_1 - x_2$ and differences' mean $\bar{d}$, variance $s_d$ are:

Item  | $x_1$     | $x_2$    | $d = x_1 - x_2$
----  | --------  | -------- | ----------------
1     | 1.186     | 1.061    | 0.125
2     | 1.151     | 0.992    | 0.059
3     | 1.322     | 1.063    | 0.259
4     | 1.339     | 1.062    | 0.277
5     | 1.200     | 1.065    | 0.135
6     | 1.402     | 1.178    | 0.222
7     | 1.365     | 1.037    | 0.228
8     | 1.537     | 1.086    | 0.449
9     | 1.559     | 1.052    | 0.507
$\bar{x_1}$ | _   |          | 1.340
$\bar{x_2}$ | _   |          | 1.066
$\bar{d}$ | _     | _        | 0.274
$s_d$   | _     | _          | 0.135

Standard Error of mean difference is $SE = s_d / \sqrt{n} = 0.135 / \sqrt{9} = 0.045$

* Null Hypothesis: $H_0 : \bar{x_1 - x_2} = 0$
* Alternate Hypothesis: $H_1 : \bar{x_1 - x_2} \neq 0$

T Score is:

$$t = \frac{\bar{x_1} - \bar{x_2}}{s_d / \sqrt{n} = (1.340 - 1.066) / (0.421 * 0.045) = 6.08$$

* Degrees of Freedom is $n_1 + n_2 - 2 = 9 + 9 - 2 = 16$ and significance level $\alpha = 0.05$. 
* Looking up in **2-tailed T table** (as we want to know any difference), critical p values is 2.120 .

$t (6.08) > critical (2.120)$, so Null Hypothesis is rejected and there is significant difference in sheer strength predictions using M1 and M2.

-----------------

## Problem 4

A new diagnostic test is designed to detect a rare disease. A test result of positive indicates the presence of the disease, while a negative result suggests its absence. The hypotheses are as follows:

* $H_0$ : The patient does not have the disease.
* $H_1$ : The patient has the disease.

(a) Define Type-I and Type-II errors in this context and explain the potential impacts of each error on the patient.

(b) Given the rarity of the disease, why might the designers of the test prioritize minimizing the Type-I error? What implications does this have for the probability of Type-II error?

(c) Suppose the probability of a Type-I error (false positive) is 0.01. If the probability of a Type-II error (false negative) is 0.2, what is the test’s power?

(d) If the prevalence of the disease is very low (e.g., 0.1%), discuss how Type-I and Type-II errors might impact the test’s overall reliability. How would you interpret a positive result?

### Solution 4

(a)
* *Type-I error* (False Positive) - patient does not have disease, but test falsely diagonises patient as having disease.
    * Impact of Error: These falsely diagonised patients would also be treated, wasting expensive medical treatment and opportunity cost
        of potentially not treating other truly sick patients due to limited hospital resources.
* *Type-II error* (False Negative) - patient has disease but is diagonised as healthy. 
    * Impact of Error: The patient won't be treated and their sickness can get even worse.

(b) As disease is rare so most people will NOT have the disease. 
    Test designers may prioritize minimizing Type-I error to minimize wastage of hospital resources 
    and try to only treat actually sick patients.
    But this will increase probability of Type-II error, as population itself and disease probability has not changed.

(c) $\alpha=0.01, \beta=0.2$, so Power/Sensitivity is: $P(predict_sick | actual_sick) = 1 - \beta = 1-0.2 = 0.8$.

(d) If prevelance of disease is very low (eg. 0.1%), false positives (Type-I error) are likely to be very high, so we should confirm positive cases with a seperate test to confirm disease before starting treatment.
