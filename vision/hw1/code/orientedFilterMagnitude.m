function [mag, theta] = orientedFilterMagnitude(im)

dim = 15;
radius = floor(dim / 2) + 1;
filter = zeros(dim, dim);
filter_size = size(filter);
im_size = size(im);

sigma = 2;
total = 0;
for y = 1:filter_size(1)
    for x = 1:filter_size(2)
        filter(y, x) = exp(-(  ((x-radius)^2 + 6*(y-radius)^2) / (2 * sigma^2) ));
        total = total + filter(y, x);
    end
end

for y = 1:filter_size(1)
    for x = 1:filter_size(2)
        filter(y, x) = filter(y,x) / total;
    end
end


[fx, fy] = gradient(filter);
out1 = imfilter(im, fy);
out2 = imfilter(im, imrotate(fy, 45 ));
out3 = imfilter(im, imrotate(fy, 90));
out4 = imfilter(im, imrotate(fy, 135));

[mapMaxVal1, mapMaxInd1] = max(abs(out1), [], 3);
[mapMaxVal2, mapMaxInd2] = max(abs(out2), [], 3);
[mapMaxVal3, mapMaxInd3] = max(abs(out3), [], 3);
[mapMaxVal4, mapMaxInd4] = max(abs(out4), [], 3);

theta = zeros(im_size(1), im_size(2));
mag = zeros(im_size(1), im_size(2));
for y = 1:im_size(1)
    for x = 1:im_size(2)
        mag(y, x) = max([mapMaxVal1(y, x), mapMaxVal2(y, x), mapMaxVal3(y, x), mapMaxVal4(y, x)]);
        theta(y, x) = atan2(-mapMaxVal3(y,x), mapMaxVal1(y, x));
    end
end

% figure;
% subplot(1, 5, 1);
% imshow(out1);
% subplot(1, 5, 2);
% imshow(out2);
% subplot(1, 5, 3);
% imshow(out3);
% subplot(1, 5, 4);
% imshow(out4);
% subplot(1, 5, 5);
% imshow(mag);
% 
% figure;
% subplot(1, 4, 1);
% imagesc(fy);
% colormap gray;
% axis image;
% 
% subplot(1, 4, 2);
% imagesc(imrotate(fy, 45, 'crop' ));
% colormap gray;
% axis image;
% 
% subplot(1, 4, 3);
% imagesc(imrotate(fy, 90, 'crop' ));
% colormap gray;
% axis image;
% 
% subplot(1, 4, 4);
% imagesc(imrotate(fy, 135, 'crop' ));
% colormap gray;
% axis image;