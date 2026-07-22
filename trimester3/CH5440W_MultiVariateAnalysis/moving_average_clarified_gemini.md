Here is how moving average imputation works for missing values in time series analysis.

---

## 1. Direction: Left-to-Right vs. Centered

* **Left to Right (Past to Future):** Mandatory for **real-time / forecasting** scenarios to avoid lookahead bias (using future values to predict past ones).
* **Centered Window:** Preferred for **offline batch processing** (historical data analysis). A centered window (e.g., $k=1$ before and $k=1$ after) preserves local trends much better than relying solely on past data.

---

## 2. Using Imputed Values in Subsequent Windows (Recursive vs. Non-Recursive)

Whether you use newly filled `NA` values to impute consecutive `NA`s depends on the method:

* **Non-Recursive (Standard Moving Average):** Calculates the average using **only known, original valid data points** within the window. If consecutive `NA`s exist, you either expand the window or ignore missing points inside the window calculation.
* **Recursive / Sequential (Autoregressive Imputation):** Fills `NA` left-to-right and **uses the newly imputed value** as a valid data point when calculating the next window. This is common when long blocks of consecutive missing values occur, though it can propagate estimation error.

In multivariate time series, this logic is typically applied **column-by-column (feature-by-feature)** unless you use cross-variable correlation models (like vector autoregression or Kalman filters).

---

## Worked Example

Suppose we have a single variable in a time series with consecutive missing values (`NA`s):

$$\text{Series: } [10, 20, \text{NA}, \text{NA}, 50]$$

Let's use a **trailing window of size $k=2$ (left-to-right)**.

### Method A: Recursive (Using Previously Imputed Values)

#### Step 1: Fill $t_3$ (first `NA`)

Look at the previous 2 values ($t_1=10, t_2=20$):


$$\text{Value}(t_3) = \frac{10 + 20}{2} = 15$$


Updated Series: $[10, 20, \mathbf{15}, \text{NA}, 50]$

#### Step 2: Fill $t_4$ (second `NA`)

Look at the previous 2 values ($t_2=20$, and our newly imputed $t_3=15$):


$$\text{Value}(t_4) = \frac{20 + 15}{2} = 17.5$$


Final Series: $[10, 20, \mathbf{15}, \mathbf{17.5}, 50]$

---

### Method B: Non-Recursive Centered Window (Offline Preferred)

If analyzing historical data offline, a **centered window** (1 point left, 1 point right) yields smoother results.

#### Step 1: Fill $t_3$

Look at $t_2=20$ (left) and $t_4=\text{NA}$ (right). Since $t_4$ is missing, skip it or average over available valid points in the range $t_2..t_5$:

* Valid neighbors around $t_3$: $t_2=20$ and $t_5=50$

$$\text{Value}(t_3) = \frac{20 + 50}{2} = 35$$



#### Step 2: Fill $t_4$

Using known valid neighbors $t_2=20$ and $t_5=50$:


$$\text{Value}(t_4) = \frac{20 + 50}{2} = 35$$


Final Series: $[10, 20, \mathbf{35}, \mathbf{35}, 50]$ *(or linear interpolation for a smoother $20 \rightarrow 30 \rightarrow 40 \rightarrow 50$ transition)*.

---