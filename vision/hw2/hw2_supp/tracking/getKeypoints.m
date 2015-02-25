% tau = .0000015 is good
function [keyXs, keyYs] = getKeypoints(im, tau)

im_size = size(im);

filter = fspecial('gaussian', 7, 1);
[Ix, Iy] = gradient(im2double(im));

Ix2 = imfilter(Ix.^2, filter);
Iy2 = imfilter(Iy.^2, filter);
Ixy = imfilter(Ix.*Iy, filter);

detM = Ix2.*Iy2 - Ixy.^2;
traceM = Ix2 + Iy2;

Mc = detM - .04 * traceM.^2;

maxes = ordfilt2(Mc, 25, ones(5, 5));
figure;
imshow(im);
keyXs = [];
keyYs = [];
for y = 1:im_size(1)
    for x = 1 :im_size(2)
        if (Mc(y, x) ~= maxes(y, x)) || Mc(y, x) < tau
            Mc(y, x) = 0;
        else
            keyXs(end + 1) = x;
            keyYs(end + 1) = y;
        end
    end
end

imshow(im);
hold on;
plot(keyXs, keyYs, 'g.', 'linewidth', 3);