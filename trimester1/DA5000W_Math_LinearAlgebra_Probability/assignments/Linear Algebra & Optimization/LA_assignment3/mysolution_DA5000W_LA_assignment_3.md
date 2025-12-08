---
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

# DA5000 Linear Algebra Assignment 3

**Name: Sohang Chopra, Roll Number: DA25M622**

## Question 1

The floor $V$ and the wall $W$ are not orthogonal subspaces, because they share a non-zero
vector (along the line where they meet). No plane $V$ and $W$ in $\mathbb{R}^3$ can be orthogonal. Find a
vector in the column spaces of both matrices such that this will be a vector $A \mathbf{x}$ and also $B \mathbf{\hat{x}}$.
Think 3X4 matrix [A B]

### Solution 1

NOTE: Here $\times$ denotes vector cross product.

Let $\mathbf{c}$ be common vector in column spaces of $A$, $B$.

- $A = [\mathbf{v} \mathbf{w}], B=[\mathbf{a} \mathbf{b}] (\mathbf{v}, \mathbf{w}, \mathbf{a}, \mathbf{b} \in \mathbb{R}^3)$
- $\mathbf{c} = (v \times w) \times (a \times b)$: c vector lies in both planes, so it is perpendicular to normal vectors of both planes
- $\mathbf{x} = ([\mathbf{v} \mathbf{w}])^\dagger c, \hat{\mathbf{x}} = ([\mathbf{a} \mathbf{b}])^{\dagger} \mathbf{c}$
- $A \mathbf{x} = B \mathbf{\hat{x}} = \mathbf{c}$: solve for coefficients


## Question 2

Suppose there are eight vectors $\mathbf{r_1}$, $\mathbf{r_2}, \mathbf{n_1}, \mathbf{n_2}, \mathbf{c_1}, \mathbf{c_2}, \mathbf{l_1}, \mathbf{l_2} \in \mathbb{R}^4$.

1. What are the conditions for those pairs to be bases for the four fundamental subspaces of a $4 \times 4$ matrix?
2. What is one possible matrix $A$ ?

### Solution 2

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

Project the vector $\mathbf{b}$ onto the line through $\mathbf{a}$. Check the error vector $\mathbf{e}$ is perpendicular to $\mathbf{a}$.

1. $b = \begin{pmatrix} 1 \\ 2 \\ 2 \end{pmatrix}$ and $a = \begin{pmatrix} 1  \\ 1  \\ 1 \end{pmatrix}$
2. $b = \begin{pmatrix} 1 \\ 3 \\ 1 \end{pmatrix}$ and $a = \begin{pmatrix} -1 \\ -3 \\ -1 \end{pmatrix}$

### Solution 3

Calculating projected vector $\mathbf{\hat{b}} = \frac{\mathbf{a} \cdot \mathbf{b}}{ |\mathbf{a}| |\mathbf{b}| }$ 
and its error vector $\mathbf{e} = \mathbf{\hat{b}} - \mathbf{b}:

1.
$$
\mathbf{\hat{b}} = \frac{1*1 + 2*1 + 2*1}{\sqrt{1^2 + 2^2 + 2^2} \sqrt{1^2 + 1^2 + 1^2}} \mathbf{a} = \frac{5}{3} \begin{pmatrix} 1 \\ 1 \\ 1 \end{pmatrix} \\
\mathbf{e} = \frac{1}{3} \begin{pmatrix} -2 \\ 1 \\ 1 \end{pmatrix}
$$

$\mathbf{e} \cdot \mathbf{a} = 0$, so the error vector $\mathbf{e}$ is perpendicular to $\mathbf{a}$.

2.
$$
\mathbf{\hat{b}} = \frac{1*(-1) + 3*(-3) + 1*(-1)}{\sqrt{1^2 + 3^2 + 1^2} \sqrt{(-1)^2 + (-3)^2 + (-1)^2}} \mathbf{a} = \begin{pmatrix} 1 \\ 3 \\ 1 \end{pmatrix} \\
\mathbf{e} = \begin{pmatrix} 1 \\ 3 \\ 1 \end{pmatrix} - \begin{pmatrix} 1 \\ 3 \\ 1 \end{pmatrix} = 0
$$

Error vector is $0$ because $\mathbf{b}$ lies along $\mathbf{a}$, so it's perpendicular to $\mathbf{a}$.


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

Find orthonormal vectors $\mathbf{A}$, $\mathbf{B}$, $\mathbf{C}$ by Gram-Schmidt method from $\mathbf{a}$, $\mathbf{b}$, $\mathbf{c}$:

$$
\mathbf{a} = \begin{pmatrix} 1 \\ −1 \\ 0 \\ 0 \end{pmatrix}, 
\mathbf{b} = \begin{pmatrix} 0 \\ 1 \\ −1 \\ 0 \end{pmatrix}, 
\mathbf{c} = \begin{pmatrix} 0 \\ 0 \\ 1 \\ −1 \end{pmatrix}
$$

Prove that $A$, $B$, $C$ are bases for the vector perpendicular to $\mathbf{d} = \begin{pmatrix} 1 & 1 & 1 & 1 \end{pmatrix}$.

### Solution 5

Vector Magnitudes are:

$$|\mathbf{a}| = |\mathbf{b}| = |\mathbf{c}| = \sqrt{2}$$

$$
\mathbf{A} = \mathbf{a} = \begin{pmatrix} 1 \\ −1 \\ 0 \\ 0 \end{pmatrix}, \mathbf{A} = \sqrt{2} \\

\mathbf{B} = \begin{pmatrix} 0 \\ 1 \\ −1 \\ 0 \end{pmatrix} - \frac{1*0 + (-1)*1 + 0*(-1) + 0*0}{ \sqrt{2} \sqrt{2} } \begin{pmatrix} 1 \\ −1 \\ 0 \\ 0 \end{pmatrix}
           = \begin{pmatrix} 1/2 \\ 1/2 \\ -1 \\ 0 \end{pmatrix}
, |\mathbf{B}| = \sqrt{3/2} \\

\mathbf{C} = \begin{pmatrix} 0 \\ 0 \\ 1 \\ −1 \end{pmatrix} - \frac{1*0 + (-1)*0 + 0*1 + 0*(-1)}{ \sqrt{2} \sqrt{2} } \begin{pmatrix} 1 \\ −1 \\ 0 \\ 0 \end{pmatrix}
                                                             - \frac{(1/2)*0 + (1/2)*0 + (-1)*1 + 0*(-1)}{ \sqrt{2} \sqrt{3/2} } 
                                                               \begin{pmatrix} 1/2 \\ 1/2 \\ -1 \\ 0 \end{pmatrix}
           = \begin{pmatrix} 1/3 \\ 1/3 \\ 1/3 \\ -1 \end{pmatrix},
|\mathbf{C}| = 2 / \sqrt{3}
$$

Dividing by magnitudes to get final orthonormal vectors:

$$
\mathbf{A} = 1 / \sqrt{2} \begin{pmatrix} 1 \\ −1 \\ 0 \\ 0 \end{pmatrix},
\mathbf{B} = 1 / \sqrt{6} \begin{pmatrix} 1 \\  1 \\ -2 \\ 0 \end{pmatrix},
\mathbf{C} = 2 / \sqrt{3} \begin{pmatrix} 1/3 \\ 1/3 \\ 1/3 \\ -1 \end{pmatrix}
$$

Checking orthogonality of each with $\mathbf{d} = \begin{pmatrix} 1 & 1 & 1 & 1 \end{pmatrix}$:

$$
\mathbf{A} \cdot \mathbf{d} = 0
\mathbf{B} \cdot \mathbf{d} = 0
\mathbf{C} \cdot \mathbf{d} = 0
$$

As $\mathbf{d}$ is perpendicular to each, and $\mathbf{A}$, $\mathbf{B}$, $\mathbf{C}$ are all ortho-normal, 
therefore $A$, $B$, $C$ are bases for the vector perpendicular to $\mathbf{d}$.
Hence proved.


## Question 6: 

Let $\mathbf{a} = (1, 2, −1), \mathbf{b} = (2, −1, 1), \mathbf{c} = (3, 1, 0) \in \mathbb{R}^3$.
Check which pairs among $\mathbf{a}, \mathbf{b}, \mathbf{c}$ are orthogonal.

### Solution 6

$$\mathbf{a} \cdot \mathbf{b} = -1, \mathbf{b} \cdot \mathbf{c} = 5, \mathbf{c} \cdot \mathbf{a} = 5$$

All dot products are non-zero, so none of the pairs are orthogonal.


## Question 7:

Let $\mathbf{v_1} = (1,1,0), v2 = (1,0,1), v3 = (0,1,1) \in \mathbb{R}^3$. 
Use the Gram–Schmidt process to compute an orthonormal basis ${\mathbf{e_1}, \mathbf{e_2}, \mathbf{e_3}}$ for $span \{ \mathbf{v_1}, \mathbf{v_2}, \mathbf{v_3} \}$.

### Solution 7

$$
\mathbf{e_1} = (1,1,0), |\mathbf{e_1}| = \sqrt{2} \\

\mathbf{e_2} = (1,0,1) - \frac{1*1 + 1*0 + 0*1}{\sqrt{2} \sqrt{2}} (1,1,0) = (1/2, -1/2, 1),
|\mathbf{e_2} = \sqrt{3/2} \\

\mathbf{e_3} = (0,1,1) - \frac{1*0 + 1*1 + 0*1}{\sqrt{2} \sqrt{2}} (1,1,0) - \frac{0*1/2 + 1*(-1/2) + 1*1}{\sqrt{2} \sqrt{3/2}} = (-0.644,  0.356,  0.711) (approx),
|\mathbf{e_3}| = 1.023 (approx)
$$

Dividing by magnitudes to get final orthnormal vectors:

$$
\mathbf{e_1} = \frac{1}{\sqrt{2}} (1,1,0) \\
\mathbf{e_2} = \frac{1}{\sqrt{6}} (1,-1,2) \\
\mathbf{e_3} = \frac{1}{\sqrt{3}} (-1,1,1)
$$


## Question 8:

Application of least squares for the regression problem.

Using the provided laptop price dataset *laptop_price_small.csv*, apply Least squares method to predict the
laptop price using the laptop features:

1. Code least squares method.
2. Identify and mention the input features (X) and target variable (Y).
3. Print the equation of the fitted hyperplane.
4. Print the Mean Squared Error (MSE) which is, $\sum_{i=1}^N (Y_i - pred(X_i))^2$.
5. Interpret the fitted hyperplane and write about your observation of the relationship between the input variables and output.

Code submission guidelines:

1. Prepare your assignment exclusively in a Jupyter Notebook (.ipynb format).
2. Ensure all code cells are executed and their corresponding outputs are visible.
3. Name the notebook as following: `{Rollnumber}_LA_MFDS_Assignment_3.ipynb`

### Solution 8

Code solution for Q8 has been submitted in seperate file `DA5000W_LA_MFDS_Assignment_3.ipynb`.
