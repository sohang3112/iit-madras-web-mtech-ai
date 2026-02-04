# DA6401W: Introduction to Deep Learning

Professor email: &lt;lnt@dsai.iitm.ac.in&gt;

Head TAs :
* Manoj Kumar &lt;da24s018@smail.iitm.ac.in&gt;
* Yuvaram Singh &lt;da24s015@smail.iitm.ac.in&gt;

In this course we'll only do supervised learning, not unsupervised learning.
All of Deep Learning, especially supervised learning, is basically curve fitting.

While creating a new architecture, activation etc. we have to make sure everything is differentiable, otherwise Deep Learning optimization will not work.

## Linear Algebra & Probability Revise (lecture 1 slides have material of lecture 2, 3, 4 as well)

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

**Loss functions measure some kind of distance.**

#### Linear Hyper-plane

It's an $n-1$ dimensional subspace of $\mathbf{R}^n$.

Plane divides space into 2 parts, so for linearly seperable data it can be used for **binary classification**.
This is in fact what the last/output layer of a neural network does in case of binary classification (sigmoid activation)
- i.e. a single sigmoid neuron creates a plane.
The job of the remaining hidden layers is to transform data into linearly seperable data for last layer to then classify.

NOTE: for regression, no activation function is used on final Linear layer as we want continous output only.

Distance of a vector $x$ from hyperplane = $\frac{x^T v}{\|v\|}$ where $v$ is normal vector of hyperplane.

A simple example of a problem that's NOT linearly seperable is XOR. So a single neural layer cannot learn it, multiple are required.

#### Singular Value Decomposition (SVD) of Matrix

$$M = U \Sigma V^T$$

where:
* $U$, $V$ are **orthogonal matrices** (i.e. $I = A A^T = B B^T$, i.e. both matrices' row & column vectors form orthonormal bases)
    * **Left Singular Vectors** are columns of $U$ - they come from eigen vectors of $M^T M$
    * **Right Singular Vectors** are columns of $V$ - they come from eigen vectors of $M M^T$.
* $\Sigma$ is a **Positive Semi-Definite Diagonal matrix** -- its non-zero diagonal entries are called **Singular Values**.
  These *diagonal values are positive and in ascending order*: $\sigma_1 \le \sigma_2 \le .. \sigma_r$ where $r$ is rank of $\Sigma$ - remaining are 0 values.

**Pseudo-Inverse** of $M$ is $V \Sigma^{-1} U^T$

For all singular values $\sigma_i$ and corresponding left singular vectors $u_i$, right singular vectors $v_i$:

$$M v_i = \sigma_i u_i$$

#### Matrix Norm

$$\|A\|_p = \sup \limits_{x \ne 0} \frac{ \|A x\|_p }{ \|x\|_p } , \quad \|A\|_2 = \sigma_{max}(A)$$

Here $\sup$ is basically equivalent to $\max$. **Matrix 2-norm is its largest singular value** (singular values calculated in SVD)

#### Taylor series, Gradient & Hessian

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


### Probability

PMF of distribution P = TODO: formula

**Probability Space**:
* Sample Space
* $F$ Event Space - contains all possible subsets of Sample Space
* $P$ **measure** for all elements of $F$ - eg. proportion of occurance of any $u \in F$

Mapping $SampleSpace \rightarrow \mathbb{R}$ is a **Random Variable**.

#### Bayes Formula

$$
P(X|Y) = \frac{ P(Y|X) P(X)}{ P(Y) } \\
\implies P(X|Y) \propto P(Y|X) P(X) \\
\implies Posterior \propto Prior \times Likelihood
$$

Here:
* $P(X)$ is **prior** (statistics known before making any observations)
* $P(X|Y)$ is **posterior** (updated probability after finding out outcome of $Y$)
* $P(Y=y | X)$ is **likelihood** (calculated based on outcome of $Y$). **It's NOT a valid PMF / PDF** because probability space itself changes for each value of $X$.

All of Deep Learning theory uses Bayesian framework. 
But if prior (training) distribution is incorrect (ie posterior distribution of test/inference data is different), then poor results.

**Sum of posteriors is 1 as sample space $Y$ is same in all**: eg. for binary classification, $P(X=0 | Y) + P(X=1 | Y) = 1$

#### WIP Entropy (Cross, Relative, KL Divergence)

Cross Entropy loss - use in classification (cross entropy and relative entropy are similar, so you're automatically using relative entropy as well here)

Minimizing Cross Entropy & KL Divergence gives same minima; we prefer cross entropy as it's easier to differentiate.

Information Theory definitions:
* Entropy is original bits of distribution (least bits req to encode)
* Relative Entropy is how many bits (ie log 2 of information) you need to encode distribution
* Cross Entropy is how many bits used if you wrongly assume distribution P is actually distribution Q + entropy of P

For true probability distribution $P$ and assumed probability distribution $Q$ (NOTE: **KL Divergence is also called Relative Entropy**):

$$
Entropy = H(P) = - \sum_{i=1}^{classes} p(x_i) \ln(p(x_i)) \\
CrossEntropy = H(P,Q) = - \sum_{i=1}^{classes} p(x_i) \ln(q(x_i)) \\
KLDivergence = D_{KL}(P || Q) = H(P,Q) - H(P) = \sum_{i=1}^{classes} p(x_i) \ln(\frac{p(x_i)}{q(x_i)})
$$

### Machine Learning

#### Supervised vs Unsupervised learning

Supervised learning            | Unsupervised
------------------------------ | ---------------
Labelled data                  | Unlabelled data
Training + Inference           | No Train, only Inference
eg. Classification, Regression | eg. PCA, Clustering, Pattern Finding

#### Loss functions

Loss functions quantify error obtained during parameter optimization.

$$\argmin Loss \{ f(x,\theta) - label(x) \}$$

* L0  norm (sparsity -promoting), 0 -1 loss:  $\|y  – y true \|_0$
* L1  norm, absolute error: $\|y  – y true \|_1$
* Squared L2  norm, Euclidean distance: $\|y  – y true \|^2_2$
* Mixed norms: linear combination of different p-norms $p ge 1$ – convex losses
* Cross entropy, F-score, etc.

#### Classification

* Sigmoid etc. activations are useful to convert non linearly seperable data into linearly seperable data.
* **Sigmoid / Softmax are basically single layer classifiers**. It converts **logits** (distances) to probabilities.

##### Binary Classification

Calculate Posterior probabilities $P(y=0 | x)$, $P(y=1 | x)$, then $a$ is log posterior ratios.

By Bayes and conditional probability:

$$P(y=1 | x) = \frac{P(x | y=1) P(y=1)}{P(x | y=0) P(y=0) + P(x | y=1) P(y=1)}$$

For binary classification, this simplifies to **Sigmoid** (using log posteriors $a_0$, $a_1$ for y=0,1):

$$P(y=1 | x) = \sigma(a_1) = \frac{1}{1 + e^{-a}}$$

Finally after sigmoid gives us the probabilities, just choose class with higher probability.

##### Multi-Class Classification

$$P(y=C_k | x) = \frac{P(x | y=C_k) P(y=C_k)}{\sum_j P(x | y=C_j) P(y=C_j)}$$

This simplifies to **Softmax** function (using log posterior vector $a$ having elements $a_k = ln P(x | y=C_k) P(y=C_k)$):

$$P(y=C_k | x) = \sigma_k(a) = \frac{e^{\alpha_k}}{\sum_j e^{\alpha_j}}$$

TODO: Logistic Regression (name has regression but actually final output is classification)

#### Regression

* $y_i = f(x_i) + \epsilon$ where $\{x_i\}, \{y_i\}$ are training inputs, labels, $\epsilon$ is error. Find $f$.
* Parameterized $f(x) = g(W,x)$ where $W$ is weights matrix ; Linear Regression: $g(W,x) = W^T x$

Linear Regression uses **linear activation**, i.e., just identity (no change)

TODO: Polynomial Regression uses Taylor's Expansion

TODO: Multi-Class Regression

TODO: Ridge Regression

TODO


#### Training & Generalization (Test) errors - Underfitting and Overfitting

![Training & Generalization error](images/train_generalize_error.png)

Assuming uniform, balanced data

Underfitting -- train error is high (too less model params), so try increasing number of model parameters or number of layers etc.

Overfitting -- low train error BUT high test error (too many model params) => regularization techniques to solve like L1, L2, Dropout etc.

NOTE: test error is also called **generalization error**.

Finding *optimal number of model parameters* is hard.

**VC Dimension** $|TrainError - TestError| \le \sqrt{O(d_{VC} \frac{log n}{n})}$ -- this is **probabilistic equation NOT deterministic** 
(it's likely to hold not guaranteed) -- TODO: CHECK what's this vc dimension (he said it's used mostly in theoritical ML not practical?)

Examples of underfit, overfit and bestfit:

![Examples: fit](images/examples_fit.png)


Some **counter-intuitive facts**:

* Sometimes more training data can lead to worse performance! TODO: examples of this?
* Double Decay

##### Double Decay

When you overfit, validation error increases. 
But after that point if you keep increasing parameters massively (millions / billions of params), then after a point accuracy increases - **Double Descent**!
LLMs operate in this *over-parameterized* zone.
But even after that when you keep increasing parameters a lot (millions / billions of params!), then validation error actually reduces!
This is **Over-parameterized region** (LLMs operate here).
It's because as no. of parameters (depth) increases, overfitting is smoothened (smoother interpolation and extrapolation).
So **Overfitting can be overcome with deeper networks**. *Interpolation Threshold* for this is when *no. of parameters = no. of data points*.

![Double Descent](images/double_descent.png)

#### Validation (split data, Cross-Validation)

In training only not validation, we maximize posterior probability. 

Split data: Train-Validation typically 80:20 ; also Test data

Cross-Validation: multiple (train,val) splits & trains, then average all the models' weights/params -- accuracy is worst accuracy from all splits.
   (NOTE: seperate test data is still recommended to be used in Cross-Validation)
    * No hard rule for number of folds in k-fold cross validation - chosen subjectively.


#### Bias-Variance tradeoff

Bias: high if model is too simple (underfitting), low if model has sufficient complexity according to data.

Variance: sensitivity from small fluctuations in training set. High variance means overfitting.

![Bias-Variance tradeoff](images/bias_variance_tradeoff.png)

When we train model on different training data sampled from same underlying data (eg. Cross Validation),
and then do inference with all the trained models on fixed validation point (TODO: on only one point, or fixed validation data):

Bias, Variance values are different at different chosen validation points.

$$
Bias(x) = E[y_{pred}] - y_{true}, \quad \text{where } y_{true} = f(x) \\
Variance(x) = Var(y_{pred}) \\
$$

Bias reduce => Variance increase

**Capacity Point** is where (bias, variance) both are overall minimized (ie any further reduction in one will only come at expense of increase in other).

$Error = E[(y_{true} - y_{pred})^2] = Bias^2 + Var(y_{pred}) + IrreducibleError)$

For finite datasets & specific model training runs, loss can be reduced to 0.
But for large datasets & considering statistical loss (ie in cross-validation, average loss of all trained models) - 
that can't go to 0, but can only be reduced till the Irreducible Loss.

#### No Free Lunch Theorem

No model can have best possible performance on all possible unseen data (since unseen data can have unique statistics).
Tradeoff between **Robustness** and **Accuracy**.

**Regularization**: Use any known statistical behaviour of entire data to optimize model (in addition to training data).

#### Maximum Likelihood Estimation (MLE) vs Maximum A Posteriori (MAP - Bayesian Inference)

Infer bias $p$ of a coin from observations of its toss $X_i ~ Bernoulli(p)$.

**Maximum Likelihood Estimation (MLE - Classical / no prior bias)**: 
* Probability of head: $\hat{p} = \frac{\sum y_i}{N}$ where $y_i \in \{0,1\}$ are experiment outputs.
* On taking many different sample observations of same coin: $Bias(\hat{p}) = 0 \quad Variance(\hat{p}) = \frac{p (1-p)}{N}$

**Maximum A Posteriori (MAP - Bayesian / prior bias)**:
* We maximize Posterior probability (ie updated probab after knowing about previous coin tosses): $\argmax\limits_{p} P(\text{data} | p) P(p)$
    * TODO QUESTION: in slide this is shown to solve to $\frac{\sum y_i}{N+1}$ -- here how did the $N+1$ come in denominator??
* Unlike MLE, here Bias is NOT 0 (since prior knowledge is used).

MLE vs MAP (Bayesian) plot (MSE error vs N number of observations) with different $w$ (weight given to prior data -- give more weight if prior is more reliable).
We can see Bayesian line is lower, i.e., for any N here, MSE is lower for Bayesian:

![MLE vs MAP](images/bayesian_inference.png)

An example of a prior is: suppose we only collect some kind of data in summer. 
So summer = prior bias; in summer model can perform better than a generic model ; but badly not in summer.

#### Grokking

* Generalization of *over-parameterized models* by **over training** (less over training needed for smaller dataset).
* **Weight Decay** helps (additional term in loss function that pushes weights closer to 0)

![Grokking](images/grokking.png)

Grokking was discovered in 2023 by OpenAI when they accidentally left a model training even after loss appeared to saturate (so straight line loss).
But after a long time (a week), the loss suddenly dropped a lot from previous straight line loss!
It's because loss wasn't actually straight line, it was just decreasing very very slowly so it wasn't noticeable.
Here loss function jumped from one local minima to far-away better local minima.

**Grokking vs Double Descent**: 
* In Double Descent no. of model parameters are increased, but in grokking no. of parameters is same - just training epochs increases.
* Grokking depends on loss function used, Double Descent doesn't.

#### No Free Lunch Theorem

It's *applicable only to parameterized supervised learning, but NOT online learning, reinforcement learning etc.*

**Inductive Bias**: bias learnt by model from traininig data (practically impossible to have 0 bias in data)

*Tradeoff between good Robustness (how much model can generalize, so less Variance) vs good Accuracy (so less Bias)*

So it's impossible to train one model which has best possible performance for any possible data.


## WIP Multilayer Perceptron (Lecture 5)

Single perceptron: $u(W^T x + b)$ (linear calculation with weights, then run non-linear activation)

* Any continous function can be approximated by a polynomial of sufficient degree.
* Deep Learning (neural network) is *Universal Function Approximator*.

width = no. of neurons in a layer, depth = no. of layers

Motivation to come up with Resnet model was to look at loss surface plot and try to design a loss with good loss surface.

ReLU activation doesn't work well with a single layer model (due to its sharp edges in plot).
But in multiple layers (ie hidden layers) it works very well. And computationally it's best as very simple (derivative is also very simple).

`sigmoid` is equivalent to `tanh` with some extra weights.

sigmoid derivative is 1/4 -> less than 1 creates problem in gradient descent (vanishing gradient). 
tanh is better (in hidden layers) - unlike sigmoid it can be negative, and has

## WIP Gradient Descent (Lecture 6)

* how to find roots of derivative of loss function ?
* Taylor approximations in higher dimensions:
    * Gradient Vector (linear approx at a point)
    * Hessian Matrix (curvature of function at a point)
* Loss $L(w + \epsilon) \approx L(w) + \nabla L(w)^T (w + \epsilon - w)$
    * For $L(w + \epsilon) - L(w) \le 0$, pick $\epsilon$ opposite to $\nabla L(w)$

* Update (using first order Taylor approx) in steepest direction (gradient of loss) $w_{n+1} = w_n - \eta \nabla L(w_n)$
    * $L(w_0) \ge L(w_1) \ge \cdots \ge L(w_n)$
* How to find gradient w.r.t all weights? - by using Backpropogation
* What is a good learning rate $\eta$ ?
* What is a good starting rate $w_0$ ?

In some situations second order Taylor approx is also used in update rule -- will be covered later.

### Backpropogation

* Compute $g = \nabla_{output} L$
TODO

* For input-label pair (x,y) and loss function C(.):

$$C(y, f^L) =$$

TODO


### Weights Initialization

DON'T initialize all weights to same value like 0 (else very bad performance). Init has to be random weights.

Control variance of randomness (U - Uniform, N - Normal distribution):

Technique  | Activations           | Distribution                                      | Remark
---------- | --------------------- | ------------------------------------------------- | -------------------
Xavier     | tanh, sigmoid         | $\mathcal{U}(\pm \sqrt{6 / (n_{l+1} + n_{l-1})})$ | NOT applicable for RELU because unlike tanh, sigmoid RELU doesn't have symmetric mean around 0
Kaiming He | RELU, Leaky RELU etc. | $\mathcal{N}(0, 2 / n_{l-1})$                     |
LeCun      | SELU                  | $\mathcal{U}(\pm \sqrt{3 / n_{l-1}})$             |

Random orthogonal matrix is used for any arbitary activation in libraries.

NOTE: in each both uniform and normal distributions with specific values can be used. What are listed here are best.


## WIP Forward pass, Back propogation, Autograd (Lecture 7) (slides not uploaded yet)

Autograd:
* automatically (dynamically) create model layers graph from function (pytorch looks at it line by line AT TRAIN & INFERENCE TIME -- NOT before hand from function AST)
    * so unlike static graphs in tensorflow (model layers defined & fixed at train & inference time), here model layers can change at runtime based on input in pytorch!!
      TODO: i think dynamic graphs are supported in tensorflow also - check.
      static graph (faster as avoids some computation), dynamic (slower) -- 
      NOTE: dynamic graph only advantage is if and for loops (ie at runtime on getting input different layers), otherwise use static graph only for faster
```python
def model(x):
    if x > 0:
        y = 1
    else:
        y = 0
    z = 2 * x
    for i in range(2):
        y = z*y + i
    return y
```
* auto called in back propogation `.backward()`
TODO

In forward pass (required first), no gradients are calculated, just graph is constructed.
Then in backpropogation, gradients of loss are calculated at each layer to finally get total.

TODO: Backpropogation gradient calculation autograd process

Backpropogation:
* Autograd computes gradients through backpropogation
    * Gradients *flow* from one node to another.
    * Recursion and matrix operations (eg. SVD) can have derivatives, according to research [Auto-Differentiating Linear Algebra (2019) by M. Seeger et al](https://arxiv.org/abs/1710.08717)
* **Vanishing** or **Exploding** gradient problems: gradients don't flow
TODO
