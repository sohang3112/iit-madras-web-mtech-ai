clear all; clc;

Data = [ 
1	10	4
2	10	5
3	11	7
4	12	11
5	13	12
6	14	14
7	15	17
8	16	18
9	17	16
10	18	15
11	20	12
];
SlNo =Data(:,1);
Speed = Data(:,2);
Luggages = Data(:,3);
X= [ ones(numel(Speed),1) Speed Speed.^2];
% X =
% 
%      1    10   100
%      1    10   100
%      1    11   121
%      1    12   144
%      1    13   169
%      1    14   196
%      1    15   225
%      1    16   256
%      1    17   289
%      1    18   324
%      1    20   400
Y=Luggages;
beta_hat = inv(X'*X)*(X'*Y);
% beta_hat =
% 
%   -67.1947
%    10.2919
%    -0.3164  

Y_Pred = X*beta_hat;
Compare = [SlNo Y Y_Pred];

% Compare =
% 
%     1.0000    4.0000    4.0807
%     2.0000    5.0000    4.0807
%     3.0000    7.0000    7.7275
%     4.0000   11.0000   10.7414
%     5.0000   12.0000   13.1224
%     6.0000   14.0000   14.8706
%     7.0000   17.0000   15.9859
%     8.0000   18.0000   16.4684
%     9.0000   16.0000   16.3180
%    10.0000   15.0000   15.5347
%    11.0000   12.0000   12.0696

% Fit seems real nice

% find average of Y and average of Y_Pred : 11.9091 (Both are same)

Average_Ys = [mean(Y) mean(Y_Pred)];

% What is sum of residuals?

Residual_Sum=sum(Y-Y_Pred); % Pretty much zero

% What is total sum of squares -TSSQ

% Two ways - 1. Simply Y'Y or 2. sum over Y^2_i

TtSSQ1 = Y'*Y;
TtSSQ2 = sum(Y.^2);  % element by element squaring of terms

TtSSQ_Compare = [ TtSSQ1  TtSSQ2];

% TSSQ_Compare = 1789        1789  Both methods gave same answer

% Let us find Regression SSQ RsSSQ1

RgSSQ1 = beta_hat'*X'*Y; % 1781.8

% Let us find Residuals Sum of Squares by 2 methods 1.RsSSQ1  or  2. RsSSQ2

RsSSQ1 = (Y-X*beta_hat)'*(Y-X*beta_hat);
RsSSQ2 =  sum((Y-Y_Pred).^2);

% Compare the two Residual SSQ

Compare_RsSSQ = [ RsSSQ1  RsSSQ2];

% Compare_RsSSQ = [7.2316    7.2316]  Both approaches give the same
% Residual Sum of Squares

% Check if Total Sum of Squares = 
% Regression Sum of Squares + Residual Sum of Squares

Total_SSQ =  RgSSQ1+RsSSQ1; % Regression SSQ + Residual SSQ

TotalSSQ_Compare = [TtSSQ1 Total_SSQ]; % Both are 1789

% Regression Sum of Squares = 1781.7684;
% Residual Sum of Squares   = 7.2316;
% Total of the above two    = 1789.0
% 
% Find optimal conveyor belt speed

x_opt = -(1/2)*(beta_hat(2)/beta_hat(3));

y_opt = [1 x_opt x_opt^2]*beta_hat;

% Now let us do the inferior First Order Model Fit

% X= [ ones(numel(Speed),1) Speed Speed.^2];  Original Model

X_First = [ ones(numel(Speed),1) Speed ]; % Reduced Model
beta_hat_First = inv(X_First'*X_First)*(X_First'*Y);



Total_SSQ =Y'*Y;

RegSSQ_First = beta_hat_First'*X_First'*Y;

Y_Pred_First = X_First*beta_hat_First; % Predictions

ResSSQ_First = (Y-Y_Pred_First)'*(Y-Y_Pred_First);

Compare_AllSQ_First = [RegSSQ_First ResSSQ_First Total_SSQ];

% Demonstrating polyfit in Matlab  % TA may find equivalent code in Python

[pLinear,SLinear] = polyfit(Speed,Luggages,1)
eqLinear = "Linear: " + pLinear(2) +  "  + "+pLinear(1) + "x  " 

[pQuad,SQuad] = polyfit(Speed,Luggages,2)

eqQuad = "Quadratic: " + pQuad(3) + "  + " + pQuad(2) + "x + " + pQuad(1) + "x^2  "  

xQuery = [0:1:20]';
yLinear = polyval(pLinear,xQuery);
yQuad = polyval(pQuad,xQuery);

scatter(Speed,Luggages)
hold on
plot(xQuery,yLinear,"-")
plot(xQuery,yQuad,"--")
hold off

xlabel("Belt Speed cm/s")
ylabel("Luggages Number/min")
legend(["Sample data" "Linear model" "Quadratic model"])
text(0.3,30,[eqLinear eqQuad])