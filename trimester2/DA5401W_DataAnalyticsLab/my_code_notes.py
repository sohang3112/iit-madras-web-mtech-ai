#region Industrial AI Week 1 - basic python, numpy, pandas, seaborn, scipy
import numpy as np
import seaborn as sns
iris = sns.load_dataset('iris')    # pandas df

from scipy import constants, special, integrate, linalg, fftpack, signal, interpolate, stats, optimize
print(constants.pi, constants.c)      # c = speed of light
print(f"Bessel Function (j0): {special.jn(0, 1.0)}")
val, err = integrate.quad(lambda x: x**2, 0, 1)   # err = estimated absolute error
# linalg.det(A), linalg.inv(A)      # A is a matrix: 2D numpy array
sig = np.array([1, 2, 1, -1, 1.5])
fftpack.fft(sig)     # Fourier Transform
signal.resample(sig, 10)

x = np.arange(10)
y = np.sin(x)
f = interpolate.interp1d(x, y, kind='cubic')
print(f(4.5))

stats.norm.pdf(0)     # probability at x=0
# TODO: scipy.optimize (last cell of Industrial AI Week 1 notebook)

#endregion

#region Pandas 1 & 2
import pandas as pd
s = pd.Series([1,2,3,4], index=['a','b','c','d'])    # series with explicit index
print(s.index)
print(s[['a','b']])        # lookup using multiple index values, get series
print(s[[0,1,2]])          # lookup using int indices
print(s.pct_change())      # relative change -- to get %age, multiply by 100

dates = pd.date_range('2016-04-01', '2016-04-06')
temperatures = pd.Series([37,38,32,34,39,31], index=dates)

# pd.to_datetime()
# df['column'].plot()  OR ELSE df['column'].plot(kind='bar')  # against index
# df = df.set_index('Date'); df.index.month
# df.size == df.shape[0] * df.shape[1]

# Adding Columns:
# df['new_column'] = value
# df.insert(1, 'new_column', value)
# df[:, 'new_column'] = value

# Deleting columns
# del df['column1', 'column2']
# col = df.pop('column')

# df1.join(df2)       # left join on index by default; args on='column', how='inner'

#endregion

#region Bootstrap_and_Method_of_Moments
# all random distributions have size argument (how many data points to generate)
lambda_true = 2
np.random.exponential(scale=1 / lambda_true, size=10)   # scale is mean; in exponential dist, mean = 1 / lambda

# Bootstrap (Standard Error, Confidence Interval) vs Method of Moments

# Bootstrap: mk many samples of distribution (with replacement):
sample = np.random.choice(population, size=n, replace=True)
# since no. of samples is large, estimate (of Bootstrap) follows normal distribution around true value of population

# Method of Moments: draw many independent samples (init with np.random.exponential())
# apply MoM to each sample to get lambda, then get probability using formula
# plot sample vs probab, sample vs lambda
# true & MoM: y = lambda * np.exp(-lambda * x)   # exponential distribution probab formula

np.percentile(sample, [2.5, 97.5])     # one or more percentile values from sample, so this gives 95% CI range
#endregion

#region Probability_Statistics

# Bayes: Posterior P(y | x) = (Likelihood P(x | y) * Prior P(y)) / Marginal Probability P(x)
# Sensitivity = P(Test+ | Disease)  [ True Positive rate ]
# Specificity = P(Test- | No Disease)  [ True Negative rate ]

# Central measure: Mode for categorical data, Median for skewed, Mean for symmetrical data

# Hypothesis Tests:
from scipy.stats import binomtest, ttest_1samp, ttest_ind
binomtest(n_heads, n_total, p_null_hypothesis, alternative='two-sided').pvalue    # 0.05 p_null_hypothesis is usually used
t_statistic, p_value = ttest_1samp(sample_array, population_mean)
t_statistic, p_value = ttest_ind(sample1, sample2)    # 2-sample T Test
#endregion

#region Optimizaton_Methods
x = np.linspace(-2, 2, 200)
y = np.linspace(-2, 2, 200)
X, Y = np.meshgrid(x, y)    # mesh req before contour
# Z = a * X**2 + (b + c) * X * Y + d * Y**2
# this is equivalent to matrix form x^T Q x
Q = np.array([[a,b], [c,d]])
quadratic = lambda x: x @ Q @ x    # x @ Q - x broadcast to (1,n) [1 dimension prepended], then back to 1D (n,) after multiply; Q @ x - 1 dimension appended and removed
# quadratic = lambda x: np.dot(np.dot(x,Q), x)         # equivalent
Z = np.zeros_like(X)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Z[i,j] = quadratic(np.array([ X[i,j], Y[i,j] ]))

import scipy
result = scipy.optimize.minimize_scalar(lambda x: y(x), bounds=(0,5000), method='bounded')
print(f'Optimal point: (x={result.x}, y={result.fun})')

# TODO: go through rem cells from Unconstrained Optimization
#endregion

#region PCA_Detailed_Tutorial
# PCA from scratch (standardize, covariance matrix > sort eigen-vectors descending by eigen-values, pick top k ; explained variance = eigen-value)
covariance_matrix = np.cov(X)      
eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)       # each column is an eigen-vector
# TODO
#endregion

#region Optimization_PCA
result = scipy.optimize.linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(x_lo, x_high))  # result.x (optimal point array), result.fun (objective func value at optimal point)
# Linear Optimization (objective and constraints are all linear): params are numpy arrays, only c is required, rest are optional
# minimize c @ x such that A_ub @ x <= b_ub, A_eq @ x = b_eq, x_lo <= x <= x_high

constraint = scipy.optimize.LinearConstraint(A, lb, ub)   # lb <= A.dot(x) <= ub  (for open-ended, pass one bound np.inf, for exact eq, pass same lb, ub)
bounds = [(x1_lo, x1_hi), (x2_lo, x2_hi), ...]   # list of bounds for each elem in 1D x
result = scipy.optimize.minimize(lambda x: objective_function(x), initial_guess_x, method='SLSQP', jac=lambda x: objective_gradient(x),
                  constraints=[constraint], bounds=bounds)
#endregion

#region Clustering_Tutorial
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# TODO: clustering from scratch: Agglomerative, DBSCAN, Spectral

# Input must be standardized (mean 0, variance 1) before PCA
X_scaled = StandardScaler().fit_transform(X_raw)
pca = PCA(n_components=3)  # n_components is optional
X_pca = pca.fit_transform(X_scaled)
# pca.explained_variance_ (absolute vals), pca.explained_variance_ratio_ (0-1 ratios)
pca.components_ # shape=(n_components, n_original_features) - set of rows are bases (principal component vectors) for the new features returned
                # "loadings" (eigenvectors of covariance matrix - directions of maximum variance in original data)
                # tells for each PCA feature, how much did each original feature contribute?
                # used for Loadings Plot

# Input must also be standardized before K Means to deal with different units of measurement in each feature
# Exception: when all features have same unit, as in PCA features
inertias, silhoutte_scores = [], []
for k in range(2,11):
    kmeans = KMeans(n_clusters=k)
    cluster_labels = kmeans.fit_predict(X_scaled)  # OR: kmeans.fit(X_scaled); kmeans.labels_
    # Centroids of each clusters are in kmeans.cluster_centers_
    inertias.append(kmeans.inertia_)
    silhoutte_scores.append(sklearn.metrics.silhoutte_score(X_scaled, cluster_labels))
# Elbow Plot: inertias vs k

# Datasets where K-Means fails:
# * crescent moon clusters (a circle with one semi-circle moved half a radius) -- DBSCAN works
# * concentric circle clusters -- DBSCAN works

# Datasets where DBSCAN fails:
# * clusters with different densities (radius) -- K-Means works

cluster_labels = DBSCAN(eps=0.5, min_samples=5).fit_predict(X_scaled)       # also requires standardized data
# "noise" points (not in any cluster) are assigned label -1
# epsilon determines max cluster / neighbourhood size, min_samples is min no. of points for a neighbourhood to be considered cluster
# NOTE: we can't specify no. of clusters, it's automatically determined

# K-Distance plot to choose epsilon for DBSCAN
nbrs = sklearn.neighbours.NearestNeighbours(n_neighbours=min_samples)
nbrs.fit(X_scaled)
distances = nbrs.kneighbours(X_scaled)
distances = np.sort(distances[:, k-1], axis=0)
plt.plot(distances)       # y=distances, x=1,2,3..
#endregion

#region Complete_Cluster_Tutorial_full.ipynb
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# Agglomerative Dendtogram (tree-like heirachy of clusters)
linkage_matrix = linkage(X, method='ward')   # ward (recommended usually: min within-cluster var), distance betwee any 2 points: Single (min), Complete (max), Average
_agglo_info_dict = dendrogram(linkage_matrix)    
plt.show()

cluster_labels = AgglomerativeClustering(n_clusters=3, method='ward').fit_predict(X_scaled)    # also requires standardized data
# choose best k (num_clusters) based on silhoutte score plot
# TODO SKIPPED: Agglomerative Clustering from-scratch implementation

# Heirachical Clustering: Agglomerative (AGNES starts from every point is a cluster then merges iteratively), Divisive (DIANA starts with all data in a cluster, breaks iteratively)

# Spectral Clustering
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.cluster import SpectralClustering

cluster_labels = SpectralClustering(n_clusters=2, n_init=2).fit_predict(X_scaled)      # also requires standardized input

# TODO: understand: Eigengap plot to find optimal k (k when largest difference between eigenvalues)
W_full = rbf_kernel(X_circles, gamma=1.0)
D_full = np.diag(W_full.sum(axis=1))
D_inv_sqrt_full = np.diag(1.0 / np.sqrt(np.diag(D_full)))
L_norm_full = np.eye(len(X_circles)) - D_inv_sqrt_full @ W_full @ D_inv_sqrt_full
eigenvalues_full, _ = eigh(L_norm_full)
plt.plot(eigenvalues_full)

# Cluster Evaluation Metrics
sklearn.metrics.silhoutte_score(X, labels_predicted)       # does not require ground-truth labels (higher better)
# Req ground-truth labels: Purity in [0,1] (higher better): cluster label = most common label in cluster. Purity = no. of correctly matched ground-truth and cluster labels / total points
# Req ground-truth labels: Entropy (higher better): entropy of a single cluster is H(C_i) = - sum(p_j log2(p_j)) where p is probability of class j being assigned to cluster i
                           # total entropy = mean of all clusters' entropy, weighted by no. of points in each cluster
#endregion

#region Complete_Clustering_Tutorial_full2.ipynb
# TODO: K-Means from scratch
#endregion

#region Regression
from sklearn.linear_model import LinearRegression
linreg = LinearRegression().fit(X, y)
ypred = linreg.predict(X)

# Ordinary Least Squares: w = (X^T X)^{-1} X^T y
X = np.hstack([X, np.ones(X.shape[0])])    # add bias term
w = np.linalg.solve(X.T @ X, X.T @ y)
#P = (X.T @ X)**(-1) @ X.T        # projection matrix
ypred = X @ w
ssr = np.sum((ypred - y)**2)     # Sum of Squared Residuals (minimized)

assert np.all(np.isclose(X.T @ (ypred - y), 0))    # X^T residual should be close to 0 (orthogonal)
#endregion

#region 5 Plots: K-Means (Elbow plot: Inertia vs k, Silhoutte Score vs k, colored clusters), KNN (distance plot, dendogram)
plt.axvline(x=3, color='red', linestyle='--')
#endregion