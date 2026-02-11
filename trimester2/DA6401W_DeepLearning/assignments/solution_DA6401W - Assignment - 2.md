# DA6401W - Assignment 2

Author: Sohang Chopra &lt;DA25M622&gt;

## Problem 1: Effect of Network Depth on Learning Performance

In this question, you will study how the depth of a neural network affects learning and
generalization. You must implement all models **from scratch using NumPy only** . The
use of `sklearn`, `torch`, or `tensorflow` for model implementation is strictly prohibited.

### (a) Dataset Generation and Experimental Setup

Generate a synthetic binary classification dataset as follows:
- Input space: $x = (x_1, x_2) \in R^2$
- Number of samples: $N = 1000$
- Class labels: $y \in \{0, 1\}$

Data generation rule:

$$y = \begin{cases}
1 & \text{if } x_1^2 + x_2^2 > 0.5 \\
0 & \text{otherwise}
\end{cases}
$$

where $x_1, x_2$ are sampled uniformly from $[-1,1] \times [-1,1]$.

Split the dataset into:
- Training set: 80% of the data
- Test set: 20% of the data

Plot the dataset and explain why a linear classifier cannot solve this problem.

### (b) Neural Network Architectures

Implement the following two neural networks:

**Model 1 (Shallow Network):**
- Input layer: 2 neurons
- One hidden layer: 20 neurons
- Output layer: 1 neuron

**Model 2 (Deeper Network):**
- Input layer: 2 neurons
- Hidden layer 1: 10 neurons
- Hidden layer 2: 10 neurons
- Output layer: 1 neuron

Both models must use:
- ReLU activation in hidden layers
- Sigmoid activation in the output layer

### (c) Training Procedure

Train both models using the following fixed hyperparameters:
- Loss function: Binary Cross-Entropy
- Optimization method: Batch Gradient Descent
- Learning rate: $\eta = 0.01$
- Number of epochs: 100
- Weight initialization: $\mathcal{N}(0, 0.1)$
- Bias initialization: zeros

Plot the training loss versus epochs for both models on the same graph.

### (d) Evaluation Metrics

Evaluate both trained models on the test set using:
- Classification accuracy
- Confusion matrix

Use a decision threshold of 0.5 on predicted probabilities.

### (e) Analysis

Compare the two models and discuss the effect of depth in terms of:
- Representational capacity
- Optimization difficulty
- Generalization performance

### Solution 1 (a)

TODO: code

### Solution 1 (b)

TODO: code

### Solution 1 (c)

TODO: code

### Solution 1 (d)

TODO: code

### Solution 1 (e)

TODO: code


## Problem 2: Backpropagation in a Feedforward Neural Network

Consider a fully connected feedforward neural network with one hidden layer used for a
regression task. The network structure is as follows:
- **Input layer:** $x \in \mathbb{R}^d$
- **Hidden layer:** $h = ReLU(W_1 x + b_1)$
- **Output layer:** $\hat{y} = W_2 h + b_2$

The loss function used is the **mean squared error (MSE)** defined as:

$$L = \frac{1}{2} (y - \hat{y})^2$$

### (a) Forward Pass

Derive the expression for the network output $\hat{y}$ in terms of the input $x$, weights, and
biases.

### (b) Loss Gradient at Output Layer

Compute the gradient of the loss $L$ with respect to the output layer parameters $W_2$ and $b_2$.

### (c) Backpropagation Through Hidden Layer

Using the chain rule, derive the expression for the gradient of the loss with respect to the hidden layer weights $W_1$. 
Clearly indicate how the derivative of the ReLU activation affects the gradient flow.

### (d) Role of the Chain Rule

Explain briefly how the chain rule enables efficient gradient computation in deep networks
and why backpropagation is computationally efficient compared to naive differentiation.

### (e) Vanishing Gradient Discussion

State whether the use of ReLU activation helps mitigate the vanishing gradient problem.
Justify your answer.

### Solution 2 (a)

TODO: theory

### Solution 2 (b)

TODO: theory

### Solution 2 (c)

TODO: theory

### Solution 2 (d)

TODO: theory

### Solution 2 (e)

TODO: theory


## Problem 3: Simple Gradient Descent

You are optimizing a loss function $L(w) = w^4 - 10 w^2 + 5 w + 40$ .

1. Start with an initial parameter $w_0 = 1$. 
   Using a learning rate (step size) of $\eta = 0.01$, perform one manual iteration of gradient descent to find $w_1$. 
   Calculate the squared error for $w_0$ and $w_1$. Did the loss decrease?
2. Will this setup of initial parameter $w_0 = 1$ reach global minima of the given error surface? 
   Give the range of the initial parameter that will definitely converge to the global minima in the standard gradient descent approach.
3. If you chose a learning rate of $\eta = 2.0$ for this specific problem, what would happen to $w_1$ and the loss at $w_1$? Show the calculation.
4. Plot the loss function for the range $w \in [-3,3]$.

### Solution 3

TODO: theory


## Problem 4: Code the Activation Functions


1. Create a class or set of functions in Python (using numpy) for the following activation
functions:
    * Sigmoid $\sigma(x) = \frac{1}{1 + e^{-x}}$
    * Tanh $tanh(x) = \frac{1 - e^{-2 x}}{1 + e^{-2 x}}$
    * ReLU $relu(x) = max(0,x)$
    * Leaky ReLU (use $\alpha = 0.01$) x if x > 0 else $\alpha x$
2. Implement the derivative for each function.
3. Visualization: Generate a range of inputs from -5 to 5. Plot each activation function and its corresponding derivative on the same graph.

### Solution 4

TODO: code


## Problem 5: Numerical: Forward Pass in a Multilayer Perceptron

Consider a multilayer perceptron with:
- Input: $x = [1, -2]^T$
- One hidden layer with 2 neurons and ReLU activation
- Output layer with 1 neuron (linear activation)


The parameters are given as:

$$
W_1 = \begin{pmatrix} 1 & -1 \\ 2 & 0 \end{pmatrix}, \quad b_1 = \begin{pmatrix} 0 \\ 1 \end{pmatrix} \\
W_2 = \begin{pmatrix} 2 & -1 \end{pmatrix}, \quad b_2 = 0
$$

1. Compute the hidden layer pre-activation values.
2. Apply the ReLU activation.
3. Compute the final network output.

### Solution 5

TODO: theory


## Problem 6: Numerical Verification of Universal Approximation Theorem

A single hidden layer multilayer perceptron (MLP) with a non-linear activation function can
approximate any continuous function on a compact domain.

Consider the target function:

$$f(x) = sin(2 \pi x) + 0.5 x^2, \quad x \in [0,1]$$

A single hidden layer neural network is defined as:

$$\hat{f}(x) = \sum_{i=1}^3 \alpha_i \sigma(w_i x + b_i)$$

where the activation function is $\sigma(z) = \frac{1}{1 + e^{-z}}$.

The network parameters are:

$$w = [2, -3, 4],  \quad b = [-1, 2, -2], \quad \alpha = [1.5, -1, 0.5]$$

1. Compute the network output $\hat{f(x)}$ for the inputs $x = \{0, 0.5, 1\}$
2. Compute the Mean Squared Error (MSE):

$$MSE = \frac{1}{3} \sum_{i=1}^3 (f(x_i) - \hat{f}(x_i))^2$$

### Solution 6

TODO: theory


## Problem 7: Programming: Gradient Checking for Neural Network Training

You need to implement a gradient checking procedure to verify the correctness of backpropagation in a multilayer perceptron (MLP).


Consider the following neural network architecture for regression:
- Input layer: $x \in \mathbb{R}^2$
- Hidden layer: 5 neurons with sigmoid activation
- Output layer: 1 neuron with linear activation


The network equations are:

$$
h = \sigma(W_1 x + b_1) \\
\hat{y} = W_2 h + b_2
$$


The loss function is $L = \frac{1}{2} (y - \hat{y})^2$.
You must generate a small synthetic dataset consisting of 20 samples where $x_1, x_2 \in Uniform(-1,1)$
and the target output is $y = x_1^2 + x_2^2$.

1. Implement forward propagation and manual backpropagation using NumPy.
2. Implement gradient checking using finite difference approximation:

$$\frac{\partial L}{\partial \theta} = \frac{L(\theta + \epsilon) - L(\theta - \epsilon)}{2 \epsilon}$$

where $\epsilon = 10^{-5}$ and $\theta$ represents any network parameter.

3. Compare analytical gradients obtained using backpropagation with numerical gradients
for at least three randomly chosen parameters.
4. Report the relative error between analytical and numerical gradients and comment on
the correctness of your implementation.


**Implementation Requirements:**
- Use NumPy only.
- Initialize weights randomly.
- Perform gradient checking before training the network.

### Solution 7

TODO: code


## Problem 8: Programming

Consider the problem of function approximation under different hypothesis
classes.


Let the true data-generating function be $y = sin(x)$ where $x \in [0, 2 \pi]$. 
A dataset is created by sampling $n$ points uniformly from this interval and adding i.i.d. Gaussian noise:

$$y_i = sin(x_i) + \epsilon_i, \quad \epsilon_i \sim \mathcal{N}(0, \sigma^2)$$


You are asked to study the **bias-variance tradeoff** using different hypothesis classes.
Let $\hat{f_D}(x)$ denote the predictor learned from a training dataset $D$ .

The expected prediction at a point $x$, over all possible training datasets of size $n$, is given by:

$$E_D[\hat{f}_D(x)]$$


The **bias** of the estimator at $x$ is defined as:

$$Bias(x) = E_D[\hat{f}_D(x)] - sin(x)$$

The **variance** of the estimator at _x_ is defined as:

$$Var(x) = E_D[(f_D(x) - E_D[f_D(x)])^2]$$

### 1. Linear Hypothesis

Assume the hypothesis class is linear:

$$y = W x + c$$

* Fit the model to the sampled data.
* Report the training & testing error. Visualize the learned hypothesis along with the true function and sampled points.
* Experiment with different values of _W_ and _c_ (either manually or via least-squares
fitting).
* Comment on the bias and variance of this model with respect to the true function.

### 2. Polynomial Hypothesis

Now consider a polynomial hypothesis of degree $d$ :

$$y = \sum_{k=0}^d w_k x^k$$

* Fit polynomial models for increasing values of $d$ (eg. 3, 5, 10).
* Report the training & testing error. Visualize the fitted polynomials along with the true function and sampled data.
* Observe the behavior of the learned function as the degree increases.
* Comment on how bias and variance change as model complexity increases.

### 3. Generalization Behavior (Optional)

Repeat the above experiments using different random samples from the same datagenerating process. 
Compare training and test performance across models and comment on generalization.

### Solution 8.1

TODO: code

### Solution 8.2

TODO: code

### Solution 8.3

TODO: code


## Problem 9

Consider a Multilayer Perceptron (MLP) consisting of fully connected layers with an activation function applied after each linear transformation.


1. Explain why activation functions are essential in an MLP. What would be the representational power of an MLP if no activation functions were used?
2. Let an MLP consist of multiple layers, each of the form

$$h_l = \phi(W_l h_{l-1} + b_l)$$

where $\phi$ is an activation function. Show that if $\phi$ is the identity function, the entire network reduces to a single linear transformation.

3. Discuss the role of nonlinearity in enabling MLPs to approximate complex functions. Briefly relate your answer to the Universal Approximation Theorem.
4. Compare sigmoid, tanh, and ReLU activation functions in terms of:
* output range,
* gradient behavior,
* suitability for deep networks.

### Solution 9

TODO: theory


## Problem 10

Consider a binary classification problem with input-label pairs:

$$x \in \mathbb{R}^d, \quad y \in \{0,1\}$$

A fully connected neural network with an input dimension of $d$ is trained using two hidden layers of sizes $\frac{d}{2}$ and $\frac{d}{4}$, 
followed by a single output neuron where all hidden layers use sigmoid activation functions. 
The output layer uses a sigmoid activation, and the loss function is binary cross-entropy.

The network is trained using gradient-based optimization under the following initialization
and training settings:
1. All weights and biases are initialized to the same constant value.
2. Xavier initialization is used for all layers.
3. Weights are initialized randomly with small independent noise.

* For each initialization setting, determine whether the network is able to learn meaningful representations.
* For each case, explain the effect of the initialization on symmetry breaking and gradient flow during training.

### Solution 10

TODO: theory


## Problem 11

Implement a two-layer neural network with 2 input neurons, 10 hidden neurons, and 1 output neuron using ReLU activation in the hidden layer to solve the XOR classification problem. Investigate how the learning rate and bias initialization affect the dying ReLU phenomenon. Weights are initialized as:

$$W \sim \mathcal{N}(0, 0.01)$$

unless stated otherwise.

**Tasks**:

1. Train the network under the following five configurations:
   - Case 1: Learning rate = 0.1, Bias initialization = -5.0, Epochs = 500
   - Case 2: Learning rate = 0.1, Bias initialization = 0.0, Epochs = 500
   - Case 3: Learning rate = 0.01, Bias initialization = -5.0, Epochs = 500
   - Case 4: Learning rate = 0.01, Bias initialization = 0.0, Epochs = 500
   - Case 5: Learning rate = 0.01, Bias initialization = random, Epochs = 10000

2. For each configuration, plot a grid of figures showing:
    - Row 1: Training loss versus epochs
    - Row 2: Fraction of dead hidden neurons versus epochs
    - Row 3: Classification accuracy versus epochs

3. Answer the following questions:
    * Which configurations exhibit dying ReLU behavior? Explain why.
    * Why are dead ReLU neurons unable to recover through gradient descent?

### Solution 11

TODO: code


## Problem 12: Basics of Computational Graphs

Consider the function:

$$z = (x + y) y$$

where $x, y \in \mathbb{R}$.

1. **Graph Representation**

Write the sequence of intermediate computations needed to evaluate $z$ . (These define the computational graph nodes.)

2. **Forward Evaluation**

Compute $z$ for $x=2, y=3$.

3. **Gradient Computation**

Using the computational graph, compute:

$$\frac{\partial z}{\partial x}, \frac{\partial y}{\partial x}$$

(d) **Conceptual**

In one or two sentences, explain why computational graphs are useful for training neural
networks.

### Solution 12

TODO: theory


