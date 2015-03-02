function aligned = getAligned(T, im, x1, y1)
[height, width] = size(im);

%[y1, x1] = find(im);
aligned = zeros(size(im));

for i = 1:size(y1, 1)
    xyPrime = T * [x1(i); y1(i); 1];
    if round(xyPrime(1)) > 0 && round(xyPrime(1)) <= width && round(xyPrime(2)) > 0 && round(xyPrime(2)) <= height
        aligned(round(xyPrime(2)), round(xyPrime(1))) = 1;
    end
end