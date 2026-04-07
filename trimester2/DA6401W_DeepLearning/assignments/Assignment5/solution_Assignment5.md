---
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

# DA6401W - Assignment 5

## Department of Data Science and AI, IIT Madras April 2026

Submitted by: Sohang Chopra &lt;DA25M622&gt;

## Problem 1: Numerical: Normalization Dynamics and Gradient Flow in Deep CNN


Consider a convolutional neural network receiving a multi-channel input of size $64 \times 64 \times 3$.
The network performs the following sequence of operations:


1. Convolution Layer 1 Filters = 16, Kernel = $7 \times 7$, Stride = 2, Padding = 3
2. Batch Normalization
3. Max Pooling Pool size = $3 \times 3$, Stride = 2, Padding = 1
4. Residual Block consisting of two convolution layers Kernel = $3 \times 3$, stride = 1, padding = 1, filters = 16 Identity skip connection.
5. Global Average Pooling followed by Fully Connected layer.


Answer the following:

1. Compute feature map dimension after each stage.
2. BatchNorm statistics: $\mu = 12, \sigma^2 = 16, \gamma = 0.5, \beta = -1$. Find normalized output for activation $x = 20$.
3. Residual mapping produces $F(x) = \begin{bmatrix} 2 \\ -1 \\ 0.5 \end{bmatrix}, x = \begin{bmatrix} 1 \\ 3 \\ -0.5 \end{bmatrix}$. Compute block output.
4. Gradient clipping with threshold $c = 5$. If gradient norm is $|g|_2 = 25$, find:
    * clipped gradient vector expression
    * new gradient norm
5. Min-max normalization range $[-4, 28]$. Compute normalized value for $x = 20$.

### Solution 1

TODO: numerical


## Problem 3

Training deep neural networks often involves stabilizing both forward activations and backward gradients. 
Two commonly used techniques are **normalization methods** (Batch Normalization, Layer Normalization) and **gradient clipping** .

1. **Batch Normalization vs Layer Normalization**: Consider an input tensor $X \in \mathbb{R}^{B \times d}$, where $B$ is the batch size and $d$ is the feature dimension.
    * Write the mathematical formulation of **Batch Normalization** and clearly indicate
    along which dimension mean and variance are computed.
    * Write the formulation of **Layer Normalization** and specify the normalization dimensions.
    * Explain why Batch Normalization performance degrades when the batch size is very
    small, whereas Layer Normalization does not suffer from this issue.
    * In the context of sequence models (e.g., Transformers), explain why Layer Normalization is preferred over Batch Normalization.

2. **Effect on Optimization Dynamics**
    * Explain how normalization methods affect the conditioning of the optimization problem.
    * Discuss the role of normalization in mitigating *internal covariate shift* . Is this explanation sufficient to justify their effectiveness?

3. **Gradient Clipping**: During training, suppose the gradient vector $g \in \mathbb{R}^n$ has a very large norm.
    * Define **gradient clipping by norm** and write its mathematical formulation.
    * Show that after clipping with threshold _c_, the resulting gradient has norm at most $c$ .
    * Explain how gradient clipping helps in training recurrent or very deep networks.

### Solution 3

TODO: theory


## Problem 5: Numerical: Effect of Stride and Padding in Convolution

Consider an input image of size $64 \times 64 \times 3$. A convolution layer is applied with the following parameters:

- Number of filters = 32
- Kernel size = $5 \times 5$
- Stride = 2
- Padding = 2


1. Compute the spatial dimensions of the output feature map.
2. Compute the total number of learnable parameters in the convolution layer (including
bias).

### Solution 5

TODO: numerical


## Problem 6: Conceptual: Residual Connections and Optimization

Consider two neural networks with identical depth:
- Network A: Plain CNN
- Network B: Residual CNN with skip connections

A residual block computes

$$y = F(x) + x$$

Answer the following:

1. Explain why residual connections improve gradient flow during backpropagation.
2. Suppose $F(x) = 0$. What is the output of the residual block? What does this imply about training very deep networks?

### Solution 6

TODO: theory


## Problem 9 Numerical: Large Kernel vs Small Kernels with Pooling

Consider an input feature map $X \in R^{64 \times 64 \times 3}$.

Two different designs are applied:

**Design A (Single Large Convolution):**
- Kernel size = $7 \times 7$
- Number of filters = 64
- Stride = 2, Padding = 3

**Design B (Smaller Convolutions + Pooling):**
- First layer: $3 \times 3$, 32 filters, stride = 1, padding = 1
- Max Pooling: $2 \times 2$, stride = 2
- Second layer: $3 \times 3$, 64 filters, stride = 1, padding = 1

**Tasks:**
1. Compute the output feature map dimensions for:
    - Design A
    - Design B (after all layers)
2. Compute the total number of learnable parameters (including bias) for Design A.
3. Compute the total number of learnable parameters (including bias) for Design B.
4. Compute the ratio:

$$\frac{\text{Parameters in Design B}}{\text{Parameters in Design A}}$$

### Solution 9

TODO: numerical


## Problem 11 (Theoretical Question - Weight Initialization in CNNs with ReLU)

Consider the following CNN architecture trained for image classification with inputs shape (batch_size, a, b, 3):


**Fan-in and Fan-out Definitions:**
- **Convolutional layers:** both fan_in and fan_out use the full receptive field area $k \times k$, multiplied by the respective channel count:

$$fanin = C_{in} \times k \times k, \quad fanout = C_{out} \times k \times k$$

- **Fully connected layers:**

fanin = number of input neurons , fanout = number of output neurons

| Layer | Type                | Details                                          | Activation |
| ----- | ------------------- | ------- ---------------------------------------- | ---------- |
| 1     | Conv2D              | kernel = $3 \times 3$, in_ch = 3, out_ch = 64    | ReLU
| 2     | BatchNorm + MaxPool | $2 \times 2$ pool                                | _
| 3     | Conv2D              | kernel = $3 \times 3$, in_ch = 64, out_ch = 128  | ReLU
| 4     | BatchNorm + MaxPool | $2 \times 2$ pool                                | _
| 5     | Conv2D              | kernel = $3 \times 3$, in_ch = 128, out_ch = 256 | ReLU
| 6     | Flatten             | $4 \times 4 \times 256 = 4096$                   | _
| 7     | FC (Linear)         | 4096 --> 1024                                    | ReLU
| 8     | FC (Linear)         | 1024 --> 10                                      | Softmax


* State the **Kaiming He Normal** initialization formula. Define every term clearly, including how fan in is computed for a convolutional layer.
* State the **Kaiming He Uniform** initialization formula and explain how it relates to the normal variant.
* For each **convolutional layer** in the network above, compute fanin, fanout, the standard deviation $\sigma$ (normal), and the bound $a$ (uniform).
* For each **fully connected layer** in the network above, compute fanin, fanout, $\sigma$, and $a$ .

### Solution 11

TODO: numerical


## Problem 12: Hyperparameter Optimization Strategies

1. How does Bayesian Optimization differ from grid search and random search in its approach to hyperparameter tuning? What key advantage does it offer?
2. Why cannot Bayesian Optimization replace gradient descent for training neural networks?
3. Why cannot gradient descent be used directly for hyperparameter tuning? What property of the hyperparameter optimization problem makes it fundamentally different from model training?

### Solution 12

TODO: theory


## Problem 13

In an image segmentation task, the goal is to separate pets from the background. The ground truth labels are provided as a tensor:

$$Y \in \mathbb{R}^{H \times W \times 1}$$

where each pixel takes a value in $\{0,1\}$, with 1 indicating the presence of a pet and 0 indicating background.

Now consider extending this task to identify additional elements in the image such as trees, roads, and other objects.

1. **Label Representation**
   * Do you think the same labeling strategy (single-channel binary mask) would be sufficient for this extended task? Justify your answer.
   * If not, propose a suitable labeling strategy. Clearly describe:
      - how each pixel should be represented,
      - the shape of the label tensor.
   * What should be the shape of the model output for this task?

2. **Loss Function**
   * What loss function would you use for this problem? Write its mathematical form.
   * In practice, datasets may have imbalance between different regions (e.g., large background vs small objects). Suggest an additional loss (or modification) to address this and briefly explain why.

### Solution 13

TODO: theory