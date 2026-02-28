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

from matplotlib import pyplot as plt
plt.axhline(y)   # horizontal line at level y
plt.fill_between(x, y1, y2)   # shade area (eg. feasible region in optimization)
plt.plot(x, y, 'r-')   # r- -> r is red, - is dashed; g- -> green dashed line, etc.

np.percentile(sample, [2.5, 97.5])     # one or more percentile values from sample, so this gives 95% CI range
#endregion

#region Probability_Statistics
plt.imshow(grid)   # grid is a 2D numpy array of 0-1 (float) or 0-255 (int); (M,N) grayscale or (M,N,3) color image shape
plt.xticks(range(6)); plt.xticklabels(range(1,7))   # xticks sets X marker points left to right, xticklabels sets actual labels at these; similarly yticks(), yticklabels() top to bottom

# Bayes: Posterior P(y | x) = (Likelihood P(x | y) * Prior P(y)) / Marginal Probability P(x)
# Sensitivity = P(Test+ | Disease)  [ True Positive rate ]
# Specificity = P(Test- | No Disease)  [ True Negative rate ]

# Central measure: Mode for categorical data, Median for skewed, Mean for symmetrical data

plt.boxplot([array1, array2, ...])   # arrays whose box plots to plot (one box for each)

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

# Both show 3D in 2D plot
plt.contour(X, Y, Z, levels=20)      # shows 2D cutoff of 3D plot at different z (as many as specified levels)

fig, axes = plt.subplots(nrows=1, ncols=1)
axes[0,0].plot_surface(X, Y, Z)    # show whole surface; .plot_surface() method only there on axis, not available directly in plt

import scipy
result = scipy.optimize.minimize_scalar(lambda x: y(x), bounds=(0,5000), method='bounded')
print(f'Optimal point: (x={result.x}, y={result.fun})')

ax1.grid(True, alpha=0.3)   # TODO
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))   # TODO

# TODO: go through rem cells from Unconstrained Optimization
#endregion

#region PCA_Detailed_Tutorial
# TODO
#endregion

#region Optimization_PCA
scipy.optimize.linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(x_lo, x_high))
# Linear Optimization (objective and constraints are all linear): params are numpy arrays, only c is required, rest are optional
# minimize c @ x such that A_ub @ x <= b_ub, A_eq @ x = b_eq, x_lo <= x <= x_high

# TODO
#endregion

#region Clustering_Tutorial
# TODO
#endregion

#region Regression
# TODO
#endregion