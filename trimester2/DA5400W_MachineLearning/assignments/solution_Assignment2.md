---
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

# Foundations of Machine Learning Assignment 2

Submitted by: Sohang Chopra &lt;DA25M622&gt;


## Problem 1
Consider a dataset with two numerical features:


   - _x_ 1 measured in kilometers, with values approximately ranging from 0 to 10.


   - _x_ 2 measured in meters, with values approximately ranging from 0 to 500.


No preprocessing or scaling is applied to the data.


(a) Explain how the difference in feature scales affects clustering when Euclidean distance is used.


(b) If K-means clustering is applied directly to this dataset without preprocessing, which
feature is likely to dominate the clustering result? Justify your answer.


(c) Describe one preprocessing technique to address this issue and explain how it changes
the geometry of the data.

## Solution 1

TODO: theory


## Problem 2


(a) Explain the role of distance (or similarity) measures in clustering algorithms.


(b) Compare **Euclidean distance** and **Mahalanobis distance** . Discuss how the
choice of distance measure affects:


     - The shape of clusters

      - Sensitivity to feature scaling and correlation


(c) Give one practical scenario where Euclidean distance may lead to poor clustering
results and justify your answer.

## Solution 2

TODO: theory


## Problem 3


(a) Explain the intuition behind the Knee (Elbow) Method for selecting the number of
clusters in partitional clustering algorithms.


(b) Discuss two limitations of the Knee Method when applied to real-world datasets.


(c) Describe one alternative approach for estimating the number of clusters and explain
how it differs conceptually from the Knee Method.

## Solution 3

TODO: theory


## Problem 4


(a) Explain the working principle of hierarchical agglomerative clustering. What is the
role of a dendrogram?


(b) Compare the following linkage criteria:


     - Single-link

     - Complete-link

     - Average-link


in terms of cluster shape, sensitivity to noise, and tendency to form compact clusters.


(c) Explain how the choice of linkage affects the structure of the resulting dendrogram.

## Solution 4

TODO: theory


## Problem 5


Hierarchical agglomerative clustering is applied to a dataset using single-linkage clustering.


(a) Explain how the presence of a small number of noisy or outlier points can significantly
alter the resulting dendrogram.


(b) Compare the sensitivity of single-linkage and complete-linkage clustering to such
noise.


(c) Discuss how this sensitivity impacts the interpretability of clusters obtained by cutting the dendrogram at a fixed height.

## Solution 5

TODO: theory


## Problem 6


(a) Explain how a dataset can be represented as a weighted undirected graph for clustering purposes.


(b) Describe how single-link and complete-link hierarchical clustering can be interpreted
using thresholded graphs.


(c) Using this graph-theoretic view, discuss one strength and one weakness of each
method.

## Solution 6

TODO: theory


## Problem 7


The _k_ -means algorithm (Lloyd’s algorithm) is widely used for partitional clustering.


(a) Can the algorithm result in fewer than _k_ clusters at any iteration, even if _k_ was
initially specified? Justify your answer.


(b) Can the algorithm ever return to the same clustering arrangement that it had in any
of the previous iterations? Justify your answer.

## Solution 7

TODO: theory


## Problem 8


Consider the following points:


_x_ 1 = [0 _, −_ 1] _,_ _x_ 2 = [0 _,_ 1] _,_ _x_ 3 = [1 _,_ 0] _,_ _x_ 4 = [1 _,_ 0] _,_ _x_ 5 = [ _−_ 1 _,_ 0] _,_ _x_ 6 = [0 _,_ 0] _._


For _k_ = 3, is _{x_ 3 _, x_ 6 _, x_ 4 _}_ a valid order of means selected during _k_ -means++ initialization?
If not, suggest one valid possible order and justify briefly.

## Solution 8

TODO: theory


## Problem 9
Consider the following 2D data points:


_P_ 1 : (7 _._ 0 _,_ 6 _._ 5) _,_ _P_ 2 : (5 _._ 0 _,_ 10 _._ 0) _,_
_P_ 3 : (6 _._ 2 _,_ 7 _._ 1) _,_ _P_ 4 : (2 _._ 0 _,_ 3 _._ 1) _,_
_P_ 5 : (9 _._ 3 _,_ 2 _._ 4) _,_ _P_ 6 : (8 _._ 5 _,_ 1 _._ 9) _,_
_P_ 7 : (2 _._ 8 _,_ 3 _._ 6) _._


Apply the DBSCAN algorithm with parameters minPts = 2 and _ε_ = 1 _._ 15 using Euclidean
distance.
After running DBSCAN with the given parameters, determine the number of clusters
formed.

## Solution 9

TODO: theory


## Problem 10


For each of the following datasets (a)–(d), assume the number of clusters is _k_ = 2. Which
clustering method among the following would work best? Justify briefly.


   - Hierarchical clustering with single-link


   - Hierarchical clustering with complete-link


   - Hierarchical clustering with average-link


   - _k_ -means


   - Gaussian Mixture Model (with no restriction on covariance matrices)


**(a)**




**(b)**


**(c)**


**(d)**

## Solution 10

TODO: theory


