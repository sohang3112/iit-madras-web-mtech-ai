
% run the NIPALS PLSR function, and use the output coefficients to predict new observations.

% SUCCESS
clear; clc;

%% 1. X and Y Data

n = 5;  % Number of samples
p = 6;   % Number of predictors

n = 10;  % Number of samples
p = 5;   % Number of predictors



X = [-1.037	0.604	-1.561	-2.472	1.297
2.145	0.513	0.396	2.527	-2.35
1.021	0.134	0.55	1.697	-1.417
0.442	0.889	-1.431	-1.024	-0.233
-1.599	-0.758	-0.519	-1.783	1.869
-1.604	-0.485	-0.359	-2.028	1.648
-1.993	-0.864	0.407	-1.656	2.051
1.427	1.021	-0.698	0.703	-1.355
0.224	0.413	-0.438	-0.032	-0.395
0.637	0.917	-1.43	-0.547	-0.378
]; 
Y= [ 0.305	-2.018	-0.745
0.774	2.835	0.096
0.298	2.028	-0.245
0.939	-0.94	-1.011
-0.715	-2.259	0.167
-0.678	-1.733	0.126
-1.399	-1.742	0.905
1.328	0.752	-0.889
0.487	0.075	-0.552
1.034	-0.478	-1.303
];





%% 2. Run PLSR NIPALS Algorithm
num_components = 3; % Extracting 2 latent variables
[Beta, T, P, W, Q,U,B] = plsr_nipalsm(X, Y, num_components);

XPRED = T*P';
YPRED  =T*B*Q'  ;
%Beta = W_star *b* Q';`

% Beta_W = W*inv(W'*W)*B*Q';
Beta_P = W*inv(P'*W)*B*Q';

% Betas = [Beta_W  Beta_P];

% YPRED_W =X*Beta_W;
YPRED_P =X*Beta_P;

%YPREDs = [YPRED_W  YPRED_P];


% Predict new observations using the PLSR model
% YPRED_NEWW = XNEW * Beta_W;  % Using Beta_W for predictions
% YPRED_NEWP = XNEW * Beta_P;  % Using Beta_W for predictions

%YPRED_NEW=[YPRED_NEWW YPRED_NEWP];

% PRESS calculations

% Leave-one-out PRESS for PLS2
%---------------------------------------------------

n = size(X,1);
q = size(Y,2);

YPRED = zeros(size(Y));
TotalResid = 0;
ResidSq =0;
for i = 1:n

    
    idx = true(n,1);
    idx(i)=false;

    Xtrain = X(idx,:);
    Ytrain = Y(idx,:);

% i, Xtrain, Ytrain

%[Beta, T, P, W, Q,U,B] = plsr_nipalsm(X, Y, num_components);
    [Beta_Train, Tnew, Pnew, Wnew, Qnew,Unew,Bnew] = plsr_nipalsm(Xtrain, Ytrain, num_components);
 %   i, Beta_Train
%    model = pls2_nipals(Xtrain,Ytrain,A);

      YPRED(i,:) = X(i,:)*Beta_Train;
 
    % YPRED = X*Beta_Train;
% i, YPRED

%sum=0;
    
   % Ypred(i,:) = predict_pls2(model,X(i,:));
end

for j=1:q

    %  i,  j, Y(:,j), YPRED(:,j),  (Y(:,j)-YPRED(:,j)).^2



        ResidSq = ResidSq+(Y(:,j)-YPRED(:,j))'*(Y(:,j)-YPRED(:,j));
end 
      
PRESS = ResidSq;
RMSECV = sqrt(PRESS/((n-1)*q));




%PRESS = sum(Residual(:).^2);

%RMSECV = sqrt(PRESS/(n*q));

