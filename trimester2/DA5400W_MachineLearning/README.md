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

**Method of Moments** (method to estimate parameters) (moments of sample & population are equated and then solve equation)
- moment is just generalized average. kth moment is $E[X^k] = \frac{x_1^k + x_2^k + ... + x_n^k}{n}$
- find sample mean, and equate it to theoritical population mean (according to assumed distribution). 
  Eg. if assuming Poisson (rare event distrib), then set its mean $\lambda$ to found sample mean.
  TODO: how to know which distribution to assume? Eg. Normal, Poisson etc.

**Maximum Likelihood Estimator**: another method to estimate parameters


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


## WIP Lecture - Clustering Analysis

Definitions:
* Centroid is mean of all point vectors. $\mu = \frac{\sum x_i}{N}$
* Radius is max distance of any point from the centroid. $r_i = max |x - \mu|^2$  -- NOTE: we DID NOT take square root here for convinience.
* Diameter is max pairwise-distance between any 2 points. It's NOT related to radius. $di_i = max |x_p - x_q|^2$ (again square root not taken here for convinience)

First, simplest method is K-means Clustering. (slower for larger data)
K (No. of clusters) is determined heuristically / with trial and error.

For large dimensional data, PCA can be done to reduce dimensionality before Clustering.




