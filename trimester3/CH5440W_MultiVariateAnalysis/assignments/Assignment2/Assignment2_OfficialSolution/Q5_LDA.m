%% CH5440W Assignment 2 - Question 5: Linear Discriminant Analysis
%  Pruthwiraj Lenka
clear; clc;

%% ---- 1. Load data (paste/import from DataforQuestion5.xlsx) ----
% Group 1 training points (F1, F2)
G1 = [ -0.0056 -0.1657;  -0.1698 -0.1585;  -0.3469 -0.1879;  -0.0894  0.0064;
       -0.1679  0.0713;  -0.0836  0.0106;  -0.1979 -0.0005;  -0.0762  0.0392;
       -0.1913 -0.2123;  -0.1092 -0.1190;  -0.5268 -0.4773;  -0.0842  0.0248;
       -0.0225 -0.0580;   0.0084  0.0782;  -0.1827 -0.1138;   0.1237  0.2140;
       -0.4702 -0.3099;  -0.1519 -0.0686;   0.0006 -0.1153;  -0.2015 -0.0498;
       -0.1932 -0.2293;   0.1507  0.0933;  -0.1259 -0.0669;  -0.1551 -0.1232;
       -0.1952 -0.1007;   0.0291  0.0442;  -0.2280 -0.1710;  -0.0997 -0.0733;
       -0.1972 -0.0607;  -0.0867 -0.0560];

% Group 2 training points (F1, F2)
G2 = [ -0.3478  0.1151;  -0.3618 -0.2008;  -0.4986 -0.0860;  -0.5015 -0.2984;
       -0.1326  0.0097;  -0.6911 -0.3390;  -0.3608  0.1237;  -0.4535 -0.1682;
       -0.3479 -0.1721;  -0.3539  0.0722;  -0.4719 -0.1079;  -0.3610 -0.0399;
       -0.3226  0.1670;  -0.4319 -0.0687;  -0.2734 -0.0020;  -0.5573  0.0548;
       -0.3755 -0.1865;  -0.4950 -0.0153;  -0.5107 -0.2483;  -0.1652  0.2132;
       -0.2447 -0.0407;  -0.4232 -0.0998;  -0.2375  0.2876;  -0.2205  0.0046;
       -0.2154 -0.0219;  -0.3447  0.0097;  -0.2540 -0.0573;  -0.3778 -0.2682;
       -0.4046 -0.1162;  -0.0639  0.1569;  -0.3351 -0.1368;  -0.0149  0.1539;
       -0.0312  0.1400;  -0.1740 -0.0776;  -0.1416  0.1642;  -0.1508  0.1137;
       -0.0964  0.0531;  -0.2642  0.0867;  -0.0234  0.0804;  -0.3352  0.0875;
       -0.1878  0.2510;  -0.1744  0.1892;  -0.4055 -0.2418;  -0.2444  0.1614;
       -0.4784  0.0282];

% Test data (F1, F2)
Test = [-0.112 -0.279; -0.059 -0.068;  0.064  0.012; -0.043 -0.052; -0.050 -0.098;
        -0.094 -0.113; -0.123 -0.143; -0.011 -0.037; -0.210 -0.090; -0.126 -0.019];

n1 = size(G1,1);   n2 = size(G2,1);

%% ---- (a) Variance (covariance) matrix for each class ----
mu1 = mean(G1)';           % 2x1
mu2 = mean(G2)';           % 2x1
S1  = cov(G1);              % uses (n-1) denominator, MATLAB default
S2  = cov(G2);

disp('S1 ='); disp(S1);
disp('S2 ='); disp(S2);

%% ---- (b) Pooled covariance ----
Sp = ((n1-1)*S1 + (n2-1)*S2) / (n1+n2-2);
disp('Sp (pooled) ='); disp(Sp);

%% ---- (c) Linear classification equation (cost ratio = prior ratio = 1) ----
Sp_inv = inv(Sp);
w = Sp_inv*(mu1-mu2);                       % 2x1 coefficient vector
c = 0.5*(mu1+mu2)'*Sp_inv*(mu1-mu2);        % scalar threshold term

fprintf('Discriminant function: d(x) = %.4f*F1 + %.4f*F2 - %.4f\n', w(1), w(2), c);
fprintf('Classify as Group 1 if d(x) > 0, else Group 2\n');

%% ---- (d) Classify training data / find misclassified points ----
d1 = G1*w - c;                 % should be > 0 for correct Group-1 classification
cls1 = ones(n1,1);  cls1(d1<=0) = 2;
mis1 = find(cls1 ~= 1);
fprintf('\nGroup 1 misclassified points (row index): '); disp(mis1');

d2 = G2*w - c;                 % should be < 0 for correct Group-2 classification
cls2 = 2*ones(n2,1); cls2(d2>0) = 1;
mis2 = find(cls2 ~= 2);
fprintf('Group 2 misclassified points (row index): '); disp(mis2');

fprintf('Total misclassified = %d / %d  (accuracy = %.2f%%)\n', ...
     numel(mis1)+numel(mis2), n1+n2, 100*(1-(numel(mis1)+numel(mis2))/(n1+n2)));

%% ---- (e) Classify the new test data ----
dt = Test*w - c;
clst = ones(size(Test,1),1); clst(dt<=0) = 2;
disp('Test point classification (1 = Group1, 2 = Group2):');
disp([Test clst dt]);
