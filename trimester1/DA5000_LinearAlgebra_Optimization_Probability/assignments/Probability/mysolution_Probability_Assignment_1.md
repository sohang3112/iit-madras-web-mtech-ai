---
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

# DA5000: Probability: Assignment 1

Name: Sohang Chopra, Roll Number: DA25M622

## Problem 1

At least one half of an airplanes engines are required to function in
order for it to operate, if each engine functions with probability $p$,
for what values of $p$ is a 4 engine plane more likely to operate than
a 2 engine plane ?

### Solution 1

This is a case of **Binomial Distribution** as each engine works with independent Bernoulli probability $p$.

1. In case of a 2-engine airplane: 

P(at least half of engines (1 out of 2) working) = 1 - P(both engines failing) = $1 - (1-p)^2$

2. In case of a 4-engine airplane:

P(at least half of engines (2 out of 4) working) = 1 - P(0 engines working) - P(1 engine working) 

Calculating:

$$P = 1 - {4\choose 0} p^0 (1-p)^4 - {4 \choose 1} p^1 (1-p)^3 = 1 - (1-p)^4 - 4p(1-p)^3$$

So:

$$
P(\text{4-engine case}) > P(\text{2-engine case}) \\
\implies 1 - (1-p)^4 - 4p(1-p)^3 > 1 - (1-p)^2 \\
\implies (1-p)^2 + 4p(1-p) < 1 \\
\implies -3p^2 + 2p < 0 \\
\implies 3p - 2 < 0
$$

Therefore `p > 2/3` is the engine probability for which a 4-engine airplane is more likely to operate than a 2-engine airplane.


## Problem 2

Assuming that the length of the phone calls in minutes is an
exponential RV with lambda = 0.1. If someone arrives at a phone
booth just before you arrive, find the probability that you will have
to wait
1. Less than 5 minutes
2. Between 5 to 10 minutes

### Solution 2

This is an **Exponential Distribution** with $\lambda = 0.1$ (it's given in the question).

Cumulative Distribution Function (CDF) is $1 - e^{-\lambda x}$ (probability of waiting less than or equal to $x$ waiting time).

1. P(less than 5 minutes) = $1 - e^{-0.1 \times 5} = 0.3935$
2. P(between 5 to 10 minutes) = $(1 - e^{-0.1 \times 10}) - (1 - e^{-0.1 \times 5}) = e^{-0.5} - e^{-1} = 0.2387$


## Problem 3

An automated optical inspection (AOI) machine is scanning a
production line of Printed Circuit Boards (PCBs). Based on
historical data, the probability that a single PCB is defective
(misaligned component or soldering error) is $p = 0.04$ (or 4%).
The inspection of each board is an independent event. Let $X$ be
the random variable representing the number of PCBs inspected up
to and including the first defective one found.
1. What is the probability that the first defective PCB found is
exactly the 10th board inspected?
2. What is the probability that the machine inspects more than
20 boards before finding the first defect?
3. On average, how many boards must the QA engineer expect
to inspect to find a single defect?

### Solution 3

This is a **Geometric Distribution**.

1. P(10th PCB is first defective one) = $(1-p)^9 p = (1-0.04)^9 0.04 = 0.0277$

2. P(more than 20 boards inspected before first defect) = $\sum_{k=21}^\infty (1-p)^{k-1} p = p \sum_{k=21}^\infty (1-p)^{k-1}$

This is an infinite geometric series. Sum of an Infinite Geometric Progression series is $\frac{a}{1-r}$ where $a$ is initial term, $r$ is geometric ratio.

So Probab = $p \frac{(1-p)^{20} p}{1 - (1-p)} = (1-p)^{20} = 0.442$

3. E(no. of boards to inspect to find a single defect) = mean of Geometric $1 / p = 1 / 0.04 = 25$


## Problem 4

A communication system transmits the digits 0 and 1. Due to noise, the digit is
incorrectly received with probability 0.2. Suppose that repetition coding is used
to reduce the error, in which five 1’s are transmitted in place of 1 and five 0’s
are transmitted in place of 0. Majority decoding is used at the receiver. What is
the probability that the message will be incorrectly decoded?

### Solution 4

This is **Binomial Distribution**, with each individual Bernoulli trial having P(wrong digit): $p = 0.2$

P(majority digits wrong (>= 3 out of 5)) is:

$${5 \choose 3} 0.2^3 (1-0.2)^2 + {5 \choose 4} 0.2^4 (1-0.2)^1 + {5 \choose 5} 0.2^5 (1-0.2)^0 = 0.05792$$


## Problem 5

Let X be a random variable exponentially distributed with parameter $lambda > 0$. If
$5 E(X) = Var(X)$, where $E(X)$ and $Var(X)$ denote the expectation and variance
of $X$, find the value of $\lambda$.

### Solution 5

In **Exponential Distribution**, $E(X) = 1 / \lambda$, $Var(X) = 1 / \lambda^2$

So, $5 / \lambda = 1 / \lambda^2 \implies \lambda = 1 / 5$


## Problem 6

Compare the Poisson approximation with the correct Binomial probability for
the following cases:
1. P (X = 2) when n = 10, p = 0.1
2. P (X = 0) when n = 10, p = 0.1
3. P (X = 4) when n = 9, p = 0.2

### Solution 6

For $n$ total events (each bernoulli trial having probability $p$), probability of $x$ successful events is: 
* Binomial: ${n \choose x} p^x (1-p)^{n-x}$
* Poisson: $\frac{\lambda^x e^{-\lambda}}{x!}$ where $\lambda = n p$

Each case calculated:

1. P (X = 2) when n = 10, p = 0.1
    * Binomial: $P = {10 \choose 2} 0.1^2 (1-0.1)^{10-2} = 45 * 0.01 * 0.9^8 = 0.1937$
    * Poisson ($\lambda = 10 \times 0.1 = 1$): $P = \frac{1^2 e^{-1}}{2!} = \frac{1}{2e} = 0.1839$

2. P (X = 0) when n = 10, p = 0.1
    * Binomial: $P = {10 \choose 0} 0.1^0 (1-0.1)^{10-0} = 0.9^10 = 0.3486$
    * Poisson ($\lambda = 10 \times 0.1 = 1$): $P = \frac{1^0 e^{-1}}{0!} = \frac{1}{e} = 0.3678$

3. P (X = 4) when n = 9, p = 0.2
    * Binomial: $P = {9 \choose 4} 0.2^4 (1-0.2)^5 = 126 * 0.2^4 * 0.8^5 = 0.066$
    * Poisson ($\lambda = 9 \times 0.2 = 1.8$): P = 1.8^4 * e^(-1.8) / 4! = 0.072