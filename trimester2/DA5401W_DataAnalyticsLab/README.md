# DA5401 : Data Analytics Lab

Prof Arun Ayyar &lt;arun.ayyar@dsai.iitm.ac.in&gt;

This will have practical session for theory that is taught in [Machine Learning](../DA5400W_MachineLearning/) class.

Libraries: 
* Numpy
* Pandas
* Scipy
* Scikit-learn
* Seaborn

**Classification Errors**: RMSE (lower is better), R^2 (higher is better)

### PCA

[PCA Plots](https://bioturing.medium.com/how-to-read-pca-biplots-and-scree-plots-186246aae063):

PCA Score (scatter) Plot:

![PCA Scatter Plot](images/pca_scatter_plot.png)

PCA Loading Plot shows how strongly each characterstic influences a principal component (X,Y axes are 2 principal components, each original component's vector is (x,y) of how much it influences the 2 principal components):
* when 2 feature vectors have a small angle between them => positively correlated
* right angle => likely no correlation
* (diverge) greater than 90 angle => negative correlation

![PCA Loading Plot](images/pca_loading_plot.png)

PCA Biplot (score + loading):

![PCA Biplot](images/pca_biplot.png)

### Optimize methods

Scalar unconstrained minimization (requires strict bounds ie not open-ended `np.inf`): `scipy.optimize.minimize_scalar(lambda x: y(x), bounds=(0,5000), method='bounded')`

Each of these is a method choice available in (vector minimization):

```python
from scipy.optimize import minimize, LinearConstraint, NonLinearConstraint
constraint1 = LinearConstraint(A, lb, ub)    # lb <= A.dot(x) <= ub
bounds = [(x1_lo, x1_hi), (x2_lo, x2_hi), ...]  # lower,upper for each elem in 1D x
minimize(lambda x: objective(x), initial_guess_x, jac=lambda x: objective_gradient(x), method='METHOD', constraints=[constraint1], bounds=bounds)`
```

Feature | SLSQP | BFGS | Nelder-Mead | CG
------- | ----- | ---- | ----------- | ----------
Full Form | Sequential Least SQuares Programming | Broyden-Fletcher-Goldfarb-Shanno | _ | Conjugate Gradient
Theory | Solves a sequence of quadratic subproblems. | A Quasi-Newton method that approximates the Hessian. | Geometric search using a moving simplex (triangle/tetrahedron). | Uses conjugate directions to find the minimum.
Requires Gradient? | Yes | Yes | No | Yes
Convergence | Fast (for constrained) | Very Fast (Superlinear) | Slow | Moderate
Problem Type | Linear constraints | Smooth, medium-scale unconstrained | Noisy or non-differentiable functions. | Large-scale problems (memory efficient).

### K-Means vs DBSCAN Clustering

## K-Means
**Use when:**
- Clusters are spherical/globular
- Clusters are similar in size (but densities differ)
- Number of clusters is known
- Fast computation is needed
- Data has no outliers

**Avoid when:**
- Clusters have arbitrary shapes (moons, circles)
- Clusters have very different sizes or densities
- Data contains many outliers
- Number of clusters is unknown

## DBSCAN
**Use when:**
- Clusters have arbitrary shapes
- Number of clusters is unknown
- Data contains outliers/noise
- Outlier detection is important
- Clusters are well-separated by density

**Avoid when:**
- Clusters have very different densities
- High-dimensional data (curse of dimensionality)
- Parameters (eps, min_samples) are hard to tune
- All points must be assigned to clusters

### Agglomerative Clustering

4 Linkage Methods: Ward (recommended usually: min within-cluster var), distance betwee any 2 points: Single (min), Complete (max), Average

## Midsem Syllabus

- [ ] Optimization: Linear `linalg` & Non-Linear `minimize_scalar`, `minimize` (SLSQP, BFGS, Nelder-Mead, CG)  (scipy.optimize) 
- [ ] MLE, MOM, Bootstrapping (numpy) 
- [x] PCA `sklearn.preprocessing.StandardScaler, sklearn.decomposition.PCA`
- Clustering (sklearn.cluster) : 
    - [x] `KMeans(num_clusters=k)`
    - [ ] `AgglomerativeClustering(num_clusters=k, method='ward')` (heirachical/tree-based clustering)
        - TODO SKIPPED: Agglomerative from-scratch implementation
    - [x] `DBSCAN(eps=0.5, num_samples=5)`
- [x] Linear Regression `sklearn.linear_model.LinearRegression` 
- Plots (matplotlib):
    - [x] K-Means: kmeans elbow plot `kmeans.inertia_` vs k (NOTE: k-means fails on data with non-spherical clusters, eg. concentric circles)
    - [x] K-Means: silhouette score plot `sklearn.metrics.silhoutte_score(X, labels)` vs k
    - [x] K-Means: clusters plot `cluster_labels = kmeans.fit_predict(X_scaled)` OR `kmeans.fit(X_scaled); kmeans.labels_`
    - [ ] KNN K-Distance plot to choose Epsilon for DBSCAN clustering: k'th nearest neighbour's distances (ascending) VS just indices (1,2...)
    - [x] Agglomerative `from scipy.cluster.hierarchy import dendrogram, linkage`: dendogram plot is "tree" of cluster heirachies (on top is all data in one cluster, then divide into parts until each point is a cluster)

## Notebooks

- [x] Pandas 1 & 2 
- [ ] ALMOST DONE: Industrial AI Week 1
- [x] Bootstrap & MoM
- [x] Probability Statistics
- [ ] WIP Optimization Methods
- [ ] PCA_Detailed_Tutorial
- [ ] WIP Optimization_PCA
- [ ] Clustering
- [ ] Regression (linear: ordinary & total least squares, logistic, etc.) - notebook not yet shared
- [ ] 5 Plots: K Means Clustering (Elbow Plot (Inertia vs k), Silhoutte Score vs k, Scatter colored by cluster labels), KNN (distance plot, dendogram)

SKIP (not coming in midsem exam): 
* Spectre Clustering

## Problems

- [x] *Part 4: Practice Exercises* cell in *Bootstrap_and_Method_of_Moments.ipynb*

### NOT IN MIDSEM SYLLABUS

Manual gradient descent (diff types) in linear regression