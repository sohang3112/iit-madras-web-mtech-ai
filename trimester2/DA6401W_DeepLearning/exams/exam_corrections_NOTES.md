Q5 (marked wrong) -> I answered -w^(-1) b , the expected answer is -b/w . Both mean same thing so should be marked correct.

Q11 (marked wrong) -> I answered 0.8, 0.1 (with space), expected answer didn't have space. should be marked correct.

Q18 (marked wrong) -> I answered 128 (numerator / denominator). expected answer is 128:1 . should be marked correct (expected format was not clear in question).

----------

## QUESTIONS WHERE I ANSWERED WRONG:

Q9 Estimate sqrt(4.2) using second-degree Taylor polynomial centered at x=4. Correct to 3 decimal places.
$$
f(x) = sqrt(x), f'(x) = 1/(2*sqrt(x)), f''(x) = -1/(4*x*sqrt(x)) \\
f(4.2) ~ sqrt(4) + (4.2-4) * 1/(2*sqrt(4)) + 1/2 (4.2-4)^2 * -1/(4*4*sqrt(4)) = 2 + .2 / 4 - .2^2 / 64 = 2.05 - .01 / 16 = 2.049
$$

Q12 Consider simple computation graph with scalar inputs x=2, y=3. Intermediate node z = xy, output loss L = z^2. Calculate gradient of loss wrt x.
Ans 2 x y^2 = 2 * 2 * 3^2 = 36

Q13 Select correct properties of norm & loss functions: (wrong option I selected was L2 regularization leads to sparse weights by setting coefficients to 0 -> only L1 does that)

Q19 Consider a 3-class classification problem with logits z = (1,2,0). True class one-hot encoded label is y = (0,1,0). Model uses softmax followed by cross-entropy loss. Gradient of loss wrt first logit?
Ans softmax of 1st logit = e^1 / (e^1 + e^2 + 0) = 0.2447; gradient of softmax + cross entropy = y_{pred} - y_{true} = 0.2447 - 0 = 0.2447

Q21 Which will reduce validation loss? MSQ: wrong option I selected was: adding more noise to training labels

Q24 True data distribution is P ~ N(2,1). Model assumes distribution Q ~ N(0,1). Calculate cross-entropy loss upto 3 decimal places.
Ans TODO

Q25 Quadratic loss L(w) = 5 w^2. Gradient descent: for what range of learning rate will weight iterations converge to w=0? Find maximum value of lr for which convergence is guaranteed?
Ans w' = (1 - 10 lr) w => -1 < 1 - 10 lr < 1 => 0 < lr < 0.2

Q26 Gradients in early layers shrink exponentially with depth but training loss still decreases.
Expected MCQ option: Effective depth of network is reduced.

Q28 scalar network: x -- w1 --> z -- ReLU --> a1 -- w2 --> z2 -- tanh --> y
x=-1, w1=2, w2=3, dL/dy = 4. Calculate dL/dw1.
Ans z = -2, so a1 = 0 (relu), so gradient = 0

Q30 re fully-connected network, parallel computations, select correct. MSQ: wrong option I selected was: increasing depth always increases expressivity.

Q31 an over-parameterized linear regression model, zero training error & least-squares solution. When optimized using gradient descent initialized at 0, which solution does it converge to?
Expected Ans: solution with smallest L2 norm

Q35 MSQ: right option I did not select was: AdaGrad has different effective learning rate for each parameter.

Q36 N training samples, mini-batch gradient descent (batch size B, n epochs). Each mini-batch (forward + backward pass) takes b seconds.
N = 50,000, B = 100, n = 20, b = 0.25 seconds. Total training time in seconds?
Ans Nnb/B = 50,000 * 20 * 0.25 / 100 = 2500

Q40 Gradient descent of loss L = 1/2 alpha w^2 with update wn = wn-1 - lr alpha w. For which range does loss converge to 0?
Ans w' = (1 - alpha * lr) w => -1 < 1 - alpha * lr < 1 => 0 < alpha * lr < 2
--------- 

## Expected Answers:

A9: 2.047, 2.052
A12: 36
A19: 0.245
A24: 3.419
A25: 0.2
A28: 0
A36: 2500
A40: 0 < lr * alpha < 2