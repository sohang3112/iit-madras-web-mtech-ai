# Discriminant Analysis — Exam Notes

## 1\. Introduction & Purpose

-   **Discriminant Analysis (DA)**: multivariate technique analyzing the relationship between **one categorical (nominal) dependent variable** and a set of **metric, normally distributed independent variables**.
-   Dependent (grouping) variable: mutually exclusive (ME) categories — each object belongs to exactly one group.
-   **Two-group DA**: 2 categories. **Multi-group DA**: >2 categories.
-   Two tasks DA performs:
    1.  **Discrimination task** — identify which describing variables best distinguish the groups, and assess their discriminatory power.
    2.  **Classification task** — assign new observations to a group based on describing variables.
-   Example: Credit scoring — classify customers as 'good'/'bad' based on age, income, employment duration, etc.

## 2\. Six-Step Procedure

1.  **Define groups** — specify categories of the dependent variable, and specify the discriminant function(s).
    - 2 groups → 1 discriminant function.
    - more than 2 groups → more than one discriminant function.
2.  **Estimate** the discriminant function(s).
3.  **Assess discriminatory power** of the estimated function(s) (overall fit).
4.  **Assess discriminatory power of each independent variable** — which contributes most to group separation.
5.  **Classification rule** — describe how new observations are assigned to groups.
6.  **Test assumptions** of DA.

## 3\. Rules for Defining Groups

-   Grouping variable must be categorical, ME, and collectively exhaustive.
-   A metric variable *can* be converted into categories (e.g., profit → low/high), but this **loses information**.
-   **Number of groups ≤ number of describing variables.**
-   **Minimum sample size guidelines:**
    -   ≥ 5 observations per describing variable (20 recommended).
    -   ≥ 20 observations **per group**.
    -   Relative group sizes should be comparable — large imbalance distorts estimation & classification.
    -   All groups must have data for **all** features (no missing variables across groups); within a group, unequal entry counts across features require deleting or imputing data.

## 4\. The Discriminant Function

$$Y = b_0 + b_1X_1 + b_2X_2 + \cdots + b_JX_J$$

-   Also called the **canonical discriminant function**; Y is the **canonical variable**.
-   **"Linear"** → the function is a weighted sum of the raw variables (first power only); no squares, products (interactions), or other nonlinear transforms. Geometrically defines a straight line/plane/hyperplane separator (not curved).
    -   Note the distinction from linear regression: regression's "linear" refers to linearity **in the coefficients** (predictors themselves can be nonlinear, e.g. X²); in **LDA**, "linear" refers to the **linear combination of the predictors**.
-   **"Canonical"** → the coefficients are chosen to be the *statistically optimal* combination — i.e., the one that **maximizes separation between groups**. If multiple functions exist (multi-group case), they are mutually **uncorrelated (orthogonal)**, each capturing successively less remaining separation (like PCA/canonical correlation).
-   Coefficients $b_0, b_j$ are estimated so that the groups differ **as much as possible** with respect to Y (this requires an objective/discriminant criterion to maximize).
-   Y is metric but does **not** directly reveal group membership — that requires a classification rule (see below).

## 5\. Discriminant Criterion (Conceptual, via worked example)

-   Example: chocolate buyers — focal brand vs. competitor, rated on **Price** and **Delicious** (1–7 scale), n = 12 per group.
-   Group means: Price — 3.5 (focal) vs 5.0 (competitor); Delicious — 4.5 (focal) vs 4.0 (competitor).
-   Since distributions overlap significantly, **neither single variable separates groups perfectly**; visual/mean comparison suggests Price discriminates better than Delicious.
-   This motivates finding an optimal **linear combination** of both variables that separates groups better than either alone — that's the discriminant function.

## 6\. Mathematical Theory of Classification

### 6.1 Basic Setup

-   Two populations π₁, π₂, described by p random variables **X**.
-   Ω = sample space of all possible x. Partition Ω into **R₁** (classify as π₁) and **R₂ = Ω − R₁** (classify as π₂) — mutually exclusive & exhaustive.
-   Populations described by density functions f₁(x), f₂(x).

### 6.2 Misclassification Probabilities

$$P(2|1) = P(X \in R_2 \mid \pi_1) = \int_{R_2} f_1(x)\, dx$$ $$P(1|2) = P(X \in R_1 \mid \pi_2) = \int_{R_1} f_2(x)\, dx$$ (Volume under density over the "wrong" region.)

### 6.3 Cost of Misclassification

-   Misclassification isn't just about probability — **cost matters**. E.g., missing a fatal disease diagnosis is far costlier than a false positive.
-   **Cost matrix**:

| True \ Classify as | π₁  | π₂  |
| ------------------ | --- | --- |
| π₁                 | 0   | c(2 | 1) |
| π₂                 | c(1 | 2)  | 0  |

-   Let p₁, p₂ = prior probabilities (p₁ + p₂ = 1).
-   **Expected Cost of Misclassification (ECM):** $$ECM = c(2|1),P(2|1),p_1 + c(1|2),P(1|2),p_2$$
-   A good rule **minimizes ECM**.
-   Minimizing ECM leads to the rule: assign **x** to π₁ if $$\frac{f_1(x)}{f_2(x)} \ge \frac{c(1|2)}{c(2|1)}\cdot\frac{p_2}{p_1}$$ (i.e., **density ratio ≥ cost ratio × prior-probability ratio**), else assign to π₂.
    -   Intuition: the equation to minimize is $T(R,f) = c(2|1)p_1 + \int_{R_1}[c(1|2)p_2f_2(x) - c(2|1)p_1f_1(x)]\, dx$; this is minimized by including in R₁ exactly those x where the bracketed integrand is negative — which rearranges into the ratio rule above.

### 6.4 Special Cases (common in practice)

(a) Equal priors (p₂/p₁ = 1): compare $\frac{f_1(x)}{f_2(x)}$ to $\frac{c(1|2)}{c(2|1)}$ (b) Equal misclassification costs: compare $\frac{f_1(x)}{f_2(x)}$ to $\frac{p_2}{p_1}$ (c) **Equal priors AND equal costs** (most common default assumption): $$R_1: \frac{f_1(x)}{f_2(x)} \ge 1 \qquad R_2: \frac{f_1(x)}{f_2(x)} < 1$$ → simply compare density values; assign to whichever population has higher density at x.

## 7\. Classification with Two Multivariate Normal Populations

### 7.1 Equal Covariance Case (Σ₁ = Σ₂ = Σ)

-   Densities: $f_i(x) = \frac{1}{(2\pi)^{p/2}|\Sigma|^{1/2}}\exp\left[-\tfrac12(x-\mu_i)'\Sigma^{-1}(x-\mu_i)\right]$, i = 1,2
-   Substituting into the ECM minimum rule and simplifying (population parameters µ₁, µ₂, Σ assumed **known**) gives:

**Allocate x to π₁ if:** $$(\mu_1-\mu_2)'\Sigma^{-1}x - \tfrac12(\mu_1-\mu_2)'\Sigma^{-1}(\mu_1+\mu_2) \ge \ln\left[\frac{c(1|2)}{c(2|1)}\cdot\frac{p_2}{p_1}\right]$$ Otherwise allocate to π₂.

### 7.2 Sample (Estimated) Version — Practical Case

-   In practice µ₁, µ₂, Σ are **unknown** → replace with sample estimates:
    -   $\bar{x}_1, \bar{x}_2$ = sample mean vectors of group 1, group 2
    -   $S_1, S_2$ = sample covariance matrices
    -   **Pooled covariance estimate** (unbiased, since Σ assumed equal across groups): $$S_{pooled} = \left[\frac{n_1-1}{(n_1-1)+(n_2-1)}\right]S_1 + \left[\frac{n_2-1}{(n_1-1)+(n_2-1)}\right]S_2$$

**Estimated Minimum ECM Rule (Fisher's Linear Discriminant Rule):**

Allocate $x_0$ to π₁ if: $$(\bar{x}_1-\bar{x}*2)'S*{pooled}^{-1}x_0 - \tfrac12(\bar{x}_1-\bar{x}*2)'S*{pooled}^{-1}(\bar{x}_1+\bar{x}_2) \ge \ln\left[\frac{c(1|2)}{c(2|1)}\cdot\frac{p_2}{p_1}\right]$$ Otherwise allocate to π₂.

### 7.3 Reduction to Scalar Comparison

Define: $$\hat{y} = (\bar{x}_1-\bar{x}*2)'S*{pooled}^{-1}x = \hat{a}'x \qquad \text{where } \hat{a}' = (\bar{x}_1-\bar{x}*2)'S*{pooled}^{-1}$$

Midpoint: $$\hat{m} = \tfrac12(\bar{x}_1-\bar{x}*2)'S*{pooled}^{-1}(\bar{x}_1+\bar{x}_2) = \tfrac12(\bar{y}_1+\bar{y}_2)$$ where $\bar{y}_1 = \hat{a}'\bar{x}_1$, $\bar{y}_2 = \hat{a}'\bar{x}_2$.

-   The full rule reduces to comparing $\hat{y}_0 = \hat{a}'x_0$ (score for a new observation) against midpoint $\hat{m}$.
-   **Equal priors & equal costs case** (ln(1) = 0, most commonly assumed):

$$\boxed{\text{Allocate } x_0 \text{ to } \pi_1 \text{ if } \hat{a}'x_0 \ge \hat{m}; \text{ otherwise allocate to } \pi_2}$$

-   **Interpretation**: DA collapses a multivariate problem into a **univariate comparison** — project x onto direction $\hat{a}$ to get scalar score $\hat{y}$; classify by whether it falls to the right or left of the midpoint $\hat{m}$ between the two group means $\bar{y}_1, \bar{y}_2$.

### 7.4 Caveat

-   Once population parameters are replaced by sample estimates, there's **no guarantee** the resulting rule truly minimizes ECM in a given application (it's only an *estimate* of the optimal rule).
-   Performance improves with **larger sample sizes**.

## 8. Summary — Key Formula for the Exam

Given equal priors & equal misclassification costs (default assumption):

1.  Compute $\bar{x}_1, \bar{x}*2, S_1, S_2 \Rightarrow S*{pooled}$
2.  Compute $\hat{a}' = (\bar{x}_1-\bar{x}*2)'S*{pooled}^{-1}$
3.  Compute $\hat{m} = \tfrac12\hat{a}'(\bar{x}_1+\bar{x}_2)$
4.  For new observation $x_0$: compute score $\hat{y}_0 = \hat{a}'x_0$
5.  If $\hat{y}_0 \ge \hat{m}$ → classify as π₁; else → π₂.

(General case: replace 0 threshold with $\ln\left[\frac{c(1|2)}{c(2|1)}\cdot\frac{p_2}{p_1}\right]$ when priors/costs are unequal.)

## 9. Conceptual Clarifications (Common Doubts)

**Ordinal → Metric scales (e.g., 1–7 ratings) used in LDA:** Justified as an approximation when: (a) there are several ordered categories (≥5); (b) categories are reasonably evenly spaced; (c) the distribution isn't extremely skewed (unimodal, symmetric); (d) sample size is reasonably large; (e) the analysis targets an approximately linear relationship. It's an accepted approximation, not mathematically exact.

**Clustering vs. Discriminant Analysis:**

|               | Clustering                         | Discriminant Analysis                                     |
| ------------- | ---------------------------------- | --------------------------------------------------------- |
| Learning type | Unsupervised                       | Supervised                                                |
| Groups        | Unknown in advance                 | Known/defined in advance                                  |
| Goal          | Discover natural/hidden structure  | Find rule to separate known groups & classify new cases   |
| Mechanism     | Distance/similarity between points | Known dependent grouping variable + independent variables |
| Example use   | Customer segmentation              | Predicting student success / medical diagnosis            |

**Why "canonical":** the discriminant function isn't an arbitrary linear combination — it is the one mathematically optimal for separating groups, derived in a standardized form.

## 10. Solved Problem: Two-Group Linear Discriminant Analysis

### Problem Statement

A chocolate manufacturer wants to know whether buyers of its **focal brand** perceive the chocolate differently from buyers of the **main competitor brand**, based on two describing variables (rated on a 1–7 scale): **Price** and **Delicious**.

**Data** (12 buyers per group):

| Group 1: Focal brand (π₁) |           | Group 2: Competitor (π₂) |           |
| ------------------------- | --------- | ------------------------ | --------- |
| Price                     | Delicious | Price                    | Delicious |
| 2                         | 3         | 5                        | 4         |
| 3                         | 4         | 4                        | 3         |
| 6                         | 5         | 7                        | 5         |
| 4                         | 4         | 3                        | 3         |
| 3                         | 2         | 4                        | 4         |
| 4                         | 7         | 5                        | 2         |
| 3                         | 5         | 4                        | 2         |
| 2                         | 4         | 5                        | 5         |
| 5                         | 6         | 6                        | 7         |
| 3                         | 6         | 5                        | 3         |
| 3                         | 3         | 6                        | 4         |
| 4                         | 5         | 6                        | 6         |

**Tasks:**
(a) Obtain the sample linear discriminant function, assuming **equal prior probabilities** and **equal misclassification costs**.
(b) Classify a **new buyer** with Price = 4, Delicious = 6.

---

### Solution

#### Step 1: Compute Group Mean Vectors

$$\bar{x}_1 = \begin{bmatrix}\bar{x}_{1,\text{Price}}\\ \bar{x}_{1,\text{Delicious}}\end{bmatrix} = \begin{bmatrix}3.5\\4.5\end{bmatrix}, \qquad \bar{x}_2 = \begin{bmatrix}5.0\\4.0\end{bmatrix}$$

*(Sum each column and divide by n₁ = n₂ = 12; e.g. Group 1 Price: (2+3+6+4+3+4+3+2+5+3+3+4)/12 = 42/12 = 3.5)*

#### Step 2: Compute Group Covariance Matrices

Using $S = \dfrac{1}{n-1}\sum (x_j - \bar{x})(x_j-\bar{x})'$ for each group:

$$S_1 = \begin{bmatrix}1.3636 & 0.8182\\0.8182 & 2.0909\end{bmatrix}, \qquad S_2 = \begin{bmatrix}1.2727 & 1.0909\\1.0909 & 2.3636\end{bmatrix}$$

**Worked example for S₁ (Price variance):**


* Deviations from mean (3.5) for Group 1 Price: −1.5, −0.5, 2.5, 0.5, −0.5, 0.5, −0.5, −1.5, 1.5, −0.5, −0.5, 0.5
* Sum of squares = 15.0 
*  variance = 15.0 / (12−1) = 15.0/11 = 1.3636 ✓
* (Covariance and Delicious-variance terms follow the same pattern using cross-products and squared deviations.)

#### Step 3: Pool the Covariance Matrices

Since DA assumes **Σ₁ = Σ₂ = Σ**, pool S₁ and S₂ (weighted by degrees of freedom):

$$S_{pooled} = \left[\frac{n_1-1}{(n_1-1)+(n_2-1)}\right]S_1 + \left[\frac{n_2-1}{(n_1-1)+(n_2-1)}\right]S_2$$

Since n₁ = n₂ = 12, weights are equal (11/22 = 0.5 each):

$$S_{pooled} = 0.5\begin{bmatrix}1.3636 & 0.8182\\0.8182 & 2.0909\end{bmatrix} + 0.5\begin{bmatrix}1.2727 & 1.0909\\1.0909 & 2.3636\end{bmatrix} = \begin{bmatrix}1.3182 & 0.9545\\0.9545 & 2.2273\end{bmatrix}$$

#### Step 4: Invert the Pooled Covariance Matrix

For a 2×2 matrix $\begin{bmatrix}a&b\\b&d\end{bmatrix}$, inverse $= \dfrac{1}{ad-b^2}\begin{bmatrix}d&-b\\-b&a\end{bmatrix}$

$$\det(S_{pooled}) = (1.3182)(2.2273) - (0.9545)^2 = 2.9360 - 0.9111 = 2.0249$$

$$S_{pooled}^{-1} = \frac{1}{2.0249}\begin{bmatrix}2.2273 & -0.9545\\-0.9545 & 1.3182\end{bmatrix} = \begin{bmatrix}1.1000 & -0.4714\\-0.4714 & 0.6510\end{bmatrix}$$

#### Step 5: Compute the Discriminant Coefficient Vector

$$\hat{a}' = (\bar{x}_1-\bar{x}_2)'S_{pooled}^{-1}$$

$$\bar{x}_1 - \bar{x}_2 = \begin{bmatrix}3.5-5.0\\4.5-4.0\end{bmatrix} = \begin{bmatrix}-1.5\\0.5\end{bmatrix}$$

$$\hat{a}_1 = (-1.5)(1.1000) + (0.5)(-0.4714) = -1.6500 - 0.2357 = -1.8857$$
$$\hat{a}_2 = (-1.5)(-0.4714) + (0.5)(0.6510) = 0.7071 + 0.3255 = 1.0326$$

$$\boxed{\hat{a}' = (-1.8857,\\ \\ 1.0326)}$$

**Sample Linear Discriminant Function:**

$$\hat{y} = -1.8857\,(\text{Price}) + 1.0326\,(\text{Delicious})$$

#### Step 6: Compute the Midpoint (Cutoff)

$$\bar{y}_1 = \hat{a}'\bar{x}_1 = (-1.8857)(3.5) + (1.0326)(4.5) = -6.6000 + 4.6467 = -1.9533$$
$$\bar{y}_2 = \hat{a}'\bar{x}_2 = (-1.8857)(5.0) + (1.0326)(4.0) = -9.4285 + 4.1304 = -5.2981$$

$$\hat{m} = \tfrac12(\bar{y}_1 + \bar{y}_2) = \tfrac12(-1.9533 - 5.2981) = -3.6257$$

#### Step 7: Classification Rule

Since priors and costs are assumed equal:

$$\text{Allocate } x_0 \text{ to } \pi_1 \text{ if } \hat{a}'x_0 \ge \hat{m}\\ (=-3.6257); \text{ otherwise allocate to } \pi_2$$

#### Step 8 (Part b): Classify New Case — Price = 4, Delicious = 6

$$\hat{y}_0 = \hat{a}'x_0 = (-1.8857)(4) + (1.0326)(6) = -7.5428 + 6.1956 = -1.3472$$

Compare to cutoff:
$$-1.3472 \\ \ge \\ -3.6257 \quad \Rightarrow \quad \text{Classify as } \boxed{\pi_1 \text{ (Focal brand buyer)}}$$

---

### Quick Sanity Check (optional, good exam habit)

Verify the rule correctly classifies a known training point from each group:

- Group 1 point (2, 3): $\hat{y} = -1.8857(2) + 1.0326(3) = -0.674$. Since $-0.674 \ge -3.6257$ → π₁ ✓ (correctly recovers its own group)
- Group 2 point (5, 4): $\hat{y} = -1.8857(5) + 1.0326(4) = -5.298$. Since $-5.298 < -3.6257$ → π₂ ✓

This confirms the discriminant function is internally consistent with the training data.

---

### Key Takeaway for Exam

The whole multivariate classification problem collapses into **one scalar comparison**:
1. Compute $\hat{a}' = (\bar{x}_1-\bar{x}_2)'S_{pooled}^{-1}$
2. Compute cutoff $\hat{m} = \tfrac12\hat{a}'(\bar{x}_1+\bar{x}_2)$
3. For any new $x_0$: compute $\hat{y}_0 = \hat{a}'x_0$, compare to $\hat{m}$.
4. $\hat{y}_0 \ge \hat{m} \Rightarrow \pi_1$; else $\Rightarrow \pi_2$.

(If priors/costs are **unequal**, replace $\hat m$ on the right-hand side with $\hat{m} + \ln\left[\frac{c(1|2)}{c(2|1)}\cdot\frac{p_2}{p_1}\right]$.)