# DA6401W: Introduction to Deep Learning

Professor email: &lt;lnt@dsai.iitm.ac.in&gt;

Head TAs :
* Manoj Kumar &lt;da24s018@smail.iitm.ac.in&gt;
* Yuvaram Singh &lt;da24s015@smail.iitm.ac.in&gt;

In this course we'll only do supervised learning, not unsupervised learning.
All of Deep Learning, especially supervised learning, is basically curve fitting.

While creating a new architecture, activation etc. we have to make sure everything is differentiable, otherwise Deep Learning optimization will not work.

## Linear Algebra & Probability Revise (lecture 1); WIP check if anything missed from lecture slide

### Linear Algebra Revision

#### Spaces and Norms

Vector Spaces $\mathbb{V}: \forall \mathbf{x}, \mathbf{y} \in \mathbb{V}, a \mathbf{x} + b \mathbf{y} \in \mathbb{V}$ 
can be Binary/Boolean, Complex $C(N)$ but we use Real spaces $R(N)$ mostly.

Vector Subpsaces are closed under vector addition, scalar multiplication and must contain zero vector.

In a neural network, neurons create projections of inputs from vector space onto a subspace.

If Inner Product $\mathbf{x}^T \mathbf{y}$ is:
* $> 0$, then vector components are along same direction
* $< 0$, then vector components are along opposite direction
* $== 0$, then **orthogonal vectors**.

If basis vectors $\mathbf{b_1} ... \mathbf{b_n}$ are orthonormal, 
then projection of vector $\mathbf{v}$ has components simply inner products with bases:
$(\mathbf{v}^T \mathbf{b_1}, ... \mathbf{v}^T \mathbf{b_n})$

p-norm $p \ge 1$ of vector $(\sum v_i^p)^{\frac{1}{p}}$ (it's defined for real spaces, NOT defined for binary spaces):
* 0-norm (counting norm) - just counts non-zero entries. It's very sparsity-promoting (ie we're trying to make ). But rarely used in practice as it's not differentiable.
  Often L0 norm is used in theory, but in practice we replace it with L1 norm.
* 1-norm $\sum v_i$ is used in popular **L1 Regularization** (minimize L1 norm to reduce overfitting by promoting sparsity of matrix).
* 2-norm (Euclidean distance from origin) is used in **L2 Regularization** (minimize L2 norm - it's used less than L1).
* Elastic loss (Mixed Norm) -- uses multiple L1,L2 norms etc. - but this is complex so not used often.

One nice property of norms as loss for optimization is that they are convex, so guaranteed to have some minima.

**We usually use Cross-Entropy loss (or binary cross entropy), but may additionally use L1,L2 norms to promote sparsity so there are less weights**.

#### Linear Hyper-plane

It's an $n-1$ dimensional subspace of $\mathbf{R}^n$.

Plane divides space into 2 parts, so for linearly seperable data it can be used for **binary classification**.
This is in fact what the last/output layer of a neural network does in case of binary classification (sigmoid activation)
- i.e. a single sigmoid neuron creates a plane.
The job of the remaining hidden layers is to transform data into linearly seperable data for last layer to then classify.

NOTE: for regression, no activation function is used on final Linear layer as we want continous output only.

Distance of a vector $x$ from hyperplane = $\frac{x^T v}{\|v\|}$ where $v$ is normal vector of hyperplane.

#### Singular Value Decomposition (SVD)

### Probability

TODO - Cross Entropy (KL Divergence + Entropy of a random variable PMF P), Relative Entropy (distance between 2 probability distributions, using their Probability Mass Functions), KL Divergence etc.

PMF of distribution P = TODO: formula

TODO

## WIP Lecture 2 - slides not uploaded yet

### Probability Revision

Cross Entropy loss - use in classification (cross entropy and relative entropy are similar, so you're automatically using relative entropy as well here)

Minimizing Cross Entropy & KL Divergence gives same minima; we prefer cross entropy as it's easier to differentiate.

All of Deep Learning theory uses Bayesian framework. 
But if prior (training) distribution is incorrect (ie posterior distribution of test/inference data is different), then poor results.

Information Theory definitions:
* Entropy is original bits of distribution (least bits req to encode)
* Relative Entropy is how many bits (ie log 2 of information) you need to encode distribution
* Cross Entropy is how many bits used if you wrongly assume distribution P is actually distribution Q + entropy of P

### Linear Algebra Revision

Taylor series, Gradient & Hessian

Taylor: polynomial expansion of function $f$, centered at point $a$, at a random point $x$ near $a$.

$$T(x) = f(a) + (x-a)^T \nabla f(a) + \frac{1}{2!} (x-a)^T \nabla^2 f(a) (x-a) + ...$$

Gradient vector (most practical optimization methods like Adam, RMSProp use upto first order derivative Taylor only)

$$\nabla f(x) = \begin{pmatrix} \frac{\partial f}{\partial x_1} (p) \\ \frac{\partial f}{\partial x_2} (p) \\ \vdots \\ \frac{\partial f}{\partial x_n} (p) \end{pmatrix}$$

Hessian matrix (Newton, LPF, GS optimization etc. use upto second-derivative Taylor)

$$H_f = \begin{pmatrix} 
\frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_1 \partial x_n} \\
\frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} & \cdots & \frac{\partial^2 f}{\partial x_2 \partial x_n} \\
\vdots                                         & \ddots                                       & \vdots \\
\frac{\partial^2 f}{\partial x_n \partial x_1} & \frac{\partial^2 f}{\partial x_n \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_n^2} \\
\end{pmatrix}$$

### Supervised vs Unsupervised learning

TODO: copy table from slides (properties)

Loss function types: Cross entropy (or binary cross entropy) loss, optionally with L1 / L2 / mixed norms

### Classification

BINARY CLASSIFICATION:

Calculate Posterior probabilities $P(y=0 | x)$, $P(y=1 | x)$, then $a$ is log posterior ratios.

By Bayes and conditional probability:

$$P(y=1 | x) = \frac{P(x | y=1) P(y=1)}{P(x | y=0) P(y=0) + P(x | y=1) P(y=1)}$$

For binary classification, this simplifies to **Sigmoid** (using log posteriors $a_0$, $a_1$ for y=0,1):

$$P(y=1 | x) = \sigma(a_1) = \frac{1}{1 + e^{-a}}$$

Finally after sigmoid gives us the probabilities, just choose class with higher probability.

Sigmoid etc. activations are useful to convert non linearly seperable data into linearly seperable data.

**Sigmoid / Softmax are basically single layer classifiers**. It converts **logits** (distances) to probabilities.

TODO: MULTI-CLASS REGRESSION:

TODO: Logistic Regression (name has regression but actually final output is classification)

### Regression

Linear Regression

TODO: Multi-Class Regression

TODO: Ridge Regression

TODO
