1. a) Activations:

Activation | Formula | Gradient | Use
Sigmoid    | 1/(1+e^-z) | y(1-y) | Binary classification output probabilities; NOT In hidden layers due to vanishing gradients
Softmax    | e^zi / sum(e^zj) | _ | Multi-class classification probabilities
ReLU       | max(0,z) | 1 if y > 0 else 0 | Hidden layers; fixes Vanishing Gradient as long as wx + b > 0
Leaky ReLU | z if z > 0 else alpha z | 1 if y > 0 else alpha | Fixes Dying ReLU
SeLU       | 

In MSE and Binary Cross Entropy -- in both use predicted probability, NOT predicted class.

MSE use with Sigmoid can cause Vanishing Gradient problem; BCE gradient "cancels out" sigmoid gradient allowing gradient to stay strong.
BCE is more sensitive to and heavily penalizes "confidently wrong".

1. b) Single-Layered model (ie no hidden layers, only an output layer) can only model linear functions, it cannot fit non-linear functions.
   
Universal Approximation Theorem: a multi-perceptron with one or more hidden layers can model any differentiable function.

2. CNN - SKIP

3. AutoEncoder, RNN - SKIP

4. RNN - SKIP
(Bootstrapping is a resampling method: resample (with replacement) ie draw many samples from dataset; then we can take average of required stat (eg. median) of all samples)

5. RNN - SKIP

6. Feed-forward:
Computational graph is built where output of a layer becomes input of next layer. Feed-forward is just calculating all intermediate outputs and then final model output.
Each layer output is activation(X W)

Backpropogation:
Weight gradients for each layer are calculated , update using gradient descent equation: W = W - lr * gradients

Gradient calculation:
dX = nabla_output loss    # (1,N)
for i in reversed layers indices:
   dZ = activation_gradient(y)
   dW = dZ^T X
   dX = W^T dZ

7. SKIP

8. SKIP



