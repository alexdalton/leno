function T = align_shape(im1, im2)

tic;
[y1, x1] = find(im1);
[y2, x2] = find(im2);

cmX1 = mean(x1);
cmY1 = mean(y1);
cmX2 = mean(x2);
cmY2 = mean(y2);

dX = cmX2 - cmX1;
dY = cmY2 - cmY1;

X = zeros(size(x1, 1) * 2,6);
X(1:2:end, 1) = x1;
X(2:2:end, 4) = x1;
X(1:2:end, 2) = y1;
X(2:2:end, 5) = y1;
X(1:2:end, 3) = 1;
X(2:2:end, 6) = 1;

T = [1; 0; dX; 0; 1; dY];

for iterations = 1:40
    xPrime = X * T;
    
    x1 = xPrime(1:2:end);
    y1 = xPrime(2:2:end);
    X(1:2:end, 1) = x1;
    X(2:2:end, 4) = x1;
    X(1:2:end, 2) = y1;
    X(2:2:end, 5) = y1;
    X(1:2:end, 3) = 1;
    X(2:2:end, 6) = 1;
    
    A = pdist2([x1, y1], [x2, y2]);
    
    [~, index] = min(A, [], 2);
    xClosest = zeros(size(index, 1), 1);
    yClosest = zeros(size(index, 1), 1);
    for i = 1:size(index,1)
        xClosest(i) = x2(index(i));
        yClosest(i) = y2(index(i));
    end
    b = zeros(2 * size(xClosest, 1), 1);
    b(1:2:end) = xClosest;
    b(2:2:end) = yClosest;
    
    T = X \ b;
    
end
toc

T = [T(1), T(2), T(3); T(4), T(5), T(6)];
aligned = getAligned(T, im1, x1, y1);
dispim = displayAlignment(im1, im2, aligned, true);
imagesc(dispim);
evalAlignment(aligned, im2)