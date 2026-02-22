# Industrial AI Week 1 - basic python, numpy, pandas, seaborn, scipy
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

# Pandas 1 & 2
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