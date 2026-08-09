# Revision from Lecture Slides

## Partial Least Squares (PLS) Regression

### 21.07.2026 > PLS Share 1.pdf

Find $w$ so that $Cov(X w, Y)$ is maximum.

PLS uses **projection** to latent structures.

PLS searches for a latent direction $t = X w$ such that:
* $t$ explains a large amount of variance in X, and
* $t$ has maximum covariance with $Y$

PLS rotates X coords system to find axis / direction where changes in X produce largest changes in Y.

Project X, Y into lower-dimensional space:

$$ 
X = T P^T + E \quad (n,p) = (n,a) \times (a,p) \\
Y = U Q^T + F \quad (n,m) = (n,a) \times (a,m)
$$

where $T$, $U$ are **score matrices** / latent variables / common structures, $P$, $Q$ are loadings of original $X$, $Y$, and $E$, $F$ are residuals.

Maximize score variance $Cov(T,U)$ .

TYPES OF PLS:
* PLS 1 : params optimally tuned to predict single response variable at a time
* PLS 2 : multiple response variables at once (useful when responses are conceptually related), more efficient than running PLS 1 many times

Preprocessing before PLS:
* handle missing values, outliers & anamolies
* variables invovled should have somehwat symmetric distributions
* Data is normalized (mean 0, variance 1) ; if very skewed then log-normalized (because PLS weights are sensitive to units, we don't want higher variance variables to influence more)
  * If any variable is indeed more important, then assign it higher scaling weight (in normalize)
  
PLS Algorithms:
* NIPALS (Non Linear Iterative Partial Least Squares) - preferred? 
* SIMPLS (Statistically Inspired Partial Least Squares)

### 28.07.2026 > PLS Share 2.pdf

