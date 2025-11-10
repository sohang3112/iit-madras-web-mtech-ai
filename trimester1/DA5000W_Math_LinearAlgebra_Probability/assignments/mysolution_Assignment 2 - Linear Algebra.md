---
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

# DA5000W — Linear Algebra and Optimization  
**Assignment 2 — October 2025**

---

## Question 1

For the following set of problems:

- Prove that $T$ is a linear transformation.  
- Find bases for both $N(T)$ and $R(T)$.  
- Compute the nullity and rank of $T$.  
- Verify the dimension theorem.  
- Determine whether $T$ is one-to-one or onto.

### (a)

$ T : \mathbb{R}^3 \to \mathbb{R}^2 $ defined by  

$$T(a_1, a_2, a_3) = (a_1 - a_2,\, 2a_3)$$

### Answer for (a)

Transform Matrix for standard basis vectors $\mathbf{e_1}$, $\mathbf{e_2}$, $\mathbf{e_3}$ is:

$$A = \begin{bmatrix}
1 & -1 & 0 \\
0 &  0 & 2
\end{bmatrix}$$

Since $T$ can be written as multiplying with this transformation matrix with input vector: $A \mathbf{x}$, 
therefore it automatically satisfies *Additive* and *Homogenity* properties, so **$T$ is a linear transform.**

**Bases of Null space $N(T)$:** solving $T(a_1, a_2, a_3) = 0$:

$$a_1-a_2=0, 2a_3=0 => a_1=a_2,\ a_3=0.$$

General solution is $(a_1,a_2,a_3)=(t,t,0)=t(1,1,0)$ (by defining a free variable $t = a_1 = a_2$).

So, Bases of Null Space: $\{(1,1,0)\}$. Nullity (dimension of null space) is $1$ since only 1 basis vector is in null space.

**Bases of Range $R(T)$:** 

Column 2 of Transformation Matrix $A$ is just negative of column 1 $\mathbf{c_2} = -\mathbf{c_1}$ so it can be removed. 
Remaining 2 column vectors are independent, so they form Bases of Range: (1,0) and (0,2).

**Dimension Theorem (aka Rank-Nullity Theorem):** $\operatorname{rank}(T)+\operatorname{nullity}(T)=2+1=3=\dim(\mathbb{R}^3)$. Verified.

**One-to-one / onto:** $T$ is not one-to-one because nullity $>0$. *It is Onto* because $\operatorname{range}=\mathbb{R}^2$ (codomain).


### (b)

$ T : \mathbb{R}^2 \to \mathbb{R}^3 $ defined by  

$$T(a_1, a_2) = (a_1 + a_2,\, 0,\, 2a_1 - a_2)$$

### Answer for (b)

Transformation Matrix (for standard bases) is:

$$
A = \begin{bmatrix}
1 &  1 \\
0 &  0 \\
2 & -2 \\
\end{bmatrix}
$$

Since $T(\mathbf{x}) = A \mathbf{x}$, **$T$ is a linear transform** as all matrix maps are linear.

**Bases of Null Space $N(T)$**: solving $T(a_1, a_2) = 0$:

$$a_1 + a_2 = 0, 0 = 0, 2a_1 - a_2 = 0 => a_2 = -a_1, a_2 = 2a_1$$

This can be satisified only by $a_1=0, a_2=0$. So Null Space has only zero vector, Bases of Null Space is empty set $\emptyset$, and Nullity = 0.

**Bases of Range Space $R(T)$**: Both columns of transform matrix $A$ are independent, so Bases of Range Space are column vectors $\{ (1,0,2), (1,0,-2) \}$. So Rank = 2.

**Dimension Theorem (aka Rank-Nullity Theorem)**: Rank (2) + Nullity (0) = No. of columns (ie no. of input variables). Hence Verified.

$T$ is **one-to-one** because nullity is 0, so inputs map to unique outputs.

### (c)

$ T : M_{2\times3}(F) \to M_{2\times2}(F) $ defined by  

$$
T\!\left(
\begin{bmatrix}
a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23}
\end{bmatrix}
\right)
=
\begin{bmatrix}
2a_{11} - a_{12} & a_{13} + 2a_{12} \\
0 & 0
\end{bmatrix}
$$

### Answer for (c)

**Proof that $T$ is a linear transform**:
Here input and output are matrices with multi-columns, so it's also a *Matrix Space*.

For 2 input matrices $A$ and $B$, $T(A+B)$ is:

$$T(A+B)=\begin{bmatrix}
2(a_{11}+b_{11})-(a_{12}+b_{12}) & (a_{13}+b_{13})+2(a_{12}+b_{12}) \\
0 & 0
\end{bmatrix} = \begin{bmatrix}
(2a_{11}-a_{12})+(2b_{11}-b_{12}) & (a_{13}+2a_{12})+(b_{13}+2b_{12}) \\
0 & 0
\end{bmatrix}
= T(A)+T(B)$$

So additivity is verified.

Let $c$ be a scalar. Compute $T(c A)$ for an input matrix $A$:

$$T(c A)=\begin{bmatrix}
2(c a_{11})-(c a_{12}) & (c a_{13})+2(c a_{12})[4pt]
0 & 0
\end{bmatrix}
=\begin{bmatrix}
c(2a_{11}-a_{12}) & c(a_{13}+2a_{12})[4pt]
0 & 0
\end{bmatrix}
=c T(A)$$

So homogeneity is verified. Therefore $T$ is a valid linear transform. Hence proved.

**Basis of Null Space $N(T)$**: Solving for $T(A) = 0$, letting free variable $t = a_{12}$:

$$2 a_{11} - a_{12} = 0, a_{13} + 2 a_{12} = 0 \implies a_{11} = t/2, a_{12} = t, a_{13} = -2t$$

So Bases of Null Space is a set with a single matrix (so *Nullity = 1*):

$$\begin{bmatrix}
1/2 & 1 & -2 \\
0   & 0 & 0
\end{bmatrix}$$

**Basis of Range Space $R(T)$**: In output second row is always 0, and elements of first row $2 a_{11} - a_{12}$, $a_{13} + 2 a_{12}$ are independent and can take any real values. So Range Space is set of all real $2 \times 2$ matrices with second row 0.

One convient bases set is:

$$
;E_{11}=\begin{bmatrix}1&0[2pt]0&0\end{bmatrix},\qquad
E_{12}=\begin{bmatrix}0&1[2pt]0&0\end{bmatrix}.
$$

Rank (dimension of $R(T)$) is 2.

**Dimension Theorem (aka Rank-Nullity Theorem)**: Rank (2) + Nullity (1) = Dimension of Domain (3). Hence verified.

$T$ is **onto** (not one-to-one) because Nullity > 0.

### (d)

$ T : P_2(\mathbb{R}) \to P_3(\mathbb{R}) $ defined by  

$$
T(f(x)) = x f(x) + f'(x)
$$

### Answer for (d)

For 2 input vectors $\mathbf{x}$, $\mathbf{y}$:

$$T(f(\mathbf{x} + \mathbf{y})) = (\mathbf{x} + \mathbf{y}) f(\mathbf{x} + \mathbf{y}) + f' (\mathbf{x} + \mathbf{y})$$

Since $f$ and $f'$ are polynomial functions, so this becomes:

$$= (\mathbf{x} f(\mathbf{x}) + f' (\mathbf{x})) + (\mathbf{y} f(\mathbf{y}) + f' (\mathbf{y}) = T(\mathbf{x}) + T(\mathbf{y})$$

This verifies additive property.

Also, for some scalar $c$:

$$T(f(c \mathbf{x})) = c \mathbf{x} f(c \mathbf{x}) + f' (c \mathbf{x}) =  c (\mathbf{x} f (\mathbf{x}) + f' (\mathbf{x})) = c T(f(\mathbf{x}))$$

This verifies homogenity property. **Hence proved that $T$ is a linear transform.**

**Bases of Null space $N(T)$** Only zero vector satisifes $T(f(\mathbf{x})) = 0$, so Nullity is 0 and Bases of Null Space is empty set $\emptyset$.

**Bases for Range $R(T)$** ${,x,;1+x^2,;2x+x^3,}$ (these three are independent and span the image).

**Rank–nullity check.** $\operatorname{rank}(T)+\operatorname{nullity}(T)=3+0=3=\dim P_2$. Verified.

**One-to-one / Onto.** $T$ is one-to-one (not onto) because Nullity = 0.

---------------------------

## Question 2

Given the set of linear equations:

$$
\begin{cases}
x + y = 2 \\
x + 2y = 3 \\
x + 3y = 4
\end{cases}
$$

1. Write in matrix form.  
2. Find the basis for the column space and the null space.  
3. Interpret these subspaces geometrically.

## Answer for Question 2

1. Matrix equation form is:

$$
\begin{bmatrix}
1 & 1 \\
1 & 2 \\
1 & 3
\end{bmatrix}
\begin{bmatrix}
x \\
y
\end{bmatrix}
=
\begin{bmatrix}
2 \\
3 \\
4
\end{bmatrix}
$$

2. For null space, $x+y=0$, $x + 2y = 0$, $x + 3y = 0$ => all these are only possible if $x = y = 0$ (zero vector). So bases of null space is empty set.

For column space, output vector is $(x+y, x+2y, x+3y)$ where both $x$ and $y$ are free variables (real numbers).

3. Geometric interpretation is that these equations represent 3 lines on a 2D plane that meet at origin $(0,0)$.

---

## Question 3

In $ \mathbb{R}^2 $, let $ L $ be the line $ y = mx $, where $ m \neq 0 $.  
Find an expression for $ T(x, y) $, where $ T $ is the reflection of $ \mathbb{R}^2 $ about $ L $.

**Hint:** Reflect by rotating the line to the x-axis, apply the reflection matrix, then rotate back.

$$
R(\theta) =
\begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}, \quad
T = R(\theta)
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
R(-\theta),
\quad \text{with } \theta = \tan^{-1}(m)
$$

## Answer for Question 3

Let $\theta=\tan^{-1}m$. The reflection matrix about the line through the origin at angle $\theta$ is
$$
T ;=; R(\theta)\begin{bmatrix}1&0[4pt]0&-1\end{bmatrix}R(-\theta)
;=;
\begin{bmatrix}\cos2\theta & \sin2\theta[4pt]\sin2\theta & -\cos2\theta\end{bmatrix}.
$$
Write $\cos2\theta$ and $\sin2\theta$ in terms of $m=\tan\theta$:
$$
\cos2\theta=\frac{1-m^2}{1+m^2},\qquad
\sin2\theta=\frac{2m}{1+m^2}.
$$
Thus the linear map (T:\mathbb R^2\to\mathbb R^2) (reflection about (y=mx)) has matrix
$$
T=\frac{1}{1+m^2}\begin{bmatrix}1-m^2 & 2m[6pt]2m & m^2-1\end{bmatrix},
$$
and for any point ((x,y)),
$$
T(x,y)=\left(\frac{(1-m^2)x+2m y}{1+m^2},;\frac{2m x+(m^2-1)y}{1+m^2}\right).
$$

---

## Question 4

For each of the following matrices $ A \in M_{n\times n}(\mathbb{R}) $:

1. Test $ A $ for diagonalizability.  
2. Find an invertible matrix $ Q $ and a diagonal matrix $ D $ such that  
   $ Q^{-1} A Q = D $.

$$
A_1 =
\begin{bmatrix}
1 & 3 \\
3 & 1
\end{bmatrix},
\quad
A_2 =
\begin{bmatrix}
1 & 1 & 0 \\
0 & 1 & 2 \\
0 & 0 & 3
\end{bmatrix},
\quad
A_3 =
\begin{bmatrix}
3 & 1 & 1 \\
2 & 4 & 2 \\
-1 & -1 & 1
\end{bmatrix}
$$

Perform the calculations for $ A_1, A_2, $ and $ A_3 $.

## Answer for Question 4

After calculation we get these for each of the above:

$$
A_1 = \begin{pmatrix}1 & 3 \ 3 & 1\end{pmatrix}
\Rightarrow
\text{Eigenvalues: } -2,, 4;\
\text{Eigenvectors: }
v_{-2}=\begin{pmatrix}-1\\1\end{pmatrix},\
v_{4}=\begin{pmatrix}1\\1\end{pmatrix};\
Q_1=\begin{pmatrix}-1&1\\1&1\end{pmatrix},
D_1=\begin{pmatrix}-2&0\\0&4\end{pmatrix}.
$$

$$
A_2 = \begin{pmatrix}1 & 1 & 0 \\ 0 & 1 & 2 \\ 0 & 0 & 3\end{pmatrix}
\Rightarrow
\text{Eigenvalues: } 1\\ (\text{mult. }2),\\ 3;\
\text{Eigenvectors: }
v_{1}=\begin{pmatrix}1\\0\\0\end{pmatrix},
v_{3}=\begin{pmatrix}\tfrac{1}{2}\\1\\1\end{pmatrix};
\text{Not diagonalizable.}
$$

$$
A_3 = \begin{pmatrix}3 & 1 & 1 \\ 2 & 4 & 2 \\ -1 & -1 & 1\\ \end{pmatrix}
\Rightarrow
\text{Eigenvalues: } 2\\ (\text{mult. }2),\\ 4;\
\text{Eigenvectors: }
v_{2}^{(1)}=\begin{pmatrix}-1\\1\\0\\ \end{pmatrix},
v_{2}^{(2)}=\begin{pmatrix}-1\\0\\1\\ \end{pmatrix},
v_{4}=\begin{pmatrix}-1\\-2\\1\\ \end{pmatrix};
Q_3=\begin{pmatrix}-1&-1&-1\\1&0&-2\\0&1&1\\\end{pmatrix},
D_3=\begin{pmatrix}2&0&0\\0&2&0\\0&0&4\\\end{pmatrix}.
$$

---

## Question 5

### (a)

A $ 2 \times 2 $ symmetric matrix has eigenvectors $ v_1 $ and $ v_2 $, corresponding to two distinct eigenvalues.  
Find the value of $ a $, given:

$$
v_1 =
\begin{bmatrix}
2 \\
4
\end{bmatrix},
\quad
v_2 =
\begin{bmatrix}
8 \\
-a
\end{bmatrix}
$$

### (b)

You are given a $ 3 \times 3 $ matrix $ A $ with the following properties:

- $ \text{trace}(A) = 4 $
- $ \det(A) = -18 $
- One eigenvalue $ \lambda_1 = -2 $

Also, $ A $ acts on a specific vector $ v $ as follows:

$$
A
\begin{bmatrix}
1 \\ 0 \\ 1
\end{bmatrix}
=
\begin{bmatrix}
3 \\ 0 \\ 3
\end{bmatrix}
$$

Answer the following:

1. What are the other two eigenvalues of $ A $?  
2. What is the result of $ A^5 v $ (where $ v $ is the vector above)?

### (c)
Is the matrix $$ (A - 3I) $$ invertible? Justify your answer.

## Answer for Question 5

# (a)

For a real symmetric matrix eigenvectors for distinct eigenvalues are orthogonal, so $v_1\cdot v_2=0$.

$v_1\cdot v_2 = 2\cdot 8 + 4\cdot(-a) = 16 - 4a.$

Setting it (dot product simplified) equal to zero: $16-4a=0.$ . So **$a = 4$$**.

# (b)

Let the other two eigenvalues be $\lambda_2,\lambda_3$.
Sum: $\lambda_1+\lambda_2+\lambda_3 = 4 \Rightarrow -2+\lambda_2+\lambda_3=4$ so $\lambda_2+\lambda_3=6.$
Product: $\lambda_1\lambda_2\lambda_3=-18 \Rightarrow (-2)\lambda_2\lambda_3=-18$ so $\lambda_2\lambda_3=9.$

The quadratic with roots $\lambda_2,\lambda_3$ is $t^2-(\lambda_2+\lambda_3)t+\lambda_2\lambda_3 = t^2-6t+9=(t-3)^2.$

Also from $A v=3v$ we see $v$ is an eigenvector with eigenvalue $3$, so $3$ is indeed an eigenvalue.

So:
* The other two eigenvalues are $\lambda_2=\lambda_3=3.$
* Since $A v=3v$, $A^5 v = 3^5 v = 243,v = \begin{bmatrix}243\\0\\243\end{bmatrix}.$

---

# (c)

From (b) we have eigenvalues (-2,3,3). The matrix $A-3I$ has eigenvalues $\lambda_i-3$, i.e. $-2-3=-5$ and $3-3=0$ (twice).

One eigenvalue of $A-3I$ is $0$, so $A-3I$ has determinant $= (-5)\cdot 0\cdot 0=0.$

$A-3I$ is **not invertible** (singular), because it has zero as an eigenvalue (equivalently its determinant is 0).


---

## Question 6
An agricultural model tracks the yearly populations of three interacting species: Wheat (W), Weevil (V), and a specialist Fungus (F).  
The population vector is  

$$
x_k =
\begin{bmatrix}
W_k \\
V_k \\
F_k
\end{bmatrix}
$$

and its evolution is governed by  

$$
x_{k+1} = A x_k
$$

where the interaction matrix $A$ is given by:

$$
A =
\begin{bmatrix}
4 & 0 & 0 \\
1 & 3 & 0 \\
2 & 1 & 2
\end{bmatrix}
$$

Your task is to analyze the long-term dynamics of this system:

1. Find the eigenvalues $\lambda$ of the matrix $A$.  
2. Find the corresponding eigenvectors $$ v $$ for each eigenvalue.  
3. **Follow-up:** The model matrix $$ A $$ is diagonalizable. Explain the significance of the matrix $P$ in the diagonalization $A = P D P^{-1}$, and what this factorization reveals about predicting the population $x_k$ after many years ($k \to \infty$).

## Answer for Question 6

Matrix triangular off the diagonal so its eigenvalues are the diagonal entries.
Eigenvalues: $; \lambda_1=4,; \lambda_2=3,; \lambda_3=2.$

Solve $(A-\lambda I)v=0$ for each $\lambda$:

* For $\lambda=4$:
  integer eigenvector: $v^{(1)}=(2,2,3)^\top$.

* For (\lambda=3):
  Eigenvector $v^{(2)}=(0,1,1)^\top$.

* For $\lambda=2$:
  Eigenvector: (v^{(3)}=(0,0,1)^\top).

$P$ is the change-of-basis matrix from the standard population coordinates to the eigenbasis. Diagonalization separates the dynamics into independent scalar scalings by the eigenvalues. That is why powers are easy to compute and why long-term prediction reduces to keeping the dominant eigenmode.

---

## Answer for Question 7

# (a) Concept & what the singular values mean

Because $\sigma_1,\sigma_2,\sigma_3$ are orders of magnitude larger than the others, a rank-3 approximation will retain almost all visible structure of the image; the discarded singular values contribute very little energy.

# (b) Storage counts and compression ratio

**Data / facts used**

* Original matrix (A) stores one number per pixel: (512\times512=262{,}144) numbers.
* Rank-(k) SVD approximation (A_k=\sum_{i=1}^k \sigma_i u_i v_i^T) can be stored by keeping:

  * (U_k) : (512\times k) entries,
  * (V_k) : (512\times k) entries,
  * (\Sigma_k) : (k) singular values.
* So total stored numbers for (A_k) = (512k + 512k + k = k(512+512+1)=k\cdot1025.)

**Summary (numbers for (k=3))**

* Original: (262{,}144) numbers.
* Rank-3 storage: (k\cdot1025 = 3\cdot1025 = 3{,}075) numbers.
* Compression ratio (original storage : compressed storage)
  (\displaystyle \frac{262{,}144}{3{,}075}\approx 85.25.)
* Relative storage reduction (=1-\frac{3{,}075}{262{,}144}\approx 98.83%) (i.e., only ≈1.17% of the original numbers are kept).

**Extra quantitative check (how much image energy the first 3 singular values capture)**

* Sum of squares of first three singular values:
  (15{,}000^2+8{,}000^2+3{,}000^2=298{,}000{,}000.)
* Upper bound on remaining squared energy (using given (\sigma_4,\sigma_5) plus the worst-case bound (\sigma_i^2\le 50^2) for the remaining (512-5=507) singular values):
  (500^2+200^2+507\cdot50^2 = 1{,}557{,}500.)
* Thus the first three singular values account for at least
  (\dfrac{298{,}000{,}000}{298{,}000{,}000+1{,}557{,}500}\approx 0.9948) → **≈99.48%** of the image energy (Frobenius-norm energy).
* The Frobenius-norm of the approximation error is therefore at most (\sqrt{1{,}557{,}500}\approx1{,}248) (absolute error in Frobenius norm), which is tiny relative to the image energy.

**Conclusion**

* Storing (A_3) requires only (3{,}075) numbers versus (262{,}144) for the full image, a compression ratio of about **85.25:1** (≈98.8% fewer numbers).
* Because the first three singular values carry ≳99.48% of the total energy, the rank-3 approximation will be visually excellent: most structure preserved, only very small fine details/noise lost.

---

## Question 8
Let  

$$
A_1 =
\begin{bmatrix}
1 & 1 & 0 \\
0 & 1 & 1
\end{bmatrix}, \quad
A_2 =
\begin{bmatrix}
-2 & 8 & 20 \\
14 & 19 & 10 \\
2 & -2 & 1
\end{bmatrix}
$$

1. Compute $$ A^T A $$ and $$ A A^T $$.  
2. Find their eigenvalues and **unit eigenvectors**.  
3. Construct the **singular value decomposition** $$ A = U \Sigma V^T $$.  
4. Multiply $$ U \Sigma V^T $$ to recover $$ A $$.

Perform the calculation for **both** $$ A_1 $$ and $$ A_2 $$.

## Answer for Question 8

Nice linear-algebra workout — I computed everything numerically and verified the reconstructions. Below I summarize the computed data (matrices, eigenpairs, SVD components) and the conclusions; the full numeric output was produced by the code cell above.

# Data (computed)

**For (A_1=\begin{bmatrix}1&1&0[4pt]0&1&1\end{bmatrix}) (shape (2\times3))**

* (A_1^T A_1 = \begin{bmatrix}1&1&0[4pt]1&2&1[4pt]0&1&1\end{bmatrix}.)

  * Eigenvalues (descending): (;[3,;1,;0]).
  * Corresponding unit eigenvectors (columns):
    [
    V_{A_1} =
    \begin{bmatrix}
    0.40824829 & 0.70710678 & -0.57735027[4pt]
    0.81649658 & 0.0        &  -0.57735027[4pt]
    0.40824829 & -0.70710678 & -0.57735027
    \end{bmatrix}.
    ]
    (These are unit vectors; the 3rd eigenvalue is 0 so its eigenvector spans the nullspace.)

* (A_1A_1^T = \begin{bmatrix}2&1[4pt]1&2\end{bmatrix}.)

  * Eigenvalues: ([3,;1]).
  * Corresponding unit eigenvectors (columns) = left singular vectors (U_{A_1}):
    [
    U_{A_1}=\begin{bmatrix} ;0.70710678 & -0.70710678[4pt] ;0.70710678 & ;0.70710678 \end{bmatrix}.
    ]

* Singular values (from SVD) are (\sigma_1=\sqrt{3}\approx1.73205081,; \sigma_2=1,; \sigma_3=0.)

* SVD components:

  * (U_{A_1}) as above (2×2),
  * (\Sigma_{A_1}) (2×3) with diagonal entries (\sqrt{3},1),
  * (V_{A_1}^T) equals the transpose of the eigenvector matrix for (A_1^T A_1) (3×3).

* Reconstruction check: (A_1 - U\Sigma V^T) has Frobenius norm ≈ (1.1\times10^{-16}) (numerical zero).

---

**For (A_2=\begin{bmatrix}-2&8&20[4pt]14&19&10[4pt]2&-2&1\end{bmatrix}) (shape (3\times3))**

* (A_2^T A_2) and (A_2A_2^T) were computed (symmetric (3\times3) matrices).

  * Singular values (SVD) are ([30,;15,;3]).
  * Therefore eigenvalues of (A_2^T A_2) (and of (A_2A_2^T)) are the squares: ([900,;225,;9]).

* Right singular vectors (columns of (V)) — from the SVD (numerical values):
  [
  V_{A_2} =
  \begin{bmatrix}
  0.33333333 & 0.66666667 & 0.66666667[4pt]
  0.66666667 & 0.33333333 & -0.66666667[4pt]
  0.66666667 & -0.66666667 & 0.33333333
  \end{bmatrix}.
  ]
  (These are unit vectors and are eigenvectors of (A_2^T A_2).)

* Left singular vectors (columns of (U)) from the SVD:
  [
  U_{A_2} =
  \begin{bmatrix}
  0.8 & -0.6 & 0.0[4pt]
  0.6 & 0.8 & 0.0[4pt]
  0.0 & 0.0 & 1.0
  \end{bmatrix}.
  ]

* (\Sigma_{A_2} = \operatorname{diag}(30,15,3)) (3×3).

* Reconstruction check: (A_2 - U\Sigma V^T) has Frobenius norm ≈ (1.16\times10^{-14}) (numerical zero).

# Summary of relationships (concise)

* Eigenvalues of (A^T A) are the squares of the singular values. For (A_1): ([3,1,0]=[\sigma_1^2,\sigma_2^2,\sigma_3^2]). For (A_2): ([900,225,9]=[30^2,15^2,3^2]).
* Columns of (V) (right singular vectors) are the unit eigenvectors of (A^T A). Columns of (U) (left singular vectors) are the unit eigenvectors of (A A^T).
* The numeric SVDs (A=U\Sigma V^T) reconstruct each (A) to machine precision.

# Conclusion

All requested items were computed: (A^T A), (A A^T), their eigenvalues and unit eigenvectors, the SVD (A=U\Sigma V^T), and verification that (U\Sigma V^T) reproduces (A) (up to tiny numerical rounding). The full numeric printout (matrices, eigenvectors and verification) is shown in the code output above.

If you want, I can:

* show a hand (symbolic) derivation for one of the matrices step-by-step, or
* produce a neatly formatted LaTeX write-up of the SVD details for either (A_1) or (A_2).

---

## Question 9
Consider the symmetric matrix

$$
S =
\begin{bmatrix}
4 & 1 & 0 \\
1 & 3 & 1 \\
0 & 1 & 2
\end{bmatrix}
$$

1. Compute the eigenvalues and eigenvectors of $$ S $$.  
2. Verify that the eigenvectors are orthogonal and form a **unitary matrix** $$ Q $$.  
3. Perform the **SVD** of $$ S $$.

## Answer for Question 9

Nice symmetric matrix — smells like a diagonalization / SVD party. I'll follow the numbers first, then summarize, then give the conclusion you can use.

# Data (computed)

Matrix
[
S=\begin{bmatrix}4&1&0[4pt]1&3&1[4pt]0&1&2\end{bmatrix}.
]

**Eigenvalues** (exact):
[
\lambda_1 = 3-\sqrt3,\qquad \lambda_2=3,\qquad \lambda_3=3+\sqrt3.
]
Numerically:
[
\lambda_1\approx 1.267949,\quad \lambda_2=3.0,\quad \lambda_3\approx 4.732051.
]

**Corresponding (unnormalized) eigenvectors** (one representative per eigenvalue):
[
v_1=\begin{bmatrix}2-\sqrt3[4pt]1-\sqrt3[4pt]1\end{bmatrix},\qquad
v_2=\begin{bmatrix}-1[4pt]1[4pt]1\end{bmatrix},\qquad
v_3=\begin{bmatrix}2+\sqrt3[4pt]1+\sqrt3[4pt]1\end{bmatrix}.
]

Normalized (unit) eigenvectors (columns of (Q)) — numerical values:
[
Q=\begin{bmatrix}
0.2113248654 & -0.5773502692 & 0.7886751346[4pt]
-0.5773502692 & 0.5773502692 & 0.5773502692[4pt]
0.7886751346 & 0.5773502692 & 0.2113248654
\end{bmatrix}.
]

# Summary / checks

* (S) is symmetric, so eigenvectors from distinct eigenvalues are orthogonal. Numerically,
  [
  Q^T Q = I_{3\times3}\quad(\text{within numerical precision}).
  ]
* Diagonalization holds:
  [
  S = Q , \mathrm{diag}(\lambda_1,\lambda_2,\lambda_3), Q^T.
  ]
  (You can check by multiplying the right-hand side; it reproduces (S) up to tiny rounding terms.)

# Conclusion — SVD of (S)

For a real symmetric matrix with positive eigenvalues (here all three (\lambda_i>0)), the SVD is especially simple: the singular values are the eigenvalues, and the left and right singular vectors coincide with the orthonormal eigenvectors.

Thus one valid SVD is
[
S = U \Sigma V^T
]
with
[
U = Q,\qquad V = Q,\qquad
\Sigma = \begin{bmatrix}\lambda_1&0&0[4pt]0&\lambda_2&0[4pt]0&0&\lambda_3\end{bmatrix}
= \begin{bmatrix}3-\sqrt3&0&0[4pt]0&3&0[4pt]0&0&3+\sqrt3\end{bmatrix}.
]

Numerically,
[
\Sigma\approx\operatorname{diag}(1.267949,,3.0,,4.732051),
]
and using the (Q) above gives (S \approx Q\Sigma Q^T) exactly (within rounding).

---

## Coding Assignment — Question 10
**Application of SVD for Image Noise Reduction**

Using the provided noisy grayscale image (link given in assignment), apply **Singular Value Decomposition (SVD)** to perform image noise reduction by reconstructing the image using a lower-rank approximation.

Plot and analyze how image quality changes as you vary the number of singular values retained.

1. Plot the singular values vs. rank.  
2. Decide an appropriate **rank cutoff** for reconstruction and justify your choice based on the singular value distribution and image quality.  
3. Reconstruct and display the image for different ranks (e.g., $$ r = 5, 10, \ldots $$) and your chosen cutoff rank.

## Answer for Question 10

Jupyter Notebook *.ipynb* file is seperately submitted for this coding question.

