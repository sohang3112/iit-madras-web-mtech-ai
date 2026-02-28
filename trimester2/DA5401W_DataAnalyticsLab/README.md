# DA5401 : Data Analytics Lab

Prof Arun Ayyar &lt;arun.ayyar@dsai.iitm.ac.in&gt;

This will have practical session for theory that is taught in [Machine Learning](../DA5400W_MachineLearning/) class.

Libraries: 
* Numpy
* Pandas
* Scipy
* Scikit-learn
* Seaborn

[PCA Plots](https://bioturing.medium.com/how-to-read-pca-biplots-and-scree-plots-186246aae063):

PCA Score (scatter) Plot:

![PCA Scatter Plot](images/pca_scatter_plot.png)

PCA Loading Plot shows how strongly each characterstic influences a principal component (X,Y axes are 2 principal components, each original component's vector is (x,y) of how much it influences the 2 principal components):
* when 2 feature vectors have a small angle between them => positively correlated
* right angle => likely no correlation
* (diverge) greater than 90 angle => negative correlation

![PCA Loading Plot](images/pca_loading_plot.png)

PCA Biplot (score + loading):

![PCA Biplot](images/pca_biplot.png)

## Notebooks

- [x] Pandas 1 & 2 
- [ ] ALMOST DONE: Industrial AI Week 1
- [x] Bootstrap & MoM
- [x] Probability Statistics
- [ ] WIP Optimization Methods
- [ ] PCA_Detailed_Tutorial
- [ ] WIP Optimization_PCA
- [ ] Clustering
- [ ] Regression (linear: ordinary & total least squares, logistic, etc.) - notebook not yet shared

SKIP (not coming in exam): 
* plotting image output
* Spectre Clustering

## Problems

- [x] *Part 4: Practice Exercises* cell in *Bootstrap_and_Method_of_Moments.ipynb*