clear all;
clc;

Data = [
  144  0.6  10
   89  1.0  10
   59  1.4  10
  278  0.6  20
  167  1.0  20
  141  1.0  20
  164  1.0  20
  129  1.4  20
  259  0.6  30
  245  1.0  30
  214  1.4  30
  ];

Lifecycle=Data(:,1);
Chargerate=Data(:,2);
Temperature=Data(:,3);

Y=Lifecycle;
X1=Chargerate;
X2=Temperature;

% i. Create the design matrix X for the raw data
X = [ones(numel(X1),1) X1 X2 X1.^2 X2.^2 X1.*X2];

% ii. Create a matric “z” 
z1=(X1-mean(X1))/(max(X1) - min(X1));
z2=(X2-mean(X2))/(max(X2) - min(X2));

Z=[ones(numel(z1),1) z1 z2 z1.^2 z2.^2 z1.*z2];

% iii. Find regression coefficients for the two different cases (X, and z). 
betahat_X=(inv(X'*X))*(X'*Y);
betahat_Z=(inv(Z'*Z))*(Z'*Y);


% iv. Find residual sum of squares, regression sum of squares, total sum of squares. Use 
% both Matrix and summation approaches and compare them.  Do the values change 
% depending upon the transformation? 

% Predicted response
YPred_X=X*betahat_X;
YPred_Z=Z*betahat_Z;

% SSE using the matrix approach
Res_SSQ1_X=(Y-X*betahat_X)'*(Y-X*betahat_X);
Res_SSQ1_Z=(Y-Z*betahat_Z)'*(Y-Z*betahat_Z);

% SSE using the summation approach
Res_SSQ2_X=0;
Res_SSQ2_Z=0;

for i=1:numel(Y)
    Res_SSQ2_X=Res_SSQ2_X+(Y(i)-YPred_X(i))^2;
    Res_SSQ2_Z=Res_SSQ2_Z+(Y(i)-YPred_Z(i))^2;
end

% Total Sum of Squares (SST)
SST = Y'*Y - numel(Y)*(mean(Y))^2;

% Regression Sum of Squares (SSR)
SSR_X = SST - Res_SSQ2_X;
SSR_Z = SST - Res_SSQ2_Z;

% v. Find the variance-covariance matrix in both cases and compare the matrices for the 
% transformed(z) and non-transformed (X) cases.  Which is better in terms of precision of 
% the regression coefficient estimates? 

p=size(betahat_X,1); % verify if total number of parameters = 6
dof_Res = numel(X1)-p; % n-p

% Computing estimate of error variance using mean square residual
sigma_hat_X2=Res_SSQ2_X/dof_Res;
sigma_hat_Z2=Res_SSQ2_Z/dof_Res;

% Variance-Covariance Matrix based on X and Z data 
Var_beta_X=inv(X'*X)*sigma_hat_X2; %Variance-Covariance Matrix based on X  data
Var_beta_Z=inv(Z'*Z)*sigma_hat_Z2; %Variance-Covariance Matrix based on Z  data

% vi. Find R2, adj. R2, PRESS, R2 PRESS for both the cases

% Coefficient of Determination R^2
R2_X=1-Res_SSQ2_X/(Y'*Y-numel(X1)*(mean(Y))^2);
R2_Z=1-Res_SSQ2_Z/(Y'*Y-numel(z1)*(mean(Y))^2);

% H Matrices
HX=X*(inv(X'*X))*X';
HZ=Z*(inv(Z'*Z))*Z';

PRESS_X=0;
PRESS_Z=0;

for i= 1: numel(Y)
    PRESS_X=PRESS_X + ((Y(i)-YPred_X(i))/(1-HX(i,i)))^2;
    PRESS_Z=PRESS_Z + ((Y(i)-YPred_Z(i))/(1-HZ(i,i)))^2;
end

% Coefficient of determination based on PRESS
R2_PRESSX=1-PRESS_X/(Y'*Y-numel(X1)*(mean(Y))^2);
R2_PRESSZ=1-PRESS_Z/(Y'*Y-numel(z1)*(mean(Y))^2);

% Adjusted R^2
MeanSq_Res_X=Res_SSQ2_X/(numel(X1)-p);
MeanSq_Res_Z=Res_SSQ2_Z/(numel(z1)-p);
MeanSq_Total=(Y'*Y-numel(X1)*(mean(Y))^2)/(numel(X1)-1);

AdjR2_X=1-MeanSq_Res_X/MeanSq_Total;
AdjR2_Z=1-MeanSq_Res_Z/MeanSq_Total;
