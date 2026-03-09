```python
from itertools import permutations, combinations, combinations_with_replacementions
import numpy as np      # np.median, np.percentile
from scipy.special import comb, perm, factorial
import scipy # scipy.stats.mode, scipy.stats.norm.pdf
```

Combinations with repetitions: $n+r-1 \choose r$

Covariance $cov(X,Y) = E[(x - \bar{x}) (y - \bar{y})]$

## Hypothesis Tests

```python
critical_value = stats.norm.ppf(alpha/2) # (mean) left-tailed H0: sample <= population ; 1-alpha/2 (right H0: sample >= population), alpha (2-tailed: sample = population)
t_statistic, p_value = stats.ttest_1samp(X, mu0 = 0.25, alternative='less')    # 'less' | 'greater' | 'two-sided'
```

## Optimization (`scipy.optimize`)

*Quadratic*: $\frac{1}{2} x^T Q x + r x, \quad \frac{dy}{dx} = Q^T x + r$

* **Scalar:** `minimize_scalar(f, bounds=(0,5), method='bounded')`
* **Linear:** `linprog(c, A_ub=A, b_ub=b, bounds=x_bounds)` (minimizes $c^T x$).
* **Vector (Unconstrained/Constrained):** `minimize(f, x0, method='METHOD', constraints=[LinearConstraint(A,lb,ub)], bounds=bnds)`
    * SLSQP: Best for constrained, uses gradients.
    * BFGS: Fast Quasi-Newton, requires gradients.
    * CG (Conjugate Gradient): Memory efficient for large-scale problems.
    * Nelder-Mead: No gradient needed; good for noisy/non-differentiable functions.
    * *Speed*: SLSQP > BFGS > CG > Nelder-Mead

## sklearn.metrics.PCA(n_components=2) & Statistics

* **PCA Steps:** `StandardScaler` (Mean 0, Var 1). Covariance Matrix `np.cov(X.T)`. Eigen-decomposition `np.linalg.eig`. Sort eigenvectors by eigenvalues (descending).
* **Explained Variance:** Equal to the eigenvalues.
* **Loadings:** `pca.components_`. Small angle = pos. correlation; 90 degree = no correlation; > 90 degree = neg. correlation.
* **Bootstrap:** `np.random.choice(data, size=n, replace=True)` to estimate CI via `np.percentile`. Standard Error $SE[\bar{x}] = \sigma / \sqrt{n}$
* **MoM:** Match sample moments to theoretical moments to solve for parameters (e.g., $\bar{x} = 1/\lambda$ for exponential).


Distribution | $E[X]$          | $Var(X) = E[X^2] - E[X]^2$
------------ | --------------- | --------------------------
Uniform      | $\frac{a+b}{2}$ | $\frac{(b-a)^2}{12}$
Bernoulli    | $p$             | _
Binomial     | $n p$           | _
Poisson      | $\lambda$       | _
Exponential  | $1 / \lambda$   | _
Normal       | $\mu$           | $\sigma$


## Clustering (`sklearn.cluster`)

*Speed*: KMeans > DBSCAN > Agglomerative > Spectral

* `KMeans(n_clusters=k)`: Spherical clusters. Sensitive to outliers.
    * *Evaluation:* Elbow Plot (`kmeans.inertia_` vs. $k$), `sklearn.metrics.silhoutte_score(X, labels)` vs $k$.
    * Default, assumes spherical clusters of similar density.
* `DBSCAN(eps=0.5, min_samples=5)`: Arbitrary shapes + noise detection (`-1` label).
    * `eps` Epsilon is max cluster radius / neighbourhood distance
    * Find `eps` using K-Distance plot (k'th Nearest Distance vs 1,2,3..): `sklearn.neighbours.NearestNeighbours` (`.fit()`, `.kneighbours()`)
    * Use for arbitary cluster shapes
* `Agglomerative(n_clusters=k, method="ward")`: Hierarchical.
    * *Linkage*: ward (Default: min intra-cluster variance), distance bw any 2 points: single (min), complete (max), average
    * *Plot*: (tree of clusters) `scipy.cluster.hierarchy.dendrogram(scipy.cluster.linkage(X, method="ward"))`
    * Can handle clusters with varying density
* **Spectral:** Good for non-convex/graph data (eg. spiral clusters).
    * *Selection:* **Eigengap plot** (largest gap between consecutive eigenvalues of Laplacian) -- TODO.

```python
# Spectral Clustering Laplacians -- Eigen-gap plot
W = rbf_kernel(X, gamma=1.0)
D = np.diag(W.sum(axis=1))
L_norm = np.eye(len(X)) - np.linalg.inv(np.sqrt(D)) @ W @ np.linalg.inv(np.sqrt(D))
# TODO: mk Eigen-gap plot to choose best k (where difference bw successive eigenvalues is greatest)
```

TODO: from-scratch implementations: K-Means, DBSCAN, Agglomerative, Spectral

## Cluster Evaluation Metrics

| Metric | Needs Ground-Truth Labels? | Best Value | Context | Method
| --- | --- | --- | --- | ---
| **Silhouette** | No | 1 | Cohesion vs. Separation | `sklearn.metrics.silhoutte_score(X, labels_predicted)`
| **Purity** | Yes | 1 | ratio of correct cluster label (dominant class) = ground-truth | _
| **Rand-INDEX** | Yes | 1 | Pair-wise Agreement | `sklearn.metrics.rand_score(labels_true, labels_predicted)`
| **Adj. RAND** | Yes | 1 | Similarity corrected for chance | `sklearn.metrics.adjusted_rand_score(labels_true, labels_predicted)`
| **Entropy** | Yes | 0 | Uncertainty within clusters: Avg of $- \sum p_i \log_2(p_i)$, weighted by cluster size |

## `sklearn.linear.LinearRegression()`

* **OLS Solution:** $w = (X^T X)^{-1} X^T y$
* **Properties:** Residuals $(y - \hat{y})$ are orthogonal to the feature space $X$ so $(y - \hat{y})^T X \approx 0$ (approx for small error tolerance).
* **Metrics:** RMSE (lower is better), $R^2$ (higher is better).

```python
# OLS from scratch
X_bias = np.column_stack([np.ones(X.shape[0]), X]) # Add bias
w = np.linalg.solve(X_bias.T @ X_bias, X_bias.T @ y)
P = np.linalg.inv(X_bias.T @ X_bias) @ X_bias.T
```

## Spectral Clustering Theory

TODO: understand

Spectral clustering is a graph-based technique that partitions data by analyzing the eigenvalues (spectrum) of a Laplacian matrix derived from the data's similarity graph. It is particularly effective for non-convex, complex cluster structures. [1, 2]  
Here are the key mathematical formulas and components of the spectral clustering algorithm. 
1. Similarity/Affinity Matrix ($W$) 
The first step is to define a pairwise similarity matrix $W$ of size $n \times n$, where $w_{ij}$ represents the similarity between data points $x_i$ and $x_j$. 

• Gaussian (RBF) Kernel: $w_{ij} = \exp\left(-\frac{\|x_i - x_j\|^2}{2\sigma^2}\right)$ 
• -Nearest Neighbors: $w_{ij} = 1$ if $x_i \in kNN(x_j)$ or $x_j \in kNN(x_i)$, otherwise $0$ [6, 7, 8]  

2. Degree Matrix ($D$) and Laplacian Matrix ($L$) [9]  
The degree matrix $D$ is a diagonal matrix containing the sum of the similarities for each point: $D_{ii} = \sum_{j=1}^n w_{ij}$ 
 
The Unnormalized Graph Laplacian $L$ is defined as: $L = D - W$ 
 
3. Normalized Laplacian Matrices 
To handle different data densities, normalized versions are often used: 

• Symmetric Normalized Laplacian (): $L_{sym} = D^{-1/2}LD^{-1/2} = I - D^{-1/2}WD^{-1/2}$ 
 
• Random Walk Normalized Laplacian (): $L_{rw} = D^{-1}L = I - D^{-1}W$ 
 

4. Eigenvalue Decomposition and Embedding 
The core of the algorithm involves finding the first $k$ eigenvectors ($u_1, \ldots, u_k$) of the Laplacian, where $k$ is the number of clusters. 

• Eigenproblem: $Lu = \lambda u$ 
• Matrix : Form a matrix $U \in \mathbb{R}^{n \times k}$ with eigenvectors $u_1, \ldots, u_k$ as columns. 
• Embedding: Let $y_i \in \mathbb{R}^k$ be the vector corresponding to the $i$-th row of $U$. This projects the original $m$-dimensional data points into a new $k$-dimensional subspace. [1, 3, 6, 13]  

5. Final Clustering 
Run K-Means on the rows of the projected matrix $U$ (or $T$ for normalized) to obtain final cluster assignments $C_1, \ldots, C_k$. 

• For , rows are normalized to unit length: $t_{ij} = \frac{u_{ij}}{(\sum_k u_{ik}^2)^{1/2}}$. [3]  

