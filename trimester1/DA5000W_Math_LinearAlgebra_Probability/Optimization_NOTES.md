# Optimization

On 13 Nov 2025, Prof Ramkrishna started covering Optimization

TODO: syllabus, notes on topics

topics covered (non-exhaustive): *Unconstrained Optimization*: basic plots (lines on 2d plane, shading), gradients, first & second derivatives, minima/maxima, **Jacobian & Hessian matrices**,
  **Numerical/approx optimization** (when exact methods can't be used): **Gradient Descent**

*Positive definite*, *Positive semi-definite* etc. : a Matrix is > 0 if all its eigenvalues are > 0, Matrix < 0 if all its eigenvalues are < 0 - others (mix) I guess are non-classifiable?

LATER **Stochastic Gradient Descent**, *Constrained Optimization*, Linear Programming (intro to **simplex method**), **Quadratic Optimization**

Exact topics shared in first Optimization lecture (shared by a colleague):

1. General introduction to optimization problems.
2. Arranging a school trip as an example of an optimization problem.
3. Mathematical formulation of the optimization problem.
4. Constraints related to the number of buses and drivers.
5. Graphical techniques for solving optimization problems.
6. Linear programming and its components.
7. Unconstrained optimization problems.
8. First and second order conditions for optimization.
9. Local vs. global minima.
10. Convex functions and their properties.
11. Gradient descent as a method for optimization.
12. Numerical methods for optimization.
13. Discussion on initial guesses and learning rates in optimization algorithms.
14. Overview of constrained optimization and future topics to be covered, including KKT conditions and linear programming with the simplex method.

## WIP 6. CONSTRAINED OPTIMIZATION
* f(x) = func to minimize or maximize
* ci(x) = 0 --- equality constraints
* cj(x) >= 0 -- inequality constraints

### Single Equality problem:
only one $c(x) = 0$

at minimum $x^*$, $\delta f(x^*) = \lambda \delta c(x^*)$ that is, constraint normal is parallel to gradient of function being optimized
This can be derived from  first order gradient of **Lagrangian** (unconstrained optimization).

Lagrangian $L(\mathbf{x}, \lambda) = f(x) - \lambda c(x)$ where $\lambda$ is *Lagrangian multiplier*.
First order gradients, one wrt x, one wrt $\lambda$ :
* $\delta_x L = \delta_x f(x) - \lambda \delta c(x) = 0$
* $delta_{\} L = - c(x) = 0$
