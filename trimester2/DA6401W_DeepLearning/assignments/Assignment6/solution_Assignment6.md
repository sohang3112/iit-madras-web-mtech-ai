---
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

# DA6401W (Intro to Deep Learning) - Assignment 6

Submitted by: Sohang Chopra &lt;DA25M622&gt;

<!-- out of 8 Qs, only 1 theory, rest code Qs -->

## Problem 7

Consider a simple Recurrent Neural Network (RNN) defined for time steps $t = 1, 2, 3$ :

$$
h_t = tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h) \\
o_t = W_{hy} h_t + b_y \\
\hat{y_t} = o_t
$$

Total loss is given by:

$$ L = \sum_{t=1}^3 L_t, \quad \text{where } L_t = \frac{1}{2} |\hat{y_t} - y_t|^2 $$

1. Derive expression for $\frac{\partial L}{\partial W_{hy}}$
2. Let $a_t = W_{hh} h_{t-1} + w_{xh} x_t + b_h$. Derive recursive expression for $\delta_t = \frac{\partial L}{\partial a_t}$.
3. Using the result above, derive $\frac{\partial L}{\partial W_{hh}}$.
4. Briefly explain why vanishing and exploding gradients occur in **Backpropogation Through Time (BPTT)** .

### Solution 7

Derivative of $y=tanh(x)$ is $1-y^2$ .

1. $\frac{\partial L}{\partial W_{hy}} = \sum_{t=1}^3 (\hat{y_t} - y_t) h_t^T$
2. 
$$
\delta_t = \frac{\partial L}{\partial a_t} = \frac{\partial L}{\partial \hat{y_t}} \frac{\partial \hat{y_t}}{\partial h_t} \frac{\partial h_t}{\partial a_t} \\
\implies \delta_t = ((\hat{y_t} - y_t) W_{hy} + \delta_{t+1} W_{hh}) (1 - h_t^2) \quad (\text{accounting for both immediate loss and also gradient from future loss}) 
$$
3. $\frac{\partial L}{\partial W_{hh}} = \sum_{t=1}^3 \delta_t h_{t-1}^T$
4. In **Backpropogation Through Time (BPTT)**, weight matrix $W_{hh}$ is repeatedly multiplied by itself as part of gradient calculation in above formula. If eigenvalues of weight matrix are more than 1, then values tend to become larger and larger (exploding gradient), else if less than 1 then values tend to shrink towards 0 (vanishing gradient).
