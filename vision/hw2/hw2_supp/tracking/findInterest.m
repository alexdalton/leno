function points = findInterest(img,w,N)
%w = 10 (window size), N = 40(# of interest points)
%Computes a covarient matrix of the gradients of an image 
orig = img;
img = double(img);
[m n ] = size(img);

[dx dy] = gradient(img);
Ix2 = dx.^2;
Iy2 = dy.^2;
IxIy = dx.*dy;

mask = ones(w);
% mask = fspecial('gaussian',w,.5);
SigX2 = imfilter(Ix2,mask);
SigY2 = imfilter(Iy2,mask);
SigXY = imfilter(IxIy,mask);

K = 25^-1;
xbound = 25;
ybound = 25;

H = SigX2.*SigY2-SigXY.^2 - K*(SigX2+SigY2).^2;
H = abs(H);
for i=1:N
    [y1 iR] = max(H);
    [y2 iC] = max(y1);
    if iR(iC) > xbound & iR(iC) < m-xbound & iC > ybound & iC < n-ybound %make sure to not exceed img size
        H(iR(iC)-xbound:iR(iC)+xbound,iC-ybound:iC+ybound)=0;
    else
        xF = max((iR(iC)-xbound),1);
        xE = min(m,(iR(iC)+xbound));
        yF = max((iC-ybound),1);
        yE = min(n,(iC+ybound));
        H(xF:xE,yF:yE) = 0;
    end;
    
    H(iR,iC)=0;
    points(i,1) = iR(iC);
    points(i,2) = iC;
    points(i,3) = y2;
end
points(:,3) = points(:,3)/max(points(:,3));
% hold off
% imshow(orig)
% hold on
% scatter(points(:,2),points(:,1))