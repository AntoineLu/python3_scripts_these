function y = FittingFunction5(x,A,n)
% FittingFuction(x,A) takes as entry a vector A of parameters and results
% the magnitude of the magnetic field created by the n=5 coils.
% Here, we have 5 parameters such that A = [I1�...�I5].
% x is a position on the group of coil's axis (x between -0.7 and -2�m)
% to use the function with a vector x, use the following arrayfun(@(y)FittingFunction5(y,A,n),x)
% Position of the coils : [-0.3 -1 -1.6 -1.8 -2.3] m
global posBob z_bob
posBob = [0.3 1 1.6 1.8 2.3];

if ~isvector(A) || length(A)~=n
    error('The input vector of parameters should be of length %d',n)
end

%importation de la carte de champs des bobines
importMat = csvread('champsBobines.csv',4,0);
z_bob = -importMat(1:102,1);
B_1 = importMat(1:102,4);
B_2 = importMat(1:102,12);
B_3 = importMat(1:102,20);
B_4 = importMat(1:102,28);
B_5 = importMat(1:102,36);

if x < z_bob(1) || x > z_bob(length(z_bob)) %a voir peut-�tre a changer
    error('Position not in bounds.')
end

precision = z_bob(2) - z_bob(1); %pr�cision du de chaque pas
for i=1:length(z_bob)
    if x == z_bob(i)
        %disp('egal')
        y = A(1)*B_1(i) + A(2)*B_2(i) + A(3)*B_3(i) + A(4)*B_4(i) + A(5)*B_5(i);
    elseif x > z_bob(i) && x < z_bob(i)+precision %si compris dans l'intervalle, on prend la valeur de la borne inf�rieure
        y = A(1)*B_1(i) + A(2)*B_2(i) + A(3)*B_3(i) + A(4)*B_4(i) + A(5)*B_5(i);
        %disp('non egal')
    else
        
    end
end