# DA5000W: LinearAlgebra & Probability

## Linear Algebra

**Faculty**: Prof Ramakrishna Pasumarthy

Common unofficial P2P Colab Notebook shared by Samuel (classmate): Linear Algebra: https://colab.research.google.com/drive/1Ka_REmcYf0RYliDglSsrnbkWQXHkfU74#scrollTo=V5HgLa5q9Crh

### IN PROGRESS: Lecture Notes

Each heading here is a title of a lecture PDF. Under that are my notes on it.

#### ALMOST DONE: Introduction: Linear Algebra for Data Science

- Solution types: Consistent (unique, infinite), Inconsistent (no solution)
- Elimination (High school method)
- Graphical Method (plot 2 equation lines, point where they meet is solution)
- **Geometry of Linear Equations**: 3 ways of viewing System of Linear Equations:
    - Matrix Form $A \mathbf{x} = \mathbf{b}$
        where $A$ is coefficient matrix, $\mathbf{x}$ is vector of unknown variables, $\mathbf{b}$ is vector of RHS values.
    - Row Picture - viewing one equation at a time. Each equation is a line (2D) / plane (3D) / hyperplane (n-D). 2 3D equations/planes meet at a 2D line/equation. In graph common inyeresection is equation solution point(s) if any.
    - Column Picture - view as one vector equation in terms of column vectors of $A$:
If $A = \mathbf{a}_1 \ \mathbf{a}_2 \ \dots \ \mathbf{a}_n$ and x vector has x1, x2 .. xn scalars then:

$$
A x = b \quad \text{translates to} \quad x_1 \mathbf{a}_1 + x_2 \mathbf{a}_2 + \dots + x_n \mathbf{a}_n = \mathbf{b}.

$$

- *Order of Matrix* is $m \times n$ (rows, columns) - $m$ equations, $n$ unknowns (rectangular matrix). Becomes square matrix if $m = n$.
- *Singular* coefficient matrix is not invertible, so either no (all dont interesect at any common line, though 2 of them might - eg. triangle 3 arms dont interesct at single common point) or infinite solutions (all interesect at common points), depending on RHS $\mathbf{b}$.

**TODO: graphically plot column view** - question came previously in an IIT question paper I think!

#### DONE: Linear Algebra 1: Vector Space Norms

**Vector Space** / subspace is a set of vectors, and a field of scalar $\mathbb{F}$, having these binary operations:
- closed under vector addition, ie $\mathbf{x} + \mathbf{y}$ also in same vector space.
- closed under scalar multiplication, ie $c \mathbf{x}$ also in same vector space.

Additionally it must satisfy these 8 properties:
- exists unique zero vector such that $\mathbf{x} + 0 = \mathbf{x}$
- Commutative: $\mathbf{x} + \mathbf{y} = \mathbf{y} + \mathbf{x}$
- Associative: $(\mathbf{x} + \mathbf{y}) + \mathbf{z} = \mathbf{x} + (\mathbf{y} + \mathbf{z})$
- Negative vector: exists unique so that $\mathbf{x} + (\mathbf{-x}) = 0$
- Identity with scalar mutliply: $1 \mathbf{x} = \mathbf{x}$
- Associativity with 2 scalars: $(c_1 c_2) \mathbf{x} = c_1 (c_2 \mathbf{x})$
- Distributivity with scalar factor: $c (\mathbf{x} + \mathbf{y}) = c \mathbf{x} + c \mathbf{y}$
- Distributivity with vector factor: $(c_1 + c_2) \mathbf{x} = c_1 \mathbf{x} + c_2 \mathbf{x}$

Examples of both: vector spaces, and not vector spaces, in below image:

![Examples: vector spaces yes / no](images/vector_space_examples.png)

**Inner Product Vector Space** is a vector space in which inner product exists $\mathbf{x} \cdot \mathbf{y} = c$

**Normed Vector Space** is an Inner Product Vector space in which a norm exists. **Norm** function converts any vector in vector space to a positive scalar length.
*p-Norm Vector Space* is a normed vector space in which p-norm $\| \mathbf{x} \|_p = p(\mathbf{x})$ exists.

**Vector Norm** is basically magnitude of a vector. Properties:
- non-zero vector -> non-zero positive scalar norm: $\| \mathbf{x} \| \gt 0$
- zero vector -> zero norm $\| \mathbf{x} \| = 0$ iff $\mathbf{x} = 0$
- scalar multiply: $\| c \mathbf{x} \| = c \| \mathbf{x} \|$
- triangular inequality: $\| \mathbf{x} \| + \| \mathbf{y} \| \le \| \mathbf{x} + \mathbf{y} \|$

Important Norms:
- 0-norm: count of vector dimensions
- 1-norm: sum of vector components
- 2-norm (Euclidean): $\sqrt{\| \mathbf{x}^2 + \mathbf{y}^2 \|}$
- general $p$-norm: $\| \mathbf{x}^p + \mathbf{y}^p \| ^ {1/p}$
- Infinity $\inf$-norm is maximum axis value of $\mathbf{x}$

**Equivalence of Norms**: 2 norms $\| . \|_a$ and $\| . \|_b$ are equivalent if one norm can be bounded wrt other norm: 

$$\exists \alpha, \beta \in \mathbb{R}^n, \alpha \| \mathbf{x} \|_a \le \| \mathbf{x} |_b \le \beta \| \mathbf{x} \|_a$$

**Metric Space** $X$ is a set where **distance metric function between 2 vectors** exists: $d: X -> X -> \mathbb{R}^+$.
*Normed vector space is a Metric space, but a Metric space need not be a Normed vector space.*

Properties of metric:
- positive: $d(\mathbf{x}, \mathbf{y}) \ge 0$
- zero distance if equal: $d(\mathbf{x}, \mathbf{y}) = 0$ iff $\mathbf{x} = \mathbf{y}$
- commutative args: $d(\mathbf{x}, \mathbf{y}) = d(\mathbf{y}, \mathbf{x})$
- triangular inequality: $d(\mathbf{x}, \mathbf{z}) \le d(\mathbf{x}, \mathbf{y}) + d(\mathbf{y}, \mathbf{z})$

**Euclidean Space**:
- *Euclidean Norm* is 2-norm
- *Euclidean distance* $d(\mathbf{x}, \mathbf{y}) = \| \mathbf{x} - \mathbf{y} \|$ using any vector norm $\| . \|$.

#### TODO: Linear Algebra 2: Span, Basis, Vector Subspace



#### TODO: Linear Algebra 3

#### TODO: Eigen Values and Eigen Vectors

#### TODO: Linear Systems Theory

#### TODO: Linear Algebra 5

#### TODO: Linear Algebra Class Notes: written by Professor in freeform using Stylus Pen


### Linear Algebra More Resources

Books:

- Numerical Linear Algebra: reading it
- [Linear Algebra by Jim Hefferon](http://joshua.smcvt.edu/linearalgebra)
- [A First Course in Linear Algebra by Robert A. Beezer](http://linear.ups.edu/download/fcla-electric-2.00.pdf)
- [Linear Algebra Toolkit by Przemyslaw Bogacki](http://www.math.odu.edu/~bogacki/lat)

--------------------------------------------

## Probability & Statistics

**Faculty**: Prof Nandan Sudarshan

### Lecture Notes

Each heading here is a title of a lecture PDF. Under that are my notes on it.

#### TODO: Lecture Note 1 & 2

#### TODO: Lecture Note 3

#### TODO: Lecture Note 4

#### TODO: Lecture Note 5.1

#### TODO: Lecture Note 5.2
