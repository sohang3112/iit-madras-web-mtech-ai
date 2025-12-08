# DA5000 Linear Algebra Assignment 3

## Question 1

The floor $V$ and the wall $W$ are not orthogonal subspaces, because they share a non-zero
vector (along the line where they meet). No plane $V$ and $W$ in $R^3$ can be orthogonal. Find a
vector in the column spaces of both matrices such that this will be a vector $A \mathbf{x}$ and also B ˆx.
Think 3X4 matrix [A B]

### Solution 1

TODO: DIDN'T FULLY UNDERSTAND QUESTION!!


## Question 2

Suppose there are eight vectors $\mathbf{r_1}$, $\mathbf{r_2}, \mathbf{n_1}, \mathbf{n_2}, \mathbf{c_1}, \mathbf{c_2}, \mathbf{l_1}, \mathbf{l_2} \in R^4$.

1. What are the conditions for those pairs to be bases for the four fundamental subspaces of a $4 \times 4$ matrix?
2. What is one possible matrix $A$ ?

### Solution 2

TODO: VERIFY MY SOLUTION

1. 2 vectors each form bases for 4 fundamental subspaces (row space, null space, column space, left null space) of $4 \times 4$ matrix (given).
   So nullity (dimension of null space) and rank (dimension of column space) are both 2, and the matrix is linearly dependent.

2. One possible such matrix $A$ is:

$$\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0
\end{bmatrix}$$


## Question 3

Project the vector $b$ onto the line through $a$. Check the error vector $e$ is perpendicular to $a$.

1. $b = \begin{pmatrix} 1 \\ 2 \\ 2 \end{pmatrix}$ and $a = \begin{pmatrix} 1  \\ 1  \\ 1 \end{pmatrix}$
2. $b = \begin{pmatrix} 1 \\ 3 \\ 1 \end{pmatrix}$ and $a = \begin{pmatrix} -1 \\ -3 \\ -1 \end{pmatrix}$

### Solution 3

TODO - question unclear, what do they mean by line through vector a?? do they mean line joining origin (0) with a??


## Question 4:
Find orthonormal vectors $q_1$, $q_2$, $q_3$ such that $q_1$, $q_2$ span the column space of

$$A = \begin{bmatrix}
 1 &  1 \\
 2 & −1 \\
−2 &  4
\end{bmatrix} $$

Which of the four fundamental subspaces contains $q_3$?

### Solution 4

Row-Reducing $A$ to find RREF form:

* $R_1 -> R_1 - R_2$ and $R_3 -> R_3 - 5 R_2$ :

$$\begin{bmatrix}
 1 &  1 \\
 2 & -1 \\
-2 &  4
\end{bmatrix}$$

* $R_2 -> -1/3 R_2$ :

$$\begin{bmatrix}
1 & 1 \\
0 & 1 \\
0 & 5
\end{bmatrix}$$

* $R_1 -> R_1 - R_2$ and $R_3 -> R_3 - 5 R_2$ :

$$\begin{bmatrix}
1 & 0 \\
0 & 1 \\
0 & 0
\end{bmatrix}$$

Columns of RREF matrix are orthogonal (dot product is 0) and have unit magnitude.
So $\mathbf{q_1} = \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix}$ 
and $\mathbf{q_2} = \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix}$ are orthonormal basis vectors of column space of $A$.

Vectors in Null Space are orthogonal to column space, so $\mathbf{q_3}$ must lie in Null Space.

Solving for Null Space (let coordinates of $\mathbf{q_3}$ be $x$, $y$, $z$):

$$
\begin{bmatrix}
1 & 0 \\
0 & 1 \\
0 & 0 \end{bmatrix}
\begin{bmatrix} x \\ y \\ z \end{bmatrix}
=
\begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}
$$

$x = 0$, $y = 0$ and $z$ is a free variable. 
So basis of Null Space is vector $\mathbf{q_3} = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$.


## Question 5:

Find orthonormal vectors $\mathbf{A}$, $\mathbf{B}$, $\mathbf{C}$ by **Gram-Schmidt method** from $\mathbf{a}$, $\mathbf{b}$, $\mathbf{c}$:

$$
\mathbf{a} = \begin{pmatrix} 1 \\ −1 \\ 0 \\ 0 \end{pmatrix}, 
\mathbf{b} = \begin{pmatrix} 0 \\ 1 \\ −1 \\ 0 \end{pmatrix}, 
\mathbf{c} = \begin{pmatrix} 0 \\ 0 \\ 1 \\ −1 \end{pmatrix}
$$

Prove that $A$, $B$, $C$ are bases for the vector perpendicular to $d = \begin{pmatrix} 1 & 1 & 1 & 1 \end{pmatrix}$.

### Solution 5



## Question 6: 
Let
a = (1, 2, −1), b = (2, −1, 1), c = (3, 1, 0) ∈R3.
(a) Check which pairs among a, b, c are orthogonal.
Question 7:
Let
v1 = (1, 1, 0), v2 = (1, 0, 1), v3 = (0, 1, 1)
in R3. Use the Gram–Schmidt process to compute an orthonormal basis {e1, e2, e3} for
span{v1, v2, v3}.
Question 8:
Application of least squares for the regression problem.
Using the provided laptop price dataset (Link), apply Least squares method to predict the
laptop price using the laptop features.
1. Code lease squares method.
2. Identify and mention the input features (X) and target variable (Y).
3. Print the equation of the fitted hyperplane
4. Print the Mean Squared Error (MSE) which is,
∑N
i=1(Yi−pred(Xi))2
N
5. Interpret the fitted hyperplane and write about your observation of the relationship
between the input variables and output
Code submission guidelines
1. Prepare your assignment exclusively in a Jupyter Notebook (.ipynb format).
2. Ensure all code cells are executed and their corresponding outputs are visible.
3. Name the notebook as following: {Rollnumber} LA M F DS Assignment 3.ipynb
Page 2
