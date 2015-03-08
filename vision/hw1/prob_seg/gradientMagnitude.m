function [mag, theta] = gradientMagnitude(im, sigma)

im_size = size(im);
gauss_filter = fspecial('gaussian', 7, sigma);

smoothed_im = imfilter(im, gauss_filter);

x_grad = imfilter(smoothed_im, [0 0 0; 1 0 -1; 0 0 0]);
y_grad = imfilter(smoothed_im, [0 1 0; 0 0 0; 0 -1 0]);

mag = zeros(im_size);
max_mag = zeros(im_size(1), im_size(2));
theta = zeros(im_size(1), im_size(2));

for y = 1:im_size(1)
    for x = 1:im_size(2)
        mag(y, x, 1) = (x_grad(y, x, 1)^2 + y_grad(y, x, 1)^2)^(1/2);
        mag(y, x, 2) = (x_grad(y, x, 2)^2 + y_grad(y, x, 2)^2)^(1/2);
        mag(y, x, 3) = (x_grad(y, x, 3)^2 + y_grad(y, x, 3)^2)^(1/2);
        max_mag(y, x) = max([mag(y, x, 1),mag(y, x, 2),mag(y, x, 3)]);
        if max_mag(y, x) == mag(y, x, 1)
            theta(y, x) = atan2(-y_grad(y, x, 1), x_grad(y, x, 1));
        elseif max_mag(y, x) == mag(y, x, 2)
            theta(y, x) = atan2(-y_grad(y, x, 2), x_grad(y, x, 2));
        else
            theta(y, x) = atan2(-y_grad(y, x, 3), x_grad(y, x, 3));
        end
    end
end

%figure;
%subplot(1, 2, 1);
%imshow(max_mag);
%subplot(1, 2, 2);
%imshow(theta);

mag = max_mag;