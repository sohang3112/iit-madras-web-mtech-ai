# DA5000 Linear Algebra & Optimization Assignment 4

Roll No. DA25M622, Name: Sohang Chopra

## Solution 1

$$f(x) = x^4 - 4x^2 \, x \in \mathbb{R}$$

1. For stationarity, first derivative must be 0: $f'(x) = 4x^3 - 8x = 0$
Solving this, stationary points are $x = 0, \pm \sqrt{2}$

2. Second Order Derivative and points' classification: 
$$
f''(x) = 12x^2 - 8 \\
f''(0) = -8 < 0 \implies \text{Local maximum} \\
f''(\pm \sqrt{2}) = 12*2 - 8 = 16 > 0 \implies \text{Local minimum}
$$

3. Values at stationary points: $f(0) = 0, f(\pm \sqrt{2}) = -4$
$\pm \sqrt{2}$ are Global Minimizers by looking at graph. 
TODO: instead of graph give some other justification, not sure what.

4. Local Maxima $0$ is NOT Global Maxima by looking at graph (function output is unbounded and goes to infinity). 
TODO: instead of graph, give some other justification.

--------

## Solution 2

NOTE: Here $\operatorname{diag}([...])$ denotes Diagonal Matrix with given values.

$$
F(x) = \frac{x_1^3 + x_2^3 + x_3^3}{2} \\
\nabla F = \frac{3}{2} \begin{pmatrix} x_1^2 \\ x_2^2 \\ x_3^2 \end{pmatrix} \\
\nabla^2 F = 3 \operatorname{diag}([x_1, x_2, x_3])
$$

For stationarity, gradient must be 0: $\nabla F = 0 \implies x_1 = x_2 = x_3 = 0$.

Hessian Matrix at (0,0,0) is $H = 3 diag([0, 0, 0]) = 0$ => Zero matrix is indefinite so cannot be sure it is minima/maxima or not.

TODO: now how to solve further to find minimizer and minimum value?

--------

## Solution 3

$$
\min\limits_{x \in \mathbb{R}^2} F(x) = \frac{1}{2} x_1^2 + 2 x_2^2 \\ 
\text{such that} \, A^T x = b \; \text{where} \, A = \begin{pmatrix} 1 \\ 3 \end{pmatrix}
$$

(a) Lagrangian $\mathcal{L}(x, \mu) = \frac{1}{2} x_1^2 + 2 x_2^2 + \mu (x_1 + 3x_2 - b)$ 
where $\mu$ is multiplier for given equality constraint.

(b) KKT Stationarity conditions:
$$
\nabla L = 0 \\
\implies \begin{pmatrix} x_1 + \mu \\ 4 x_2 + 3 \mu \end{pmatrix} = 0 \\
$$

(c) Solving stationarity gives $x_1 = \frac{4}{3} x2 = - \mu$. This is independent of constant $b$ (RHS in equality constraint).

---------

## Solution 4

$$
\min f(x,y) = (x-1)^2 + (y+2)^2 = x^2 + y^2 - 2 x + 2 y + 5 \\
\nabla f = 2 \begin{pmatrix} x - 1 \\ y + 1 \end{pmatrix} \\
\nabla^2 f = 2 \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}
$$

1. Gradient Descent update rule using given learning rate $\alpha=0.25$ and starting point $(x_0,y_0) = (0,0)$:

$$(x_{k+1}, y_{k+1}) = (x_k, y_k) - \alpha \nabla F = (x_k, y_k) - 0.25 * 2 (x_k - 1, y_k + 1) = 0.5 (x_k + 1, y_k - 1)$$

Updates for 3 iterations:

$$
x_0 = (0,0) \\
x_1 = (0+1, 0-1) = (1,-1) \\
x_2 = (1+1,-1-1) = (2,-2) \\
x_3 = (2+1,-2-1) = (3,-3)
$$

2. To find stationary value, $\nabla F = 0 \implies (x,y) = (1,-1)$. $\nabla^2 F = 2 I > 0$, so $(1,-1)$ is minimizer point.
Distance of gradient descent updated point $x_3=(3,-3)$ from optimal point $(1,-1)$ is $2 \sqrt{2}$.

3. Newton update method:

$$
(x_{k+1}, y_{k+1}) = (x_k, y_k) - (\nabla^2 f(x_k,y_k))^-1 \nabla f(x_k,y_k) \\
\implies (x_{k+1}, y_{k+1}) = (x_k, y_k) - (2I)^{-1} * 2 (x_k-1, y_k+1) \\
\implies (x_{k+1}, y_{k+1}) = (1,-1)
$$

So Newton method converges directly in single iteration to optimal solution $(x^*,y^*) = (1,-1)$ from any starting point.

----------------

## Solution 5

$$
\min\limits_{(x,y) \in \mathbb{R}^2} f(x,y) = x + 3y \\
\text{subject to} \; x^2 + 2y^2 \le 1 , x + y \le 1 , y \le x
$$

1. Let Lagrangian multipliers for the inequality constraints be $\lambda_1, \lambda_2, \lambda_3$. 

Lagrangian function is:

$$\mathcal{L}(x,y,\lambda_1,\lambda_2,\lambda_3) = x + 3y - \lambda_1 (x^2 + y^2 - 1) + \lambda_2 (x + y - 1) - \lambda_3 (y - x)$$

KKT Conditions are:

* Stationarity $\nabla \mathcal{L} = 0$:

$$\begin{pmatrix} -2 \lambda_1 x + \lambda_2 + \lambda_3 + 1 \\ -2 \lambda_1 y + \lambda_2 - \lambda_3 + 3 \end{pmatrix} = 0$$

* Primal Feasability:

$$
x^2 + 2y^2 \le 1 \\
x + y \le 1 \\
y \le x
$$

* Dual Feasability: Inequality Lagrangian multipliers must be non-negative: $\lambda_1 \le 0, \lambda_2 \le 0, \lambda_3 \le 0$

* Complementary Slackness:

$$
\lambda_1 (x^2 + y^2 - 1) = 0 \\
\lambda_2 (x + y - 1) = 0 \\
\lambda_3 (y - x) = 0
$$

2. Solving: TODO
