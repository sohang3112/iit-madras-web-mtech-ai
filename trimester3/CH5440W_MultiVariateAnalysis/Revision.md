# Revision from Lecture Slides

## Partial Least Squares (PLS) Regression

PLS practically relevant application areas today:

| **Application Area**                        | **Primary Sub-Tasks / Methods**                                                                       | **Practical Relevance & Current Industry Usage**                                                                                                                                                   |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Chemometrics & Spectroscopy**             | NIR/FTIR calibration, chromatography quantitative analysis, process analytical technology (PAT).      | **Critical / Industry Standard.** Remained the foundational method across chemical and pharmaceutical manufacturing due to high collinearity in spectral bands and low sample counts.              |
| **Omics & Bioinformatics**                  | Metabolomics, proteomics, transcriptomics biomarker discovery (mostly via sparse PLS-DA / OPLS-DA).   | **High / Common Baseline.** Widely used for exploratory analysis and feature selection, though increasingly supplemented or benchmarked against regularized models (ElasticNet) and GBDTs.         |
| **Neuroimaging & fMRI Analysis**            | Brain-behavior mapping, resting-state fMRI connectivity, voxel-wise latent multivariate associations. | **Moderate to High.** Actively used in cognitive neuroscience to associate full-brain spatial patterns with multi-dimensional behavioral batteries.                                                |
| **Industrial Process Control & Monitoring** | Soft-sensing, batch process trajectory tracking, multivariate statistical process control (MSPC).     | **Moderate to High.** Extensively deployed in refineries and chemical plants to estimate hard-to-measure output properties from real-time sensor streams without overfitting.                      |
| **Structural Equation Modeling (PLS-SEM)**  | Consumer behavior modeling, marketing path models, organizational research with latent factors.       | **Moderate (Domain-Specific).** Standard in marketing and management science when sample sizes are small and distributions are non-normal, but rarely used in mainstream tech/ML engineering.      |
| **Computer Vision (Feature Extraction)**    | Face recognition, pedestrian detection, visual tracking on latent projections.                        | **Low / Mostly Historical.** Largely superseded by deep representation learning (CNNs, Vision Transformers) over the past decade; primarily relevant in niche low-power edge regimes.              |
| **General Tabular Machine Learning**        | Supervised dimensionality reduction and regression on correlated tabular features.                    | **Low.** Modern tabular practitioners largely favor Tree Ensembles (XGBoost, LightGBM, CatBoost) or Ridge/Lasso regularization, which handle non-linearities and sparsity with less manual tuning. |

### 21.07.2026 > PLS Share 1.pdf

Find $w$ so that $Cov(X w, Y)$ is maximum.

PLS uses **projection** to latent structures.

PLS searches for a latent direction $t = X w$ such that:
* $t$ explains a large amount of variance in X, and
* $t$ has maximum covariance with $Y$

PLS rotates X coords system to find axis / direction where changes in X produce largest changes in Y.

Project X, Y into lower-dimensional space:

$$ 
X = T P^T + E \quad (n,p) = (n,a) \times (a,p) \\
Y = U Q^T + F \quad (n,m) = (n,a) \times (a,m)
$$

where $T$, $U$ are **score matrices** / latent variables / common structures, $P$, $Q$ are loadings of original $X$, $Y$, and $E$, $F$ are residuals.

Maximize score variance $Cov(T,U)$ .

TYPES OF PLS:
* PLS 1 : params optimally tuned to predict single response variable at a time
* PLS 2 : multiple response variables at once (useful when responses are conceptually related), more efficient than running PLS 1 many times

Preprocessing before PLS:
* handle missing values, outliers & anamolies
* variables invovled should have somehwat symmetric distributions
* Data is normalized (mean 0, variance 1) ; if very skewed then log-normalized (because PLS weights are sensitive to units, we don't want higher variance variables to influence more)
  * If any variable is indeed more important, then assign it higher scaling weight (in normalize)
  
PLS Algorithms:
* NIPALS (Non Linear Iterative Partial Least Squares) - preferred? 
* SIMPLS (Statistically Inspired Partial Least Squares)

### 28.07.2026 > PLS Share 2.pdf -- TODO

### 11.08.2026 > Discriminant Analysis

According to Gemini, Discriminant Analysis is actually obsolete now in all its application areas (save for a few niches) :(

| **Application**                         | **Real-World Popularity**             | **Dominant Modern Replacement**                           | **Where LDA is Still Actively Used**                                                     |
| --------------------------------------- | ------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **ML Classification**                   | **Very Low** (niche only)             | XGBoost, LightGBM, Logistic Reg, Neural Nets              | **Brain-Computer Interfaces (BCI/EEG)**, real-time embedded systems, simple chemometrics |
| **Supervised Dimensionality Reduction** | **Low to Moderate**                   | PCA (unsupervised), UMAP, Feature Selection               | Linear preprocessing before low-power hardware classifiers                               |
| **Data Visualization**                  | **Low**                               | t-SNE, UMAP, PCA                                          | Quick linear multi-class cluster check                                                   |
| **Feature Diagnostics / Importance**    | **Low in ML** (Moderate in Academics) | SHAP, Permutation Importance, Lasso                       | **Social sciences / Psychology** (via SPSS/Stata), econometrics                          |
| **Anomaly / Outlier Detection**         | **Low**                               | Isolation Forest, One-Class SVM, Mahalanobis/Autoencoders | Classical statistical quality control                                                    |

Linear Discriminant Analysis vs Logistic Regression:

| Feature / Aspect                | Linear Discriminant Analysis (LDA)                                                                          | Logistic Regression                                                                                                    |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Feature Distribution Assumption | Assumes features X within each class follow a multivariate normal distribution.                             | No assumption about the distribution of X (works with skewed, categorical, or non-normal data).                        |
| Covariance Assumption           | Assumes all classes share the same covariance matrix ($\Sigma_1 = \Sigma_2$​).                              | No equal covariance assumption required.                                                                               |
| Optimization / Solution         | Closed-form analytic solution (exact estimates for mean and covariance). Extremely fast to compute.         | Iterative optimization (e.g., gradient descent, L-BFGS, Newton-Raphson) to maximize likelihood.                        |
| Handling Outliers               | Sensitive to outliers, as sample means and covariance matrices can be heavily skewed by extreme points.     | More robust to outliers compared to LDA.                                                                               |
| Separation Problem              | Handles well-separated classes stably.                                                                      | Can suffer from instability/divergence when classes are perfectly separated (coefficients explode unless regularized). |
| Sample Size Efficiency          | If assumptions hold, it is statistically more efficient and achieves higher accuracy with smaller datasets. | Requires more training samples to match LDA's efficiency when LDA's normality assumptions hold.                        |