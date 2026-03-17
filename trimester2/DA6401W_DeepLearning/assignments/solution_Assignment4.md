---
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

# DA6401W - Assignment 4

Submitted by: Sohang Chopra &lt;DA25M622&gt;

## Problem 1: Theoretical Question 

Consider training a deep neural network using stochastic gradient
descent (SGD) on a non-convex loss surface. Curriculum learning is implemented by first
training on "easy" examples and gradually introducing harder examples.

Which of the following statements is **most theoretically accurate** ?

1. Curriculum learning guarantees convergence to a flatter minimum.
2. Curriculum learning modifies early gradient statistics, thereby influencing the optimization trajectory in parameter space.
3. Curriculum learning changes the global minimum of the objective function.
4. Curriculum learning eliminates the effect of random initialization.s

### Solution 1

TODO: theory


## Problem 5: (Conceptual MCQ) Nesterov Accelerated Gradient

Momentum methods are commonly used to accelerate gradient-based optimization in deep
learning. Nesterov Accelerated Gradient (NAG) modifies the classical momentum method.

Which of the following statements best describes the key idea behind **Nesterov momentum** ?

1. The gradient is computed at the current parameter location without using momentum.
2. The gradient is computed after performing a _look-ahead_ step using the momentum
term.
3. The learning rate is automatically adjusted based on the magnitude of gradients.
4. The optimization step ignores past gradients completely.
5. The algorithm guarantees convergence to the global optimum for non-convex problems.

### Solution 5

TODO: theory


## Problem 7

Consider a fully connected neural network trained for a classification task. During training,
**dropout** is applied to a hidden layer with dropout probability _p_ .


1. Explain how dropout helps prevent overfitting in neural networks. In your answer, discuss
why dropout can be interpreted as implicitly training an ensemble of subnetworks.
2. During training, neurons are randomly dropped with probability _p_ . However, during
inference (testing), dropout is not applied
    * Explain how the network output is adjusted during inference to account for dropout used during training.
    * Why is this scaling necessary?
3. Suppose the output of a neuron before dropout is $h$ . 
Let the dropout mask be $m \sim Bernoulli(1-p)$. The output after dropout during training is $\bar{h} = m h$.
Compute $E[\bar{h}]$.
4. Dropout is often applied to fully connected layers but less frequently to convolutional
layers in modern architectures. Provide two reasons why dropout may be less effective
in convolutional layers.

### Solution 7

TODO: theory


## Problem 10: (Numerical Question) Label Smoothing

A classification task has _K_ = 4 classes. Label smoothing with parameter $\epsilon = 0.1$ is applied.
If the true class is class 2, compute the smoothed target distribution.

### Solution 10

TODO: numerical


## Problem 11: Numerical: One Iteration of Steepest Descent

Consider the quadratic objective function

$$f(w_1, w_2) = 2 w_1^2 + w_1 w_2 + w_2^2$$

The steepest descent update rule is

$$w_{t+1} = w_t - \eta \nabla f(w_t)$$

Given:

$$w_0 = \begin{pmatrix} 2 \\ -1 \end{pmatrix}, \quad \eta = 0.1$$

Compute the updated parameter vector $w_1$ after one iteration of steepest descent.

### Solution 10

TODO: numerical


## Problem 13: Numerical: One Iteration of ADMM for Lasso Problem

*Note (ADMM intuition):* The Alternating Direction Method of Multipliers (ADMM) is an
optimization algorithm used to solve problems where the objective function can be split into
multiple components with simple structure.

In ADMM, the constrained problem

$$\min_{w,z} f(w) + g(z), \text{subject to } w = z$$

is solved by performing *alternating updates*:

- A quadratic minimization step for $w$
- A proximal (soft-thresholding) step for $z$
- A dual variable update enforcing consistency between $w$ and $z$

For the Lasso problem, the $z$-update corresponds to applying the **soft-thresholding operator**, which promotes sparsity in the solution.

Consider the Lasso optimization problem

$$min_w \frac{1}{2} \|A w - b\|_2^2 + \lambda \|z\|_1, \quad \text{subject to } w = z$$

Using the ADMM formulation, the augmented Lagrangian is

$$\mathcal{L}_p(w,z,u) = \frac{1}{2} \|A w - b\|_2^2 + \lambda \|z\|_1  + \frac{\rho}{2} \|w - z + u\|_2^2$$

where $u$ is the scaled dual variable.

Given:

$$A = \begin{bmatrix} 1 & 0 \\ 0 & 2 \end{bmatrix}, \quad b = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$$

Initial Values:

$$w_0 = z_0 = u_0 = \begin{pmatrix} 0 \\ 0 \end{pmatrix}$$

Parameters:

$$\lambda = 0.5, \quad \rho = 1$$

Compute:

1. The updated $w_1$
2. The updated $z_1$ using the soft-thresholding operator
3. The updated dual variable $u_1$

### Solution 13

TODO: numerical