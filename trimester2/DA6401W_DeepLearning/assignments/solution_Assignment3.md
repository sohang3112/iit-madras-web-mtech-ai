---
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

# DA6401W - Assignment 3

Submitted by: Sohang Chopra &lt;DA25M622&gt;


## Problem 2: Gradient Accumulation and Memory Constraints in Deep Learning

Training modern neural networks often requires large batch sizes for stable gradients and faster convergence.
However, GPU memory limits often make large batches infeasible. In this problem, we will
analyze optimizer memory usage and derive why _gradient accumulation_ is used in frameworks
such as PyTorch.

**Assume:**

- A neural network with $P$ parameters
- Each parameter stored in 32-bit floating point (4 bytes)
- A batch size of $B$
- Gradient accumulation steps or number of mini-batches $K$ .

**Memory Footprint of Optimizers**

Consider the memory required to store parameters, gradients, and optimizer states.

1. For **Stochastic Gradient Descent (SGD)** without momentum, determine the total memory required for storing parameters and gradients.
2. For **SGD with Momentum**, the optimizer additionally stores a momentum vector of the same size as the parameters. Compute the total memory requirement.
3. For the **Adam optimizer**, two additional vectors $m_t$ and $v_t$ are stored for each parameter. Compute the total optimizer memory footprint.
4. Suppose $P = 10^9$ parameters. Compute the memory required (in GB) for each of the above optimizers.

**Batch Size and Activation Memory**

During training, memory is also required to store intermediate activations for backpropagation.
Assume the activation memory per sample is $A$ bytes.

1. Express the total activation memory required for batch size $B$ .
2. Suppose the GPU memory limit is $M$ bytes. Write an inequality involving $B$, $A$, and optimizer memory that must hold for training to fit into memory.
3. Explain why increasing batch size $B$ may become infeasible for very large models.

**Convergence vs Batch Size**

Empirical studies suggest that very small batch sizes produce noisy gradient estimates and
slow convergence.

1. Suppose we desire an effective batch size $B_{large}$, but due to memory limits we can only fit a mini-batch of size $b$ where $b < B_{large}$.
2. Propose a strategy that allows us to simulate a larger batch using multiple smaller mini-batches without increasing memory usage.
3. Let $K$ denote the number of such mini-batches processed before updating the parameters. Express the relationship between $B_{large}$, $b$ and $K$.

**Equivalence of Gradient Accumulation and Large Batch Updates**

Let the loss over a batch be defined as the average loss:

$$L(\theta) = \frac{1}{B} \sum_{i=1}^B l(x_i, \theta)$$

where $l(x_i, \theta)$ is the loss for sample $i$.

Assume we divide the batch into $K$ mini-batches each of size $b = B / K$ .

1. Write the gradient of the full batch loss $\nabla_\theta L(\theta)$.
2. Let $g_k$ be the gradient computed from mini-batch $k$ :

$$g_k = \frac{1}{b} \sum_{i \in B_k} l(x_i, \theta)$$

Show that:

$$L(x_i, \theta) = \frac{1}{K} \sum_{k=1}^K g_k$$

3. Explain why gradient accumulation allows training with large effective batch sizes even
when GPU memory cannot hold the entire batch simultaneously.

### Solution 2

TODO:  numerical


## Problem 3

Consider a two-layer neural network defined as follows for a single training example $(x[i], y[i])$ (square brackets denote vector indexing):

$$
z_1[i] = W_1 x[i] + b_1 \\
a_1[i] = ReLU(z_1[i]) \\
z_2[i] = W_2 a_1[i] + b_2 \\
\hat{y}[i] = \sigma(z_2[i])
$$

The binary cross-entropy loss is given by

$$L[i] = y[i] \ln(\hat{y}[i]) + (1 - y[i]) \ln(1 - \hat{y}[i])$$

and the empirical risk over $m$ samples is

$$J = \frac{-1}{m} \sum_{i=1}^m L[i]$$

Here, $x[i]$ represents a single input example, and is of shape $\mathbb{R}^{D_x \times 1}$ . 
$y[i] \in \mathbb{R}$ is single output label and is a scalar. There are $m$ samples in the dataset. The hidden layer $z_1$ has $D_{a_1}$ neurons.

1. What are the shapes of $W_1$, $b_1$, $W_2$, $b_2$ for a single example? 
   If the network is vectorized over $m$ examples, what are the shapes of the parameters? What are the shapes of $x, y$ after vectorization?
2. Compute $\frac{\partial J}{\partial \hat{y}[i]}$. Refer to this quantity as $\delta_1[i]$. What is $\frac{\partial J}{\partial \hat{y}}$ ?
3. Compute $\frac{\partial \hat{y}[i]}{\partial z_2}$. Refer to this quantity as $\delta_2[i]$.
4. Compute $\frac{\partial z_2}{\partial a_1}$. Refer to this quantity as $\delta_3[i]$.
5. Compute $\frac{\partial a_1}{\partial z_1}$. Refer to this quantity as $\delta_4[i]$.
6. Compute $\frac{\partial z_1}{\partial W_1}$. Refer to this quantity as $\delta_5[i]$.
7. Compute $\frac{\partial J}{\partial W_1}$. Carefully indicate the shapes.

### Solution 3

Rewriting formulae in terms of vectors of inputs and outputs $x, y$ (samples are rows, features are columns):

$$
z_1 = x W_1^T + b_1 \\
a_1 = ReLU(z_1) \\
z_2 = a_1 W_2^T + b_2 \\
\hat{y} = \sigma(z_2) \quad (\text{Sigmoid}) \\
J = \frac{1}{m} \sum -y \ln(\hat{y}) - (1 - y) \ln (1 - \hat{y}) \quad (\text{Loss/Risk over all samples})
$$

For vectorized network, shapes are (where $m$ is no. of samples, $d$ is no. of input dimensions, $l_1$ is no. of neurons in 1st layer (hidden)):
* $W_1: (l_1, d)$, $b_1: (1, l_1)$
* $W_2: (1, l_1)$, $b_2: (1, 1)$
* $x: (m, d)$, $y: (m, 1)$

NOTE: During vector addition, numpy automatically repeats the bias vectors $b_1, b_2$ via array shape broadcasting (to replace 1 in bias shape dimension) to make the shapes compatible.

If passing only a single example, then $m = 1 \implies x: (1, d), y: (1, 1)$ - shapes of weights and biases aren't affected.

In below, Unit Step Function $u(z) = ReLU'(z)$ is used, which is 1 if $z > 0$ else 0:

$$
\delta_1 = \frac{\partial J}{\partial \hat{y}} = \frac{1}{m} (-\frac{y}{\hat{y}} + \frac{1 - y}{1 - \hat{y}}) \quad (\text{Shape: } (m, 1)) \\
\delta_2 = \frac{\partial \hat{y}}{\partial z_2} = \hat{y} (1 - \hat{y}) \quad (\text{Sigmoid derivative; Shape: } (m, 1)) \\
\delta_3 = \frac{\partial z_2}{\partial a_1} = W_2 \quad (\text{Shape: } (1, l_1)) \\
\delta_4 = \frac{\partial a_1}{\partial z_1} = u(z_1) \quad (\text{ReLU derivative; Shape: } (m, l_1)) \\
\delta_5 = \frac{\partial z_1}{\partial W_1} = x^T \quad (\text{Shape: (d, m)}) \\
\frac{\partial J}{\partial W_1} = ((\delta_1 \cdot \delta_2) \delta_3 \cdot \delta_4)^T x = \frac{1}{m} [((\hat{y} - y) W_2) \cdot u(z_1)]^T \quad (\text{Shape: } (l_1, d))
$$

NOTE: Here $x \cdot y = x^T y$ is dot product.

## Problem 5: Theory: Spectral Convergence of Optimization Methods

Let $f(w) = \frac{1}{2} w^T a w$ where $A \in \mathbb{R}^{d \times d}$ is symmetric positive definite with eigenvalues $\lambda_1 \le \cdots \le \lambda_d$.

Let the spectral decomposition of $A$ be $A = Q D Q^T$ where $D = diag(\lambda_1, \cdots, \lambda_d)$.

(a) Show that Gradient Descent with optimal fixed step size

$$\eta^* = \frac{2}{\lambda_1 + \lambda_d}$$

has convergence rate

$$\|w_k - w^*\|_2 \le (\frac{K-1}{K+1})^K \|w_0 - w^*\|_2$$

where $K = \frac{\lambda_d}{\lambda_1}$

*Hint*:
- Compute $\nabla f(w)$ and write the Gradient Descent update.
- Express the error iteration using $e_k = w_k - w^*$ .
- Use the spectral decomposition $A = Q D Q^T$ to analyze the behavior along eigendirections.

2. Explain mathematically why (using spectral arguments):
- Newton's method converges in one step.
- Conjugate Gradient converges in at most _d_ steps.
- AdaGrad cannot eliminate dependence on k completely.


*Hint*:
- Compute the gradient and Hessian of $f(w)$.
- Write the Newton update and simplify using properties of $A$.
- Consider how optimization methods behave along the eigenvectors of $A$ .
- Recall that Conjugate Gradient constructs $A$-conjugate directions.

### Solution 5

TODO: numerical


## Problem 7: Solve by hand

You are training a 3-layer neural network for a regression task. The network
consists of an input layer (size 3), two hidden layers (size 3 each), and a linear output layer
(size 1).

Network Architecture:
- Layer 1 (Hidden): 3 nodes. Activation: ReLU.
- Layer 2 (Hidden): 3 nodes. Activation: Sigmoid.
- Layer 3 (Output): 1 node. Activation: Linear (None).
- Loss Function: Squared Error, defined as $L = (\hat{y} - y)^2

Initial Values: 
* Input Vector $x = \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}$.
* Target Label $y = 1$
* Learning Rate $\eta = 0.01$

Initial Weights & Biases:(Note: Biases $B_1, B_2, B_3$ are all initialized to zero vectors).

$$
W_1 = \begin{bmatrix} 1 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 2 \end{bmatrix} \\
W_2 = \begin{bmatrix} -1 & 0 & 0.5 \\ 1 & 0 & -0.5 \\ 2 & 0 & -1 \end{bmatrix} \\
W_3 = \begin{bmatrix} 2 & 2 & 2 \end{bmatrix}
$$

Your Task:

1. Perform a forward pass to compute the network's prediction $\hat{y}$ and the Loss $L$.
2. Perform a backward pass to compute the gradients of the loss with respect to all weights and biases.
3. Execute one step of Gradient Descent to calculate the updated weights $W_1, W_2, W_3$ and biases $B_1, B_2, B_3$.

### Solution 7

Activations:
* `y = ReLU(z) = z if z > 0 else 0` -- its gradient is `ReLU'(z) = 1 if z > 0 else 0`
* $y = Sigmoid(z) = \frac{1}{1 + e^{-z}}$ -- its gradient is $y (1 - y)$

1. Forward Pass:

$$
z_1 = W_1 x + B_1 = \begin{bmatrix} 1 \\ -1 \\ 2 \end{bmatrix} \\
a_1 = ReLU(z_1) = \begin{bmatrix} 1 \\ 0 \\ 2 \end{bmatrix} \\
z_2 = W_2 a_1 + B_2 = \begin{bmatrix} -0.5 \\ 0.5 \\ -1 \end{bmatrix} \\
a_2 = Sigmoid(z_2) \approx \begin{bmatrix} 0.37 \\ 0.62 \\ 0.73 \end{bmatrix} \\
\hat{y} = W_3 a_2 + B_3 \approx 3.46 \quad (\text{Predicted Output}) \\
L = (\hat{y} - y)^2 = (3.46 - 1)^2 \approx 6.05 \quad (\text{Loss: Squared Error})
$$

2. Backward Pass (Calculate Gradients):

$$
\frac{\partial L}{\partial \hat{y}} = 2 (\hat{y} - y) \approx 12.10 \quad (\text{Loss gradient}) \\

\frac{\partial L}{\partial a_2} = 12.10 W_3^T \approx \begin{bmatrix} 24.20 \\ 24.20 \\ 24.20 \end{bmatrix} \\
\frac{\partial L}{\partial W_3} = 12.10 a_2^T \approx \begin{bmatrix} 4.477 & 7.502 & 8.833 \end{bmatrix} \quad (\text{Layer 3 weights gradient}) \\

\frac{\partial a_2}{\partial z_2} = a_2 (1 - a_2) = \begin{bmatrix} 0.2331 \\ 0.2356 \\ 0.1971 \end{bmatrix} \\
\frac{\partial L}{\partial z_2} = \left( \frac{\partial L}{\partial a_2} \right)^T \frac{\partial a_2}{\partial z_2} = TODO
$$

3. Gradient Descent to update weights:

$$
TODO
$$


## Problem 9: Numerical: Two Steps of Adam Optimizer


Consider minimizing the scalar function:

$$f(w) = \frac{1}{2} w^2$$

**Consider:**
- $w_t$ : parameter at iteration $t$
- $g_t$: gradient at iteration $t$
- $\beta_1$ : exponential decay rate for first moment
- $\beta_2$ : exponential decay rate for second moment
- $\eta$ : learning rate
- $\epsilon$ : small constant for numerical stability

Let:

$$w_0 = 2, \quad \eta = 0.1, \quad \beta_1 = 0.9, \quad \beta_2 = 0.999, \quad \epsilon = 0$$

1. Compute $w_1$ weight after 1st iteration.
2. Compute $w_2$ weight after 2nd iteration.

### Solution 9

TODO: numerical


## Problem 11: Theoretical Question 

A recommendation system predicts whether a user will **like** a movie $y = 1$ or **not like** it $y = 0$ using two features:

- $x_1 \in \{0,1\}$ : whether the movie is **fiction** (1 = fiction, 0 = non-fiction) - a **dense** feature, present for every movie. 
  The user generally likes fiction and dislikes non-fiction.
- $x_2 \in \{0,1\}$ : whether the movie is **directed by Director Y** - a **sparse** feature, true for very few movies. 
  Whenever Director Y directs, the user likes the movie regardless of genre.

The model is logistic regression $\hat{y} = w_1 x_1 + w_2 x_2$ with cross-entropy loss. 
The per-sample gradient is:

$$g_{i,t} = (\hat{y_t} - y_t) x_{i,t}$$

SGD is run for one epoch over the following 6 movies, with $\hat{y} \approx 0.5$ throughout and $\eta = 0.5$:


Sample | $x_1$ (fiction) | $x_2$ (Dir. Y) | $y$ (liked) | Reason
------ | --------------- | -------------- | ----------- | -----------------------
1      | 1               | 0              | 1           | fiction --> liked
2      | 0               | 0              | 0           | non-fiction --> not liked
3      | 1               | 0              | 1           | fiction --> liked
4      | 0               | 0              | 0           | non-fiction --> not liked
5      | 1               | 0              | 1           | fiction --> liked
6      | 0               | 1              | 1           | non-fction but Dir. Y --> liked


Observe: $x_1$ follows a clean pattern across all 6 samples. $x_2 = 1$ only in sample 6 - a non-fiction movie that the user likes *only* because of Director Y. This is the strongest and cleanest signal in the data, yet $w_2$ receives a gradient update only once in the entire epoch.

1. Compute the net weight update for each weight over the full epoch:

$$\Delta w_i = - \eta \sum_{i=1}^6 g_{i,t}$$

Show your working sample by sample for both $w_1$ and $w_2$.

2. You should observe that $w_2$ receives far fewer non-zero gradient updates than $w_1$ across the epoch. 
   Explain precisely why sparsity of $x_2$ causes learning signal scarcity of $w_2$,
   and why a uniform learning rate \eta cannot compensate for this imbalance even when $x_2$ is the stronger predictor.

3. AdaGrad maintains a per-parameter sum of squared gradients $G_i = \sum_{t=1}^6 g_{i,t}^2$ and replaces the fixed learning rate with:

$$\eta_i^{eff} = \frac{\eta}{G_i + \epsilon}$$

Using your gradients from part 1, compute $G_1, G_2$, and the ratio $\eta_2^{eff} / \eta_1^{eff}$ (use $\epsilon = 10^{-8}$). 
Explain how this ratio reflects AdaGrad's response to gradient starvation.

### Solution 11

TODO: numerical


## Problem 13: Effect of Initialization on Gradient Flow

Consider a deep neural network with 15 hidden layers using ReLU activation. All weights are initialized from $\mathcal{N}(0, 0.01^2)$ (very small variance).

Which of the following is MOST likely to happen during the first few training epochs? Give a detailed explanation for your choice.

1. Activations explode as depth increases.
2. Activations shrink toward zero as depth increases.
3. Gradients become exactly zero for all neurons.
4. The network immediately reaches optimal performance

### Solution 13

No. 2 is most likely - Activations shrink toward zero as depth increases.

**Reason**:

Weights are very small as initialized with mean 0, small variance.
During forward pass, inputs are multiplied by weights to get outputs and then passed through ReLU.
Since weights are small, activation outputs are also small.
Each subsequent layer's output gets smaller and smaller as all weights are very small.
So Activations shrink twoards 0 as depth increases.


## Problem 16: Numerical: Adam Update in Two Dimensions

Consider the function $f(w_1, w_2) = w_1^2 + 4 w_2^2$.

At iteration $t = 1$, the parameter vector is $w_0 = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$

The Adam optimizer uses the following update rules:

$$
g_t = \nabla f(w_t) \\
m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t \\
v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2 \\
\hat{m_t} = \frac{m_t}{1 - \beta_{1,t}}, \quad \hat{v_t} = \frac{v_t}{1 - \beta_{2,t}} \quad (\text{Bias Correction}) \\
w_{t+1} = w_t - \frac{\hat{m_t}}{\sqrt{\hat{v_t}} + \epsilon} \eta \quad (\text{Parameter Update})
$$

Given: $\eta = 0.1, \quad \beta_1 = 0.9, \quad \beta_2 = 0.999, \quad \epsilon = 10^{-8}$

Assume: $m_0 = [0,0], \quad v_0 = [0,0]$

Compute the updated parameter vector $w_1$ after one Adam update step.

### Solution 16

TODO: numerical


