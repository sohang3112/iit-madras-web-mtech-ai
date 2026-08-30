# Partial Least Squares (PLS) — Condensed Exam Notes
### CH5440 Multivariate Analysis





---


## 1. Why PLS? (Motivation)

Classical **Multiple Linear Regression (MLR)** needs X to be full rank. It breaks down when:

- **p >> n** (more predictors than observations) — X can't be full rank; may become **singular**.
- **Collinear variables** — nearly dependent columns → X'X singular, MLR unstable.
- **Noisy data**, redundant information.

> Even when p and n are comparable ("square data") or n >> p ("tall data"), PLS is still useful when collinearity exists.

**Key cause of singularity when p is large:** over-parameterization — rows/columns become linearly dependent.

**PLS purpose:** Build a **predictive** model (unlike PCA, which has no defined response) by projecting high-dimensional, collinear data onto a small number of **latent variables (LVs)**.

---

## 2. Core Idea

PLS = combines **PCA's dimension reduction** + **MLR's prediction goal**.

- PCA: reduces dimensionality of X only, **ignoring Y**.
- MLR: predicts Y, but fails when X is singular/collinear.
- **PLS**: decomposes **X and Y simultaneously** into latent variables (factors) that **maximize the covariance** between them.

> "PLS doesn't look for major trends in the data; it looks for trends that connect inputs (X) to outputs (Y)."

### The Fundamental Objective
$$t = Xw$$
where **w** = weight vector, **t** = latent score (X-space direction).

PLS finds **w** such that:
1. *t* explains a large amount of variation in X, **and**
2. *t* has maximum covariance with Y.

$$\boxed{\text{Find } w \text{ so that } \text{Cov}(Xw, Y) \text{ is maximum}}$$

**Geometric view:** PLS rotates the X-coordinate axes until one axis points in the direction that is *most useful for predicting Y* — not merely the direction of largest variance in X (that's PCA).

---

## 3. PCA vs PCR vs PLS (High-Yield Comparison)

| Aspect                  | PCA / PCR                                                        | PLS                                                                 |
| ----------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------- |
| Component extraction    | **Unsupervised** — based only on variance in X                   | **Supervised** — based on maximizing **covariance** between X and Y |
| Objective               | Best explain variance in X                                       | Best explain variance in X **and** covariance with Y                |
| Role of Y               | Ignored during extraction (used only later in MLR step, for PCR) | Actively guides extraction of every component                       |
| Correlation matrix used | Full matrix (all variables, incl. correlation among predictors)  | Only the **sub-matrix** linking **predictors ↔ responses**          |
| Predictive power        | Weaker — components not optimized for prediction                 | Stronger — components optimized directly for predicting Y           |
| Best for                | Understanding internal structure of X                            | Robust prediction under multicollinearity/high dimensionality       |

### Correlation Matrix Schematic (Σ for Y's and X's)
For Y₁,Y₂ (responses) and X₁,X₂,X₃,X₄ (predictors), arranged as one big correlation matrix:

- **Blue block** = correlation **between responses** (Y–Y)
- **Orange block** = correlation **between predictors** (X–X)
- **Green block** = correlation **between predictors and responses** (X–Y)

**PCA** uses the **orange** sub-matrix (X–X) → PCR reduces X dimensionality via PCA, then regresses Y on the components (still ignores Y during extraction).
**PLS** uses the **green** sub-matrix (X–Y correlations) to extract factors.
Using the **entire** matrix (no distinction of X/Y) → reduces to plain PCA.

**Technical requirement:** correlation matrix elements must lie in [–1, +1], and matrix must be **square and symmetric**. (Note: the X–Y sub-matrix itself is generally **not square** and has **no special symmetry** for general p, m.)

### Visual/Conceptual difference (PC1 vs PLS1)
- PC1 is oriented to capture max variance in X, **regardless of Y** — it can be nearly perpendicular to the direction Y increases in.
- PLS1 is **rotated** relative to PC1, tilted toward the direction in which Y increases/decreases — it sacrifices a little X-variance to gain relevance to Y.

---

## 4. The Model Equations (Outer Relations)

$$X = TP' + E \qquad (n\times p = n\times a \; \times \; a\times p)$$


$$Y = UQ' + F^{*} \qquad (n\times k = n\times a \; \times \; a\times k)$$

| Symbol | Meaning                                                                               |
| ------ | ------------------------------------------------------------------------------------- |
| T, U   | **Score matrices** (n×a) — latent variables/common structure for X and Y              |
| P, Q   | **Loadings** (p×a, k×a) — show how original variables contribute to latent structures |
| E, F*  | Residuals (noise / unexplained structure)                                             |
| a      | number of latent variables (factors) extracted                                        |

**Goal:** Maximize Cov(T, U).

### Inner Relation (links T and U)
$$U = TB + H$$
- B = diagonal matrix (a×a) relating the two score spaces.
- H = residual (n×a).

### Mixed Relation (obtained by substitution)
$$Y = (TB+H)Q' + F^{*} = TBQ' + (HQ' + F^{*})$$
$$\boxed{Y = TBQ' + F}$$
- F = residual of the **mixed relation** (used for prediction — this is why F, F* matter: prediction is PLS's ultimate goal).
- Because rank of Y is not necessarily reduced by 1 per component, the **maximum number of components extractable = rank of X**.

---

## 5. Weights vs Loadings — Critical Distinction

| Aspect         | Weight (w)                                          | Loading (p)                                                                       |
| -------------- | --------------------------------------------------- | --------------------------------------------------------------------------------- |
| Purpose        | **Defines** the latent variable                     | Describes how original X variables are **reconstructed** from the latent variable |
| Computed from  | Optimizing covariance between X and Y               | Regression of X on score t                                                        |
| Formula        | $t = Xw$                                            | $X \approx tp^T$                                                                  |
| Interpretation | Importance of each X variable in **constructing** t | Correlation/contribution of t in **reconstructing** each X variable               |
| Used for       | Projection (going from data → score)                | Reconstruction/decomposition (going from score → data)                            |

### Solved Example — Weights & Loadings
**Step 1 (Weight vector):** Standardized X₁,X₂,X₃. Suppose PLS finds
$$w = \begin{bmatrix}0.7\\0.6\\0.4\end{bmatrix} \Rightarrow t = 0.7X_1+0.6X_2+0.4X_3$$
This tells us **how to combine** the original variables to get the latent variable t.

**Step 2 (Loading vector):** Once t is known, express X back in terms of t: $X \approx tp^T$. Suppose
$$p = \begin{bmatrix}0.9\\0.8\\0.5\end{bmatrix} \Rightarrow X_1\approx 0.9t,\; X_2\approx 0.8t,\; X_3\approx 0.5t$$
This tells us **how strongly** each original variable relates to the latent score.

---

## 6. Solved Example — "Hunting for Hidden Patterns"

**Setup:** A chemical reactor has sensors: Temperature, Pressure, Flow rate, Catalyst age; output = Product purity.

**Individual correlations with purity (weak):**

| Variable     | Correlation with purity |
| ------------ | ----------------------- |
| Temperature  | 0.20                    |
| Pressure     | 0.18                    |
| Flow         | 0.15                    |
| Catalyst age | 0.10                    |

Each sensor **alone** is weakly related to purity. **But** a hidden linear combination:
$$t = 0.7(\text{Temp}) + 0.5(\text{Pressure}) - 0.4(\text{Flow}) + 0.3(\text{Catalyst age})$$
may correlate **0.95** with purity!

**Interpretation:**
- **PCA** asks: "which direction explains the largest variation in X?" → ignores Y entirely, may pick a direction irrelevant to purity.
- **PLS** asks: "which direction in X best predicts Y?" → even if that direction has only *moderate* variance in X, PLS prefers it because of its strong predictive power.

This is the essence of "hunting": among useful info + noise + redundant info in X, PLS searches for the combination most predictive of Y.

**General setup:** X = [X₁,X₂,X₃,X₄], Y=[Y₁,Y₂]. None of the individual Xᵢ predicts Y well, but
$$t = 0.6X_1+0.5X_2-0.3X_3+0.4X_4$$
strongly predicts both responses. This t is a **latent score** — "hidden" because it doesn't correspond to any single measured variable.

---

## 7. Solved Numeric Example — Computing t₁ = Xw₁

**Given (illustrative small dataset):** n=10 observations, p=5 predictors, k=3 responses.

$$X_{(10\times5)} = \begin{bmatrix}2&4&6&5&3\\3&5&7&6&4\\4&7&9&8&5\\ \vdots\end{bmatrix},\qquad Y_{(10\times3)}=\begin{bmatrix}20&12&30\\24&15&35\\ \vdots\end{bmatrix}$$

Suppose (found via NIPALS iteration) the first weight vector is:
$$w_1 = \begin{bmatrix}0.2916\\0.4525\\0.5556\\0.5054\\0.3822\end{bmatrix}\ (p\times1)$$

**Step:** Compute the score vector $t_1 = Xw_1$ (each row of X dotted with w₁):

For observation 1: $t_1^{(1)} = 2(0.2916)+4(0.4525)+6(0.5556)+5(0.5054)+3(0.3822) = 9.4004$

Repeating for all 10 rows gives the full score vector:
$$t_1 = [9.40,\ 11.59,\ 15.29,\ 17.48,\ 21.11,\ 23.75,\ 27.00,\ 30.57,\ 33.27,\ 36.84]^{T}$$

**Interpretation table:**

| Quantity | Dimension | Represents                                                                      |
| -------- | --------- | ------------------------------------------------------------------------------- |
| w₁       | p×1       | Direction (combination of variables) defining the 1st latent variable           |
| t₁       | n×1       | Coordinates (scores) of all n observations after projecting onto that direction |

**Analogy (flashlight):** w₁ is the *direction of the flashlight beam*; t₁ contains the *positions/shadows* of all observations along that beam.

**Checking validity:** After finding Y-scores u₁ = Yq₁ similarly, if we compute correlation between t₁ and u₁, we should see it very close to 1 (e.g., corr = 0.9998), confirming X-scores and Y-scores are strongly correlated for the first factor — exactly the PLS objective (max covariance).

---

## 8. PLS1 vs PLS2

|             | **PLS1**                                         | **PLS2**                                                                                                        |
| ----------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| Response    | **Single** Y variable modeled at a time          | **Multiple** Y variables (columns) modeled simultaneously                                                       |
| Extraction  | Components optimally tuned for that one response | Components explain covariance structure across **all** responses at once                                        |
| Use case    | Simpler interpretation; single prediction task   | Responses are conceptually related; more efficient than running separate PLS1 models; captures shared structure |
| Commonality | Most common variant in practice (both)           |                                                                                                                 |

---

## 9. Data Preprocessing (always precedes PLS)

1. **Screen & clean**: handle missing values, outliers, anomalies.
2. Works best when variables are roughly **symmetric**; log-transform highly skewed variables.
3. **Center & scale (normalize)**: subtract mean, divide by std. dev → every variable has mean 0, SD 1.

**Why normalize/scale?**
- Weights are very sensitive to measurement **units**.
- Without scaling, high-variance variables dominate the model unfairly.
- Scaling puts all variables on **equal footing**.
- (If some X variables are *known* to be more important, you can deliberately assign them higher scaling weight.)

After centering & scaling, **covariance matrix = correlation matrix** — this is why "PLS starts from the correlation matrix."

---

## 10. PLS Theory — Formal Statement

- t₁ is a linear combination of variables in **X** that has **maximum covariance** with a linear combination of variables in **Y**, subject to normalizing constraints:
$$\text{Cov}(t_1, u_1)\ \text{is MAXIMUM}, \quad t_1 = Xw_1,\ u_1 = Yq_1$$
- q₁ = a **Y weight vector**; elements of u₁ = **Y scores**.
- For the **first** factor, X-scores and Y-scores are expected to be strongly correlated.

**Extracting subsequent factors — Deflation:**
- Use all factors extracted so far to predict both X and Y; work on the **residuals**.
- New weight vectors are computed on these residuals (NIPALS).
- This process is called **deflation**: X, Y are split into (prediction + residual), and the next factor uses only the residual.
- Ensures new factors are **orthogonal** to (independent of) previously extracted ones.

**Notation for 'a' extracted factors:**
- W = p×a matrix of weight vectors w₁,...,w_a
- T, U = n×a matrices of X-scores, Y-scores (t₁..t_a, u₁..u_a)

**Orthogonality property:** X is decomposed as X = TP′ with **T′T = I** (T′ = T⁻¹), i.e., latent factors are orthogonal.

---

## 11. NIPALS PLS2 Algorithm — Full Step Sequence

Instead of below long 12 steps, a colleague shared that the core of NIPALS is just 3 steps  Weights(only for X)->score->loadings . Finally using loading deflate and remove from X(E) or Y(F) from previous step 

Weights compress original X to scores 

Loaadings deflate score to orignal space

**Initialization:** E₀ = X̃ (mean-centered, scaled X); F₀ = Ỹ (mean-centered, scaled Y).
For each component h = 1, 2, …, a, repeat:

| Step   | Operation                                                                                                             | Equation                                            |
| ------ | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| **0**  | Initialize $U_h$ = a column of $F_{h-1}$ (e.g., highest-variance column of Y)                                         | —                                                   |
| **1**  | Regress $E_{h-1}$ on uₕ to get X-weights                                                                              | $w_h' = [u_h'u_h]^{-1}u_h'E_{h-1}$                  |
| **2**  | Normalize wₕ                                                                                                          | $w_h' = w_h'/\lVert w_h\rVert$                      |
| **3**  | Regress $E^T_{h-1}$ on wₕ to get X-scores                                                                             | $t_h' = [w_h'w_h]^{-1}w_h'E_{h-1}'$                 |
| **4**  | Regress $F_{h-1}$ on tₕ to get Y-loadings                                                                             | $q_h' = [t_h't_h]^{-1}t_h'F_{h-1}$                  |
| **5**  | Normalize $q_h$                                                                                                       | $q_h' = q_h'/\lVert q_h\rVert$                      |
| **6**  | Regress $F^T_{h-1}$ on qₕ to get new uₕ                                                                               | $u_h' = [q_h'q_h]^{-1}q_h'F_{h-1}'$                 |
| **7**  | **Convergence check**: if $\lVert t_h - t_{h-1}\rVert > \varepsilon_c$, repeat from Step 1 with new uₕ; else continue | $\lVert t_h-t_{h-1}\rVert \le \varepsilon_c$        |
| **8**  | Regress $E_{h-1}$ on tₕ to get X-loadings                                                                             | $p_h' = [t_h't_h]^{-1}t_h'E_{h-1}$                  |
| **9**  | Rescale tₕ to match new pₕ                                                                                            | $t_h = t_h\lVert p_h\rVert$                         |
| **10** | Normalize pₕ (to length 1, comparable to PCA loadings)                                                                | $p_h' = p_h'/\lVert p_h\rVert$                      |
| **11** | Regress uₕ on tₕ to get inner-relation coefficient bₕ                                                                 | $b_h = [t_h't_h]^{-1}t_h'u_h$                       |
| **12** | **Deflate** (remove explained part from X, Y)                                                                         | $E_h = E_{h-1}-t_hp_h'$; $F_h = F_{h-1}-t_hb_hq_h'$ |

Then increment h and repeat until a factors are extracted (max a = rank of X).

### Why each cross-regression (quick logic, exam-friendly)
- **u → w** (Step 1): X-weights must reflect directions in X relevant to Y; regressing X-residual against the Y-score u finds exactly that ($w \propto E^T u$). PCA would instead maximize variance in E alone — PLS instead maximizes covariance with Y's latent structure.
- **t → q** (Step 4): Since PLS ultimately predicts Y from X's latent score t, we ask "how does Y vary along this X latent direction?" → project Y onto t to get q. This is why **X-scores (not loadings)** are used to find Y-loadings.
- Mnemonic: **u guides discovery of w** (which X-directions matter for Y); **t guides discovery of q** (how Y responds along the X latent direction). The algorithm alternates Y-guided extraction of X-components and X-guided reconstruction of Y — this alternation is what maximizes covariance while keeping predictive relevance.

### Mathematical Flow (1 component, cyclic)
$$u_h \xrightarrow{X^T} w_h \xrightarrow{X} t_h \xrightarrow{Y^T} q_h \xrightarrow{Y} u_h \;(\text{repeat till convergence})$$

### Why Steps 9–10 (normalize p, rescale t)?
- pₕ is normalized to length 1 so that loadings are **comparable to PCA loadings** (standard convention).
- Since pₕ changed by normalization, tₕ must be **rescaled** to stay consistent with the (E = tp′) relation.

### Why use mixed relation Y = TBQ′ + F (not outer relation Y=UQ′+F*) for updating/prediction?
- F, F\* exist specifically to support **prediction** — the actual goal of PLS.
- Because Y's rank is not necessarily reduced by exactly 1 per extracted factor, using the mixed relation allows extracting as many components as the **rank of X**.

---

## 12. Final Regression Coefficients (Prediction Equation)

Once **a** components are extracted, giving W (p×a), P (p×a), Q (k×a):

Substituting the score equation into the model:
$$Y = XW(P^TW)^{-1}Q^T$$

$$\boxed{\beta = W(P^TW)^{-1}Q^T}$$

This is **the most important prediction equation in PLS2** — β is the final (p×k) regression coefficient matrix relating original X directly to Y.

| Matrix | Dimension |
| ------ | --------- |
| X      | n × p     |
| Y      | n × q(k)  |
| W      | p × A     |
| P      | p × A     |
| Q      | q × A     |
| β      | p × q     |

---

## 13. NIPALS vs SIMPLS (know the names)

| Algorithm  | Full form                                                                |
| ---------- | ------------------------------------------------------------------------ |
| **NIPALS** | Nonlinear Iterative Partial Least Squares (iterative, described above)   |
| **SIMPLS** | Statistically Inspired Partial Least Squares (non-iterative alternative) |

Both extract latent variables/components/factors after centering (and possibly scaling) all variables.

---

## 14. One-Page Ultra-Summary (Last-Minute Revision)

1. **Why PLS:** handles p>>n, multicollinearity, singular X — MLR fails, PCA ignores Y.
2. **Core equations:** X = TP′+E, Y = UQ′+F*, inner relation U = TB+H, mixed relation Y = TBQ′+F.
3. **Objective:** maximize Cov(Xw, Y) i.e. Cov(t, u).
4. **PCA vs PLS:** PCA/PCR use X–X correlations (unsupervised); PLS uses X–Y correlation sub-matrix (supervised).
5. **Weight (w)** defines/builds the latent variable (t=Xw); **Loading (p)** reconstructs X from t (X≈tp′).
6. **PLS1** = single Y; **PLS2** = multiple Y's simultaneously.
7. **NIPALS loop per factor:** u→w (normalize)→t→q (normalize)→u (converge?) → p (normalize, rescale t) → b → **deflate** E,F.
8. **Deflation** = removing explained variance so next factor is orthogonal to previous ones; max factors = rank(X).
9. **Final prediction:** β = W(P′W)⁻¹Q′, so Ŷ = Xβ.
10. Always **center & scale** data first (equal footing across units).