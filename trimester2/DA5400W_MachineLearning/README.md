# DA45400W : Foundations of Machine Learning

* Prof Nirav Pravinbhai Bhatt &lt;niravbhatt@smail.iitm.ac.in&gt;
* Course group email &lt;da5400w@code.iitm.ac.in&gt;

Machine Learning usually requires significant feature engineering, but Deep Learning often automatically transforms features.

## Lecture 1 - Optimization Revision (recording uploaded but slides not uploaded yet)

* Constrained vs Unconstrained (aka **Static**) optimization
* Linear, Quadratic, Non linear programming
* Integer optimization
* Direct vs Iterative solution
* **Arthur Samuel's pardigm/mechanism** to improve performance by tweaking weights/parameters.
* Gradient Descent

### Mathematical Optimization

* Linear function: $a f(x) + b f(y) = f(ax + by)$
    * **Linear vs Affine linear**: linear has only scaling $A x$, with transform it becomes Affine linear $A x + b$
* Convex function ($\lambda \in [0,1]$): $\lambda f(x_1) + (1 - \lambda) f(x_2) \le f(\lambda f(x_1) + (1 - \lambda) f(x_2))$

Optimize: select best elem (or multiple best elems) from available set of options.

Optimization problem with decision variables: maximize **cost/objective/loss function** $f(\mathbf{x})$ subject to constraints $g_i(\mathbf{x}) \le 0$ .

NOTE: constraints can be both linear and non-linear, sometimes linear are written seperately $A_i x \le b_i$.

### Optimization Types

* Linear programming: maximize $c^T x$ subject to $A_i x \le b_i$
* Quadratic
* Non-linear

### Constrained Optimization

#### KKT 

Has to be used for non-linear optimization.

Lagrangian $L(\mathbf{x}, \mathbf{\lambda}, \mathbf{\mu}) = f(\mathbf{x}) + \mathbf{\lambda}^T h(\mathbf{x}) + \mathbf{\mu}^T g(\mathbf{x})$

* First-order necessary condition: 
$$
\nabla L(\mathbf{x^*}, \mathbf{\lambda}) = 0 \
h_i(\mathbf{x^*}) = 0 \\
g_j(\mathbf{x^*}) = 0 \\
\lambda_i \ge 0, \mu_j \ge 0 \\
$$

Complementary condition $\mu_j g_j(\mathbf{x^*}) = 0$ (NOTE: $\mu_j$ is dependent on $x$, here we're talking only about values of $\mu_j$ at $x^*$)

* Second-order necessary condition: TODO

**LICQ**: Linearly Independent (TODO: rem full form)

### Unconstrained Optimization

#### Gradient Descent

* If learning rate is too big, oscillation diverges
* If learning rate is too low, it takes a long time to converge.

Learning Rate should be (determine these by checking loss values):
* Near local solution: proceed quickly with small learning rate
* Far from local solution: proceed quickly with large learning rate

Types of Gradient Descent (here L is loss) - tradeoff in convergence vs computation (speed, memory):
* Batch GD $w_{i+1} = w_i - \eta \nabla L(w)$ -- smoother convergence, but loads a lot of data into memory so slower
* Stochastic GD (online/streaming data) (different update rule) -- uses less (only one data at a point), faster
* Mini-batch GD: hybrid of batch and SGD -- (NOTE: for convergence Batch is best if can fit data into memory. There can be some extreme data in a mini-batch which affects strongly, but would affect batch GD less due to averaging out with more data)


## Lecture 2