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


   - A neural network with _P_ parameters


   - Each parameter stored in 32-bit floating point (4 bytes)


   - A batch size of _B_


   - Gradient accumulation steps or number of mini-batches _K_ .


**Memory Footprint of Optimizers**


Consider the memory required to store parameters, gradients, and optimizer states.


(a) For **Stochastic Gradient Descent (SGD)** without momentum, determine the total
memory required for storing parameters and gradients.


2


(b) For **SGD with Momentum**, the optimizer additionally stores a momentum vector of
the same size as the parameters. Compute the total memory requirement.


(c) For the **Adam optimizer**, two additional vectors _mt_ and _vt_ are stored for each parameter. Compute the total optimizer memory footprint.


(d) Suppose _P_ = 10 [9] parameters. Compute the memory required (in GB) for each of the
above optimizers.


**Batch Size and Activation Memory**


During training, memory is also required to store intermediate activations for backpropagation.


Assume the activation memory per sample is _A_ bytes.


(a) Express the total activation memory required for batch size _B_ .


(b) Suppose the GPU memory limit is _M_ bytes. Write an inequality involving _B_, _A_, and
optimizer memory that must hold for training to fit into memory.


(c) Explain why increasing batch size _B_ may become infeasible for very large models.


**Convergence vs Batch Size**


Empirical studies suggest that very small batch sizes produce noisy gradient estimates and
slow convergence.


(a) Suppose we desire an effective batch size _B_ large, but due to memory limits we can only
fit a mini-batch of size _b_ where _b < B_ large.


(b) Propose a strategy that allows us to simulate a larger batch using multiple smaller
mini-batches without increasing memory usage.


(c) Let _K_ denote the number of such mini-batches processed before updating the parameters. Express the relationship between _B_ large, _b_, and _K_ .


**Equivalence of Gradient Accumulation and Large Batch Updates**


Let the loss over a batch be defined as the average loss:



_L_ (\theta) = [1]

_B_



_B_


l( _xi,\theta)

_i_ =1



where l( _xi,\theta) is the loss for sample _i_ .


Assume we divide the batch into _K_ mini-batches each of size _b_ = _B/K_ .


(a) Write the gradient of the full batch loss \nabla\thetaL_ (\theta).


3


(b) Let _gk_ be the gradient computed from mini-batch _k_ :



_gk_ = [1]

_b_




- \nabla\theta l( _xi,\theta)


_i \in Bk_



Show that



\nabla\thetaL_ (\theta) = [1]

_K_



_K_


_gk_

_k_ =1



(c) Explain why gradient accumulation allows training with large effective batch sizes even
when GPU memory cannot hold the entire batch simultaneously.

### Solution 2

TODO:  theory


## Problem 3

Consider a two-layer neural network defined as follows for a single training example ( _x_ [(] _[i]_ [)] _, y_ [(] _[i]_ [)] ):


_z_ 1 [(] _[i]_ [)] = _W_ 1 _x_ [(] _[i]_ [)] + _b_ 1

_a_ [(] 1 _[i]_ [)] [= ReLU(] _[z]_ 1 [(] _[i]_ [)][)]

_z_ 2 [(] _[i]_ [)] = _W_ 2 _a_ [(] 1 _[i]_ [)] [+] _[ b]_ [2]

_y_ ^ [(] _[i]_ [)] = \sigma( _z_ 2 [(] _[i]_ [)][)]


The binary cross-entropy loss is given by


_L_ [(] _[i]_ [)] =         - _y_ [(] _[i]_ [)] log ^ _y_ [(] _[i]_ [)] + (1 - y_ [(] _[i]_ [)] ) log(1 - y_ ^ [(] _[i]_ [)] )


and the empirical risk over _m_ samples is



_J_ = _[-]_ [1]

_m_



_m_


_L_ [(] _[i]_ [)] _._

_i_ =1



Here, _x_ [(] _[i]_ [)] represents a single input example, and is of shape R _[D][x][ \times ]_ [1] . _y_ [(] _[i]_ [)] _ \in _ R is single output
label and is a scalar. There are _m_ samples in the dataset. The hidden layer _z_ 1 has _Da_ 1
neurons.


(a) What are the shapes of _W_ 1 _, b_ 1 _, W_ 2 _, b_ 2 for a single example? If the network is vectorized
over _m_ examples, what are the shapes of the parameters? What are the shapes of _X_
and _Y_ after vectorization?

(b) Compute _ \parital  \parital Jy_ ^ [(] _[i]_ [)] [. Refer to this quantity as] \delta 1 [(] _[i]_ [)][. What is] _[ \parital J]_ _ \parital y_ ^ [?]

(c) Compute _[ \parital ]_ _ \parital z_ _[y]_ [^][(] 2 _[i]_ [)] [. Refer to this as] \delta 2 [(] _[i]_ [)][.]

(d) Compute _ \parital a_ _[ \parital z]_ [2] 1 [. Refer to this as] \delta 3 [(] _[i]_ [)][.]

(e) Compute _[ \parital a]_ _ \parital z_ 1 [1] [. Refer to this as] \delta 4 [(] _[i]_ [)][.]


4


(f) Compute _ \parital W \parital z_ 11 [. Refer to this as] \delta 5 [(] _[i]_ [)][.]

(g) Compute _ \parital J_
_ \parital W_ 1 [. Carefully indicate the shapes.]

### Solution 3

TODO: theory 

## Problem 5: Theory: Spectral Convergence of Optimization Methods


Let


_f_ ( _w_ ) = [1]

2 _[w][T]_ _[Aw]_


where _A  \in _ R _[d][ \times ][d]_ is symmetric positive definite with eigenvalues


\lambda _ 1 _\le   \le_ \lambda d_


5


Let the spectral decomposition of _A_ be


where \lambda  = diag( \lambda _ 1 _, . . ., \lambda d_ ).



_A_ = _Q_ \lambda  _Q_ _[T]_



(a) Show that Gradient Descent with optimal fixed step size


2
\eta _[*]_ =
\lambda _ 1 + \lambda d_


has convergence rate




     - k -_ 1
||w_ [(] _[k]_ [)] - w_ _[*]_ ||_ 2 _\le_

k + 1




- _k_
||w_ [(0)] - w_ _[*]_ ||_ 2



where


_Hint:_



k = _[\lambda ][d]_

\lambda _ 1




    - Compute \nabla f_ ( _w_ ) and write the Gradient Descent update.

     - Express the error iteration using _e_ [(] _[k]_ [)] = _w_ [(] _[k]_ [)] - w_ _[*]_ .

     - Use the spectral decomposition _A_ = _Q_ \lambda  _Q_ _[T]_ to analyze the behavior along eigendirections.


(b) Explain mathematically why (using spectral arguments):


     - Newton's method converges in one step.

     - Conjugate Gradient converges in at most _d_ steps.

     - AdaGrad cannot eliminate dependence on k completely.


_Hint:_


     - Compute the gradient and Hessian of _f_ ( _w_ ).

     - Write the Newton update and simplify using properties of _A_ .

     - Consider how optimization methods behave along the eigenvectors of _A_ .

     - Recall that Conjugate Gradient constructs _A_ -conjugate directions.

### Solution 5

TODO: theory


## Problem 7: Solve by hand

You are training a 3-layer neural network for a regression task. The network
consists of an input layer (size 3), two hidden layers (size 3 each), and a linear output layer
(size 1).


Network Architecture:


   - Layer 1 (Hidden): 3 nodes. Activation: ReLU.


   - Layer 2 (Hidden): 3 nodes. Activation: Sigmoid.


   - Layer 3 (Output): 1 node. Activation: Linear (None).


   - Loss Function: Squared Error, defined as _L_ = (^ _y -_ _y_ ) [2]






 



Initial Values: Input Vector ( _X_ ):


Target Label ( _y_ ): 1
Learning Rate ( \eta ): 0.01



1
1
1







Initial Weights & Biases:(Note: Biases _B_ 1 _, B_ 2 _, B_ 3 are all initialized to zero vectors).







 



_W_ 1 =



1 0 0
0 _-_ 1 0
0 0 2











 



_W_ 2 =



 _-_ 1 0 0 _._ 5

 1 0 _-_ 0 _._ 5
2 0 _-_ 1







_W_ 3 = 2 2 2


Your Task:


1. Perform a forward pass to compute the network's prediction ( _y_ ^) and the Loss ( _L_ ).


2. Perform a backward pass to compute the gradients of the loss with respect to all weights
and biases.


7


3. Execute one step of Gradient Descent to calculate the updated weights ( _W_ 1 _, W_ 2 _, W_ 3)
and biases ( _B_ 1 _, B_ 2 _, B_ 3)

### Solution 7

TODO: theory


## Problem 9: Numerical: Two Steps of Adam Optimizer


Consider minimizing the scalar function:



**Consider:**


 - _wt_ : parameter at iteration _t_



_f_ ( _w_ ) = [1]

2 _[w]_ [2]


8


   - _gt_ : gradient at iteration _t_

   - \beta 1 : exponential decay rate for first moment

   - \beta 2 : exponential decay rate for second moment

   - \eta : learning rate


   - \epsilon : small constant for numerical stability


Let:


_w_ 0 = 2 _,_ \eta = 0 _._ 1 _,_ \beta 1 = 0 _._ 9 _,_ \beta 2 = 0 _._ 999 _,_ \epsilon = 0


(a) Compute _w_ 1 weight after 1st iteration.


(b) Compute _w_ 2 weight after 2nd iteration.

### Solution 9

TODO: theory


## Problem 11: Theoretical Question 

A recommendation system predicts whether a user will **like** a
movie ( _y_ = 1) or **not like** it ( _y_ = 0) using two features:


   - _x_ 1 _ \in {_ 0 _,_ 1 _}_ : whether the movie is **fiction** (1 = fiction, 0 = non-fiction) — a **dense**
feature, present for every movie. The user generally likes fiction and dislikes non-fiction.


   - _x_ 2 _ \in {_ 0 _,_ 1 _}_ : whether the movie is **directed by Director Y**    - a **sparse** feature, true
for very few movies. Whenever Director Y directs, the user likes the movie regardless
of genre.


The model is logistic regression ^ _y_ = \sigma( _w_ 1 _x_ 1 + _w_ 2 _x_ 2) with cross-entropy loss. The per-sample
gradient is:


_gi_ [(] _[t]_ [)] =                       - _y_ ^ [(] _[t]_ [)] - y_ [(] _[t]_ [)][] _ x_ [(] _i_ _[t]_ [)]


SGD is run for one epoch over the following 6 movies, with ^ _y ≈_ 0 _._ 5 throughout and \eta = 0 _._ 5:


Sample _x_ 1 (fction) _x_ 2 (Dir. Y) _y_ (liked) Reason
1 1 0 1 fiction _->_ liked
2 0 0 0 non-fiction _->_ not liked
3 1 0 1 fiction _->_ liked
4 0 0 0 non-fiction _->_ not liked
5 1 0 1 fiction _->_ liked
6 0 1 1 non-fction but Dir. Y _->_ liked


Observe: _x_ 1 follows a clean pattern across all 6 samples. _x_ 2 = 1 only in sample 6 — a
non-fiction movie that the user likes _only_ because of Director Y. This is the strongest and
cleanest signal in the data, yet _w_ 2 receives a gradient update only once in the entire epoch.


(a) Compute the net weight update for each weight over the full epoch:



\Delta _wi_ = _- \eta



6


_gi_ [(] _[t]_ [)]

_t_ =1



Show your working sample by sample for both _w_ 1 and _w_ 2.


10


(b) You should observe that _w_ 2 receives far fewer non-zero gradient updates than _w_ 1 across
the epoch. Explain precisely why sparsity of _x_ 2 causes learning signal scarcity of _w_ 2,
and why a uniform learning rate \eta cannot compensate for this imbalance even when _x_ 2
is the stronger predictor.

(c) AdaGrad maintains a per-parameter sum of squared gradients _Gi_ = [] _t_ [6] =1 [(] _[g]_ _i_ [(] _[t]_ [)][)][2][ and]
replaces the fixed learning rate with:


\eta
\eta i_ [eff] = ~~_\sqrt_~~
_Gi_ + \epsilon


Using your gradients from part (a), compute _G_ 1, _G_ 2, and the ratio \eta 2 [eff] _[/η]_ 1 [eff] (use \epsilon =
10 _[-]_ [8] ). Explain how this ratio reflects AdaGrad's response to gradient starvation.

### Solution 11

TODO: theory


## Problem 13: Effect of Initialization on Gradient Flow


Consider a deep neural network with 15 hidden layers using ReLU activation. All weights are
initialized from _N_ (0 _,_ 0 _._ 01 [2] ) (very small variance).


Which of the following is MOST likely to happen during the first few training epochs? Give
a detailed explanation for your choice.


(A) Activations explode as depth increases.


(B) Activations shrink toward zero as depth increases.


(C) Gradients become exactly zero for all neurons.


(D) The network immediately reaches optimal performance

### Solution 13

TODO: theory


## Problem 16: Numerical: Adam Update in Two Dimensions

Consider the function
_f_ ( _w_ 1 _, w_ 2) = _w_ 1 [2] [+ 4] _[w]_ 2 [2]

At iteration _t_ = 1, the parameter vector is


1
_w_ [(0)] =
2


The Adam optimizer uses the following update rules:


_gt_ = \nablaf_ ( _wt_ )


_mt_ = \beta 1 _mt-_ 1 + (1 - \beta 1) _gt_


_vt_ = \beta 2 _vt-_ 1 + (1 - \beta 2) _gt_ [2]


13


Bias correction:


Parameter update:


Given:


Assume



_mt_ _vt_
_m_ ^ _t_ = _,_ _v_ ^ _t_ =
1 - \beta 1 _[t]_ 1 - \beta 2 _[t]_


_wt_ +1 = _wt -_ \eta ~~_\sqrt_~~ _m_ ^ _t_
_v_ ^ _t_ + \epsilon


\eta = 0 _._ 1 _,_ \beta 1 = 0 _._ 9 _,_ \beta 2 = 0 _._ 999 _,_ \epsilon = 10 _[-]_ [8]



0
_m_ 0 =
0




- 0
_,_ _v_ 0 =
0







Compute the updated parameter vector _w_ [(1)] after one Adam update step.

### Solution 16

TODO: theory


