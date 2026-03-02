# DA5401 : Data Analytics Lab

Prof Arun Ayyar &lt;arun.ayyar@dsai.iitm.ac.in&gt;

This will have practical session for theory that is taught in [Machine Learning](../DA5400W_MachineLearning/) class.

Libraries: 
* Numpy
* Pandas
* Scipy
* Scikit-learn
* Seaborn

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

SKIP (not coming in exam): 
* plotting image output
* Spectre Clustering

## Problems

- [x] *Part 4: Practice Exercises* cell in *Bootstrap_and_Method_of_Moments.ipynb*