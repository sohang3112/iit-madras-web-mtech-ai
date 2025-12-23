# DA5000 Linear Algebra & Optimization Assignment 4

Roll No. DA25M622, Name: Sohang Chopra

## Solution 1

$$
f(x) = x^4 - 4x^2 \, x \in \mathbb{R}

$$

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

---

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

---

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

---

## Solution 4

$$
\min f(x,y) = (x-1)^2 + (y+2)^2 = x^2 + y^2 - 2 x + 2 y + 5 \\
\nabla f = 2 \begin{pmatrix} x - 1 \\ y + 1 \end{pmatrix} \\
\nabla^2 f = 2 \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}

$$

1. Gradient Descent update rule using given learning rate $\alpha=0.25$ and starting point $(x_0,y_0) = (0,0)$:

$$
(x_{k+1}, y_{k+1}) = (x_k, y_k) - \alpha \nabla F = (x_k, y_k) - 0.25 * 2 (x_k - 1, y_k + 1) = 0.5 (x_k + 1, y_k - 1)

$$

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

---

## Solution 5

The optimization problem is:
$$
\min_{(x,y)\in\mathbb{R}^2} f(x,y)=x+3y
$$
subject to
$$
g_1(x,y)=x^2+2y^2-1\le 0,\quad
g_2(x,y)=x+y-1\le 0,\quad
g_3(x,y)=y-x\le 0.
$$

1.

Introduce Lagrange multipliers $\lambda_1,\lambda_2,\lambda_3\ge 0$ for $g_1,g_2,g_3$ respectively.  

The Lagrangian is
$$
\mathcal L(x,y,\lambda)=x+3y
+\lambda_1(x^2+2y^2-1)
+\lambda_2(x+y-1)
+\lambda_3(y-x).
$$

* Stationarity:
$$
\nabla_{x,y}\mathcal L=0 \;\Longrightarrow\;
\begin{cases}
1+2\lambda_1 x+\lambda_2-\lambda_3=0,\\
3+4\lambda_1 y+\lambda_2+\lambda_3=0.
\end{cases}
$$

* Primal feasibility
$$
x^2+2y^2\le 1,\quad x+y\le 1,\quad y\le x.
$$

* Dual feasibility
$$
\lambda_1,\lambda_2,\lambda_3\ge 0.
$$

* Complementary Slackness
$$
\lambda_1(x^2+2y^2-1)=0,\quad
\lambda_2(x+y-1)=0,\quad
\lambda_3(y-x)=0.
$$

2. Because the objective is linear and the feasible set is compact and convex, the optimum lies on the boundary.

* Case: only the quadratic constraint active.

Assume $\lambda_1>0,\quad \lambda_2=\lambda_3=0$.

Stationarity reduces to $1+2\lambda_1 x=0,\qquad3+4\lambda_1 y=0$, which gives $x=-\frac{1}{2\lambda_1},\qquad y=-\frac{3}{4\lambda_1}$.

Complementary slackness with $g_1=0$:
$$
x^2+2y^2=1.
$$

Substitute:
$$
\frac{1}{4\lambda_1^2}
+2\cdot\frac{9}{16\lambda_1^2}
=1
\;\Longrightarrow\;
\frac{11}{8\lambda_1^2}=1
\;\Longrightarrow\;
\lambda_1^2=\frac{11}{8}.
$$

Hence
$$
\lambda_1=\sqrt{\frac{11}{8}},
$$
and
$$
x^*=-\sqrt{\frac{2}{11}},\qquad
y^*=-\frac{3}{2}\sqrt{\frac{2}{11}}.
$$

Feasibility check:
$$
x^*+y^*=-\frac{5}{2}\sqrt{\frac{2}{11}}<1,\qquad
y^*<x^*.
$$
Both linear constraints are strictly satisfied, so $\lambda_2=\lambda_3=0$ is consistent.

3. Objective value at the candidate point

$$
f(x^*,y^*)=x^*+3y^*
=-\sqrt{\frac{2}{11}}-\frac{9}{2}\sqrt{\frac{2}{11}}
=-\frac{11}{2}\sqrt{\frac{2}{11}}
=-\sqrt{\frac{11}{2}}.
$$

So all KKT conditions are satisfied at
$$
(x^*,y^*)=\left(-\sqrt{\frac{2}{11}},\;-\frac{3}{2}\sqrt{\frac{2}{11}}\right),
$$
with multipliers
$$
\lambda_1=\sqrt{\frac{11}{8}},\quad \lambda_2=\lambda_3=0.
$$

Therefore, the global minimum is
$$
\boxed{f_{\min}=-\sqrt{\frac{11}{2}}}
$$
attained at the point above.

----

## Solution 6

### 1. $f(x) = \|x\|_\infty = \max_i |x_i|$

For any $x,y \in \mathbb{R}^n$ and $\theta \in [0,1]$,
$$
\|\theta x + (1-\theta)y\|_\infty
= \max_i |\theta x_i + (1-\theta)y_i|
\le \max_i \big(\theta |x_i| + (1-\theta)|y_i|\big)
\le \theta \|x\|_\infty + (1-\theta)\|y\|_\infty.
$$

Hence, $f(x)$ satisfies the convexity definition.

**Conclusion:** $f(x)$ is convex.

### 2. $f(x) = e^{2x} - 4x,\; x \in \mathbb{R}$

Compute derivatives:
$$
f'(x) = 2e^{2x} - 4, \quad
f''(x) = 4e^{2x}.
$$

Since $e^{2x} > 0$ for all $x$,
$$
f''(x) = 4e^{2x} > 0 \quad \forall x.
$$

**Conclusion:** $f(x)$ is convex by the second-order condition.

### 3. $f(x) = x \log x,\; x > 0$

Compute derivatives:
$$
f'(x) = \log x + 1, \quad
f''(x) = \frac{1}{x}.
$$

For $x > 0$,
$$
f''(x) = \frac{1}{x} > 0.
$$

**Conclusion:** $f(x)$ is convex on $x > 0$.

----

## Solution 7

Given Linear Programming problem is to Maximize  
$$
Z = 5x_1 + 4x_2
$$

Subject to  
$$
\begin{aligned}
6x_1 + 4x_2 &\le 24 \\
x_1 + 2x_2 &\le 6 \\
-x_1 + x_2 &\le 1 \\
x_2 &\le 2 \\
x_1, x_2 &\ge 0
\end{aligned}
$$

Introducing slack variables $s_1, s_2, s_3, s_4 \ge 0$:

$$
\begin{aligned}
6x_1 + 4x_2 + s_1 &= 24 \\
x_1 + 2x_2 + s_2 &= 6 \\
-x_1 + x_2 + s_3 &= 1 \\
x_2 + s_4 &= 2
\end{aligned}
$$

Initial Simplex Tableau is:

| Basis | $x_1$ | $x_2$ | $s_1$ | $s_2$ | $s_3$ | $s_4$ | RHS |
|------|------|------|------|------|------|------|-----|
| $s_1$ | 6 | 4 | 1 | 0 | 0 | 0 | 24 |
| $s_2$ | 1 | 2 | 0 | 1 | 0 | 0 | 6 |
| $s_3$ | -1 | 1 | 0 | 0 | 1 | 0 | 1 |
| $s_4$ | 0 | 1 | 0 | 0 | 0 | 1 | 2 |
| $Z$ | -5 | -4 | 0 | 0 | 0 | 0 | 0 |

In these iterations:

- Entering variable: $x_1$ (most negative in $Z$-row)
- Leaving variable: $s_1$
- Next entering variable: $x_2$
- Leaving variable: $s_2$

After performing simplex iterations, no negative coefficients remain in the $Z$-row.

$$
x_1 = 2,\quad x_2 = 2
$$

Objective value:
$$
Z_{\max} = 5(2) + 4(2) = 18
$$

So the optimal solution is $x_1 = 2,\; x_2 = 2$ with maximum value $Z_{\max} = 18$.

## Solution 8

1. Given Linear Programming problem is to Maximize
$$
Z = 50x_1 + 30x_2
$$

Subject to
$$
500x_1 + 300x_2 \le 20000 \quad \text{(Flour)}
$$
$$
200x_1 + 150x_2 \le 10000 \quad \text{(Sugar)}
$$
$$
100x_1 + 50x_2 \le 5000 \quad \text{(Butter)}
$$
$$
x_1 \ge 0,\; x_2 \ge 0
$$

2. The feasible region is the common area satisfying all constraints in the first quadrant.  
Corner points are:
- $(0,0)$
- $(40,0)$
- $(0,66.67)$
- Intersection of Flour and Sugar constraints

Solve intersection:
$$
500x_1 + 300x_2 = 20000
$$
$$
200x_1 + 150x_2 = 10000
$$

Solution:
$$
x_1 = 20,\quad x_2 = 33.33
$$

3. Optimal Production Plan
At $(x_1, x_2) = (20,\; 33.33)$,

$$
Z_{\max} = 50(20) + 30(33.33) = Rs.\,2000
$$
 
4. To maximize profit, the bakery should produce **20 cakes** and **approximately 33 cookies**, earning a maximum profit of **Rs. 2000**.

------

## Solution 9

1.
**Constraint analysis**

The inequality $(x-2)(x-4)\le 0$ holds between the roots $2 \le x \le 4$.
So the **feasible set** is $\mathcal{F} = [2,4]$.

**Objective values on the feasible set**

The objective $f(x)=x^2+1$ is increasing for $x>0$.

Evaluate endpoints: $f(2)=5,\quad f(4)=17$.

So Optimal solution is $x^\star = 2$ and Optimal value is $f^\star = 5$.

2. 
- **Objective**: $f(x)=x^2+1$ is an upward-opening parabola.
- **Feasible set**: Interval $[2,4]$ on the $x$-axis.
- **Optimal point**: Point $(2,5)$ on the parabola.
- **Lagrangian**: $L(x,\lambda)=x^2+1+\lambda (x-2)(x-4),\quad \lambda\ge 0$

For increasing $\lambda>0$, the quadratic term changes curvature, and the minimum of $L(x,\lambda)$ shifts left of the feasible region.

3. Dual function $g(\lambda)$

$$
g(\lambda)=\inf_x L(x,\lambda) \\
\implies L(x,\lambda)=(1+\lambda)x^2-6\lambda x+(8\lambda+1)
$$

Minimize over $x$:
$$
x(\lambda)=\frac{3\lambda}{1+\lambda}
$$

Substitute back:
$$
g(\lambda)=1+8\lambda-\frac{9\lambda^2}{1+\lambda},\quad \lambda\ge 0
$$

**Sketch**
- $g(\lambda)$ is concave and increases initially, then saturates.

4. Dual problem and concavity

**Dual problem** $\max_{\lambda\ge 0} \; g(\lambda)$

**Verification**
- $g(\lambda)$ is the infimum of affine functions in $\lambda$.
- Therefore, $g(\lambda)$ is concave.
- Hence, the dual is a **concave maximization problem**.

5. Dual optimal value and solution

**Evaluation**

At $\lambda=0$, $g(0)=1$.

As $\lambda\to\infty$, $g(\lambda)\to 5$.

**Conclusion**
- Dual optimal value: $g^\star = 5$
- Dual optimal solution: $\lambda^\star \to \infty$

Therefore we get:
- Primal optimal value: $5$
- Dual optimal value: $5$
- Strong duality holds.
- Primal optimum at $x^\star=2$