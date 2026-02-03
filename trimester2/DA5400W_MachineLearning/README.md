# DA45400W : Foundations of Machine Learning

Faculty:
* Prof Nirav Pravinbhai Bhatt &lt;niravbhatt@smail.iitm.ac.in&gt;
* Prof Tirthankar Sengupta &lt;tirtha.s@gmail.com&gt;

Course group email &lt;da5400w@code.iitm.ac.in&gt;

Machine Learning usually requires significant feature engineering, but Deep Learning often automatically transforms features.

## Lecture 1 (Optimization) & Lecture 2 (Probability) revision (common lecture slides)

### Optimization Revision

* Constrained vs Unconstrained (aka **Static**) optimization
* Linear, Quadratic, Non linear programming
* Integer optimization
* Direct vs Iterative solution
* **Arthur Samuel's pardigm/mechanism** to improve performance by tweaking weights/parameters.
* Gradient Descent

#### Mathematical Optimization

* Linear function: $a f(x) + b f(y) = f(ax + by)$
    * **Linear vs Affine linear**: linear has only scaling $A x$, with transform it becomes Affine linear $A x + b$
* Convex function ($\lambda \in [0,1]$): $\lambda f(x_1) + (1 - \lambda) f(x_2) \le f(\lambda f(x_1) + (1 - \lambda) f(x_2))$

Optimize: select best elem (or multiple best elems) from available set of options.

Optimization problem with decision variables: maximize **cost/objective/loss function** $f(\mathbf{x})$ subject to constraints $g_i(\mathbf{x}) \le 0$ .

NOTE: constraints can be both linear and non-linear, sometimes linear are written seperately $A_i x \le b_i$.

#### Optimization Types

* Linear programming: maximize $c^T x$ subject to $A_i x \le b_i$
* Quadratic
* Non-linear

#### Constrained Optimization

##### KKT 

Has to be used for non-linear optimization.

Lagrangian $L(\mathbf{x}, \mathbf{\lambda}, \mathbf{\mu}) = f(\mathbf{x}) + \mathbf{\lambda}^T h(\mathbf{x}) + \mathbf{\mu}^T g(\mathbf{x})$

* First-order necessary condition: 
$$
\nabla L(\mathbf{x^*}, \mathbf{\lambda}) = 0 \
h_i(\mathbf{x^*}) = 0 \\
g_j(\mathbf{x^*}) = 0 \\
\lambda_i \ge 0, \mu_j \ge 0 \\
$$

Complementary condition $\mu_j g_j(\mathbf{x^*}) = 0$ (NOTE: $\mu_j$ is dependent on $x$, here we're talking only about values of $\mu_j$ at $x^*$)

* Second-order necessary condition: TODO

**LICQ**: Linearly Independent (TODO: rem full form)

#### Unconstrained Optimization

##### Gradient Descent

* If learning rate is too big, oscillation diverges
* If learning rate is too low, it takes a long time to converge.

Learning Rate should be (determine these by checking loss values):
* Near local solution: proceed quickly with small learning rate
* Far from local solution: proceed quickly with large learning rate

Types of Gradient Descent (here L is loss) - tradeoff in convergence vs computation (speed, memory):
* Batch GD $w_{i+1} = w_i - \eta \nabla L(w)$ -- smoother convergence, but loads a lot of data into memory so slower
* Stochastic GD (online/streaming data) (different update rule) -- uses less (only one data at a point), faster
* Mini-batch GD: hybrid of batch and SGD -- (NOTE: for convergence Batch is best if can fit data into memory. There can be some extreme data in a mini-batch which affects strongly, but would affect batch GD less due to averaging out with more data)


### Probability Revision 

* Experiments & Random Variables
* Sample Space $\Omega$
* Events:
    * Set Algebra:
        * Commutative (both union & intersection) $E \cup F = F \cup E$, $E \cap F = F \cap E$
        * Associative (both union & intersection) $(E \cup F) \cup G = E \cup (F \cup G)$, $(E \cap F) \cap G = E \cap (F \cap G)$
        * Distributive (both union on intersection & intersection on union) $(E \cup F) \cap G = (E \cap G) \cup (F \cap G)$, $(E \cap F) \cup G = (E \cup G) \cap (F \cup G)$
    * Independent & Mutually Exclusive events
    * Union $E \cup F$, Intersection $E \cap F$, Null event (mutually exclusive) $E \cap F = \emptyset$
    * Complement $E^c = \Omega - E$, Difference $E - F = E \cap F^c$
* Counting:
    * $n$ distinct objects can be arranged in $n!$ ways
    * Permutations: $^n\mathrm P^r = \frac{ n! }{ (n-r)! }$
    * Combinations: $^n\mathrm C^r = \frac{ n! }{ r! (n-r)! }$
* Probability Measure: a function $P: Event -> [0,1]$ such that for mutually exclusive events, $P(E \cup F) = P(E) + P(F)$


## WIP Lecture 3 - slides not uploaded

Bias-Variance Tradeoff: TODO details

2 estimators $\theta_1$, $\theta_2$ of same unknown parameter $\theta$

Relative Efficiency = $MSE_1 / MSE_2$

Estimator with less MSE (mean squared error) is more efficient. 
So if relative efficiency here is $< 1$, then $\theta_1$ is more efficient.

This is used in Cross-Validation and other places.

**Likelihood** [good explanation](https://www.statlect.com/glossary/log-likelihood):
* Assuming a probability distribution having density function $p(x; \mathbf{\theta})$ (x is single input, $\mathbf{\theta}$ is vector of parameters to be estimated)
* Likelihood is joint probability $P(\mathbf{x} | \mathbf{\theta})$ of observing sample (collection of inputs) $\mathbf{x}$ (in assumed distribution) given parameters $\mathbf{\theta}$ :
    * during training, learn optimal parameter $\hat{\theta}$ to maximize likelihood in [Maximum Likelihood Estimator](#maximum-likelihood-estimator-mle)
    * during validation, if likelihood on test data is low, it means train issue: model overfit on training data OR training data distribution is not representative of test data.
* Since all inputs are assumed to be Independent & Identically Distributed, joint probability is simply product of probability of each input in sample (having $N$ inputs):

$$L(\mathbf{\theta}; \mathbf{x}) = P(x | \theta) = \Pi_{i=1}^N x_i$$

### Estimating Parameters

Estimator = Set of estimated parameters

#### Method of Moments

**Moment** is just generalized average. k'th moment is $E[X^k] = \frac{x_1^k + x_2^k + ... + x_n^k}{n}$ where $n$ is sample size (no. of inputs)

If probability distribution density function $p(x; \mathbf{\theta})$ has $m$ parameters to be estimated, then equate theoritical and sample moments to estimate all paramteters:

$$
\begin{pmatrix} E[X^1 | \theta] \\ E[X^2 | \theta] \\ \vdots \\ E[X^m | \theta] \end{pmatrix} 
= \begin{pmatrix} \frac{1}{n} \sum x_i^1 \\ \frac{1}{n} \sum x_i^2 \\ \vdots \\ \frac{1}{n} \sum {x_i^m} \end{pmatrix}
$$

In general this is non-linear system of equations. In case of linear estimation, this reduces to linear regression using **Ordinary Least Squares**:

$$(X^T X) \beta = X^T y$$

#### Maximum Likelihood Estimator (MLE) 

Assuming training data follows a particular probability distribution, learn optimal parameter $\hat{\theta}$ to maximize likelihood:

$$\hat{\theta} = \argmax{L(\theta; X_{train})}$$

This should maximize accuracy on test data also assuming it follows same distribution.

#### Finding best Estimator

For a probability distribution with density $(p(x; \theta)$, compare 2 estimators (set of estimated parameters) $\hat{\theta_1}$, $\hat{\theta_2}$ (of true value $\theta$) by:
* **Bias**: Find biases of estimators: $Bias(\hat{\theta}) = E[\hat{\theta}] - \theta$
* **Variance**: Find variances of estimators: $Var(\hat{\theta}) = \sigma^2 = \frac{1}{n-1} \sum (x_i - E[x])^2$ (sample variance so denominator is $n-1$ due to Bessel's Correction)
    * Estimator with lower variance is called **Minimum Variance Unbiased Estimator**.
    * If both estimators are unbiased or have equal bias, then this only is better estimator as its MSE will automatically be lower.
* **MSE (Mean Squared Error)**: Lower is better: $MSE = E[(f(X) - X)^2]$

NOTES: 
* **Better to do all 3 checks using test data rather than training data.**
* Estimator with lower MSE is always better. But bias, variance tell why (high bias means underfitting, high variance means overfitting).

## WIP Lecture 4 - PCA (Principal Components Analysis) - Linear Algebra Revision

Coefficient matrix $A$ does NOT need to be square, can be rectangular (in linear system of equations $A x = b$)

Effect of row-operations on determinant:
* add 2 rows => determinant is unchanged
* multiply a row with a constant => deterimant is multiplied with the constant
* swap 2 rows => determinant sign flips

Covariance matrix $x^T x$ is square matrix.

For an eigenvalue $\lambda_i$, which is a root of characterstic equation $det(A - \lambda I) x = 0 \implies (\lambda - \lambda_1)^{p_1} (\lambda_1 - \lambda_2)^{p_2} ... (\lambda - \lambda_n)^{p_n} = 0$
* **Dimension of Eigenspace** is nullity of $A - \lambda_i I$ -  - i.e. no. of eigenvector bases (linearly independent).
* **Algebraic Multiplicity** is no. of times it appears as a root - i.e. power $p_i$.
* **Geometric Multiplicity** is *dimension of its eigen-space.

$$\forall \lambda_i, GeometricMultiplicity \le AlgebraicMultiplicity$$

In real symmetric matrices, eigen-vectors of distinct eigenvalues are orthogonal.

* Matrix $A$ is **diagonalizable** if it can be written as $A = P D P^{-1}$ where $P$ is an invertible matrix and $D$ is a diagonal matrix.
* Square matrix is **orthogonal** iff $P^T = P^{-1}$
* **Spectral Theorem**: A real symmetric matrix is *orthogonally diagonalizable*.
* Square matrix is *diagonalizable* iff for each eigen value, $GeometricMultiplicity = AlgebraicMultiplicity$.
* So from above, for any real symmetric matrix, for all eigen values $GeometricMultiplicity = AlgebraicMultiplicity$.

Construct set of orthonormal eigenvectors for a $n \times n$ real symmetric matrix:
* TODO

**Optimization Problem** (which we try to solve using PCA): 

$$
\max \|A x\|^2 \\
s.t. \quad \|x\| = 1
$$

TODO: optimization problem


## WIP Lecture 5 & 6 - Clustering Analysis

Definitions:
* Centroid is mean of all point vectors. $\mu = \frac{\sum x_i}{N}$
* Radius is max distance of any point from the centroid. $r_i = max |x - \mu|^2$  -- NOTE: we DID NOT take square root here for convinience.
* Diameter is max pairwise-distance between any 2 points. It's NOT related to radius. $di_i = max |x_p - x_q|^2$ (again square root not taken here for convinience)

First, simplest method is K-means Clustering. (slower for larger data)
K (No. of clusters) is determined heuristically / with trial and error.

For large dimensional data, PCA can be done to reduce dimensionality before Clustering.

### WIP K-Means Clustering 

Criticisms / Weaknesses:

* Finds local optima only, not global
* Works with numeric data ony
  * Centroids & distance not defined for other types
  * Use actual data points: medoids (medoid is an alternative way of calculating centroid even for other data types)
* Does not scale well to large data sets
  * Workaround: Sampling (ie train on a sample subset of whole large data)
* Pre-specify number of clusters

#### TODO Heirachical Clustering Types




## Misc

### Calculus

- **Gamma Integral**: $\int_0^\infty x^2 e^{-x / \alpha} dx = 2! \alpha^3$

### Python Code

- Plot **contour** (2D visualization of a 3D surface) using matplotlib: `X, Y = np.meshgrid(x,y,indexing="ij"); Z = polynomial(X,Y); plt.contourf(x,y,Z,levels=20)`


## TODO Practice Questions

* (Coding Questions) Q3, 5 of Assignment 1 (skipped as not required for submission)

