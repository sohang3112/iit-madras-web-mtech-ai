clear all
clc

A= [ 1     4
     2     5
     3     6];
sA=size(A);
B=A';
% B =
% 
%      1     2     3
%      4     5     6
sB = size(B);
C=A*A';
sC=size(C);

% C =
% 
%     17    22    27
%     22    29    36
%     27    36    45

D=A'*A;

% D =
% 
%     14    32
%     32    77

out =[sA sB sC];

% out =
% 
%      3 x 2     2 x 3     3 x 3

M = [
     1     2
     3     4 ];
DeterminantM = det(M);
InvM = inv(M);
Check = M*InvM;

% InvM =
% 
%    -2.0000    1.0000
%     1.5000   -0.5000


% Find eigenvalues and eigenvectors of Matrix D

% D =
% 
%     14    32
%     32    77

[eve eva]=eig(D); % eva = eigenvalue  eve = eigenvector

% eva =
% 
%     0.5973         0
%          0   90.4027

% eve =
% 
%    -0.9224    0.3863
%     0.3863    0.9224

% Features of positive definite matrix

PDM = [ 2 -1 0
       -1 2 -1
        0 -1 2];

[evePDM  evaPDM] = eig(PDM);
determinant_PDM = det(PDM);
Symmetric_PDM   = PDM';

% eigenvectors of PDM are
% 

% evePDM =
% 
%     0.5000   -0.7071   -0.5000
%     0.7071    0.0000    0.7071
%     0.5000    0.7071   -0.5000

% eigenvalues of PDM are

% evaPDM =
% 
%     0.5858         0         0
%          0    2.0000         0
%          0         0    3.4142

% Determinant of PDM are 
 % det(PDM) = 4

% Symmetric PDM' = PDM

out_PDM =[PDM  PDM'];

% out_PDM =

    %  2    -1     0          2    -1     0
    % -1     2    -1         -1     2    -1
    %  0    -1     2          0    -1     2
    % 
    % Both PDM and PDM' are the same

% Inverse of PDM exists
PDM_Inv = inv(PDM);

% PDM_Inv =
% 
%     0.7500    0.5000    0.2500
%     0.5000    1.0000    0.5000
%     0.2500    0.5000    0.7500

% Note the inverse of PDM is also symmetric just like PDM itself


% u'PDMu>0;

u=[-1 -1 -1]';

uTPDMu = u'*PDM*u;

% uTPDMu = 2

% Diagonal entries are positive

diagonal_PDM = diag(diag(PDM));

% Cholesky Lower (L) and Upper (U) Triangular Decompositions 
% 1. Upper Triangular Factor (R)
R = chol(PDM);
% Result: R'*R equals PDM



% R =
% 
%     1.4142   -0.7071         0
%          0    1.2247   -0.8165
%          0         0    1.1547
% 
% R'*R =
% 
%     2.0000   -1.0000         0
%    -1.0000    2.0000   -1.0000
%          0   -1.0000    2.0000

% Lower Triangular Factor (L)

L = chol(PDM, 'lower');

% L =
% 
%     1.4142         0         0
%    -0.7071    1.2247         0
%          0   -0.8165    1.1547


% Result: L*L' equals PDM


% L*L'
% 
% ans =
% 
%     2.0000   -1.0000         0
%    -1.0000    2.0000   -1.0000
%          0   -1.0000    2.0000

% Orthogonal Matrices

OGM1 = [1/sqrt(2) -1/sqrt(2)
        1/sqrt(2) 1/sqrt(2)];

%	Square matrix (equal number of rows and columns)
% Order_OGM1 = size(OGM1);
% 
% b)	Matrix columns and rows are orthonormal

ONC1= norm(OGM1(:,1));
ONC2= norm(OGM1(:,2));
ONR1= norm(OGM1(1,:));
ONR2= norm(OGM1(2,:));

out_ON=[ONC1 ONC2 ONR1 ONR2];

% out_ON =     1.0000    1.0000    1.0000    1.0000




% c)	Transpose = Inverse i.e., 
% OGM′=inv(OGM)

out_TI =[OGM1' inv(OGM1)];

%out_TI =
   %  0.7071    0.7071         0.7071    0.7071
   % -0.7071    0.7071        -0.7071    0.7071



% Such that
% OGM*OGM′=I

IsitI = OGM1*OGM1';

% IsitI =
% 
%     1.0000         0
%          0    1.0000

% YES 

% d)	 Columns and rows are having unit length

% Already checked above see b)

% e)	Dot product of different rows  = 1 if rows are same
%        Dot product of different rows  = 0 if rows are not same

norows=numel(OGM1(:,1));

for i=1:norows % number of elements in first column of OGM1
    
    
    for j= 1:norows
    prod_rows(i,j) = (OGM1(i,:))*(OGM1(j,:))';

    
    end
end

% prod_rows =

    % 1.0000         0
    %   0         1.0000

% e)	Dot product of different columns  = 1 if columns are same
%       Dot product of different columns  = 0 if columns are not same

nocolumns=numel(OGM1(1,:));

for i=1:nocolumns % number of elements in first row of OGM1
        
    for j= 1:nocolumns
    
        prod_columns(i,j) = (OGM1(:,i))'*(OGM1(:,j));

    
    end
end

% prod_columns =
%      1.0000     0
%          0    1.0000

% f)	Dot product of different rows = 0  See above
% g)	 Determinant of OGM = -1 or +1

         Determinant_OGM1 =det(OGM1);

 % Determinant_OGM1 =  1.0000

% h)	 When you multiply two orthogonal matrices you get the resulting matris also as orthogonal

% Let us multiply  OGM1 with itself

OGM11 = OGM1*OGM1;
    %    0   -1.0000
    % 1.0000         0

IsitI2 = OGM11'*OGM11;  % Is it identity matrix?

% IsitI2 =
% 
%     1.0000         0
%          0    1.0000

% i)	Orthogonal matrices preseve the length of vectors.  
% If we apply an orthogonal matrix OGM  on vector a to get vector b then both a and b have the same length. 
%  Hence the vectors are neither contracted or expanded upon transformations using the orthogonal matrix.
% 
a=[-10 +20]';
length_a=norm(a);
b= OGM1*a; 
length_b=norm(b);

% a =
% 
%    -10
%     20
% 
% b =
% 
%   -21.2132
%     7.0711
% 
% 
% 
% length_a = 22.3607
% 
% length_b = 22.3607

% Angles are preserved in orthogonal transformation

% Let OGM1 apply on any two vectors c and d

c=[1 -4 7];
d=[-7 2 5];

% Finding angle between two vectors

% Angle in radians
theta = atan2(norm(cross(c,d)), dot(c,d));
% Angle in degrees
theta_deg_cd = rad2deg(theta);

% The angles between vectors c and d is theta_deg = 73.8145

% Let us now apply orthogonal transformation on vectors c and d
% simultaneously to get new two vectors c2 and d2

% Define a new orthogonal matrix OGM3 of size 3x3

OGM3 = [1/3 2/3 2/3; 2/3 1/3 -2/3; 2/3 -2/3 1/3];

% OGM3 =
% 
%     0.3333    0.6667    0.6667
%     0.6667    0.3333   -0.6667
%     0.6667   -0.6667    0.3333


NewMatrix_cd = OGM3*[c' d'];

% NewMatrix_cd =
% 
%     2.3333    2.3333
%    -5.3333   -7.3333
%     5.6667   -4.3333

c2 = NewMatrix_cd(:,1)';
d2 = NewMatrix_cd(:,2)';

% Angle in radians
theta = atan2(norm(cross(c2,d2)), dot(c2,d2));
% Angle in degrees
theta_deg_c2d2 = rad2deg(theta);
compare_angles =[theta_deg_cd   theta_deg_c2d2];

% compare_angles =    73.8145   73.8145  

% Angles are preserved even after orthogonal transformation just as lengths
% :)

