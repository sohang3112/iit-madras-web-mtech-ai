% Here is the complete MATLAB implementation of the PLSR algorithm using the NIPALS method, followed by a practical example to demonstrate how it works.
% MATLAB Function: plsr_nipals.m
% This function takes the predictor matrix X, response matrix Y, and the desired number of components A as inputs. 
% It returns the regression coefficients Beta, along with the scores, loadings, and weights.
% Matlab
function [Beta, T, P, W, Q, U,B] = plsr_nipalsm(X, Y, A)

%global b

    % PLSR_NIPALS Partial Least Squares Regression via NIPALS algorithm.
    %
    % Inputs:
    %   X - Predictor matrix (n x p)
    %   Y - Response matrix (n x m)
    %   A - Number of latent components to extract
    %
    % Outputs:
    %   Beta - Final regression coefficients for scaled/centered data (p x m)
    %   T    - X-scores (n x A)
    %   P    - X-loadings (p x A)
    %   W    - X-weights (p x A)
    %   Q    - Y-loadings (m x A)
    %   U    - Y Scores  (m x A)
    %   B    - Diagonal Element (ax1)

    [n, p] = size(X);
    [~, m] = size(Y); % ignored number of rows
    
    % Step 1: Center and scale the data (Z-score normalization)
    % X0 = (X - mean(X)) ./ std(X);
    % Y0 = (Y - mean(Y)) ./ std(Y);

    % Step 1: Do NOT Center  the data 
    X0 = (X - 0*mean(X)) ./ 1;
    Y0 = (Y - 0*mean(Y)) ./ 1;

    

   % [X0   Y0]
    
    % Pre-allocate matrices for storage
    T = zeros(n, A);
    P = zeros(p, A);
    W = zeros(p, A);
    Q = zeros(m, A);
    U = zeros(n, A);
    B = zeros(A,A);
    
    max_iter = 500;
    tolerance = 1e-6;
    
    % Step 2: Iterative Loop for Each Component
    for h = 1:A
        % 2.1 Initialize Y-score u with a column of Y0
        u = Y0(:, 1);

        u_old = zeros(n, 1);
        
        for iter = 1:max_iter

           
            % 2.2 Compute and normalize X-weights (w)
           

         
          
           w = (X0' * u) / (u' * u);  % X0 is same as E0
         
         
            w = w / norm(w);
            
            % Component 1 weights 

            

            % 2.3 Compute X-scores (t)
            t = X0 * w/(w'*w);

            % iter
            % 
            % [t]
            
            % 2.4 Compute Y-weights/loadings (q)
            q = (Y0' * t) / (t' * t);

            q=q/norm(q);

% iter
             % q  % Check
            
            % 2.5 Update Y-scores (u) Most Important Step
            u = (Y0 * q) / (q' * q);


            % iter
            % 
            % u
           
         %  [ t u] % check t and u values for convergence

          %  u
            % 2.6 Check for convergence of the score vector
            if norm(u - u_old) < tolerance
                break;
            end
            u_old = u;
              % u

        end
        
        % 2.7 Compute X-loadings (p)

        p = (X0' * t) / (t' * t);
        t = t*norm(p);
        pprime=p'/norm(p);
        p=pprime';

       
        % Store the results for component h
        T(:, h) = t;
        P(:, h) = p;
        W(:, h) = w;
        Q(:, h) = q;
        U(:,h) = u;
        b=t'*u/(t'*t);

        B(h,h) = b;
         
   %  b=1;



        % 2.8 Deflate X0 and Y0 matrices
       

        
        X0 = X0 - t * p';

        t*p';

        t*q';

        
        Y0 = Y0 - t*b * q'; % Using inner relation: Y0 = Y0 - b*t*q' (where b=1 for normalized t)

        % X0
        % 
        % Y0
        
    end
    
    % Step 3: Compute final regression coefficients (Beta)
    % Transform weights to be compatible with original un-deflated X
    W_star = W * inv(P' * W); 
  %  Beta = W_star * Q';
    Beta = W_star *B* Q';
end
