function bmap = edgeOrientedFilters(im)

im_size = size(im);

binary_edge = edge(rgb2gray(im), 'canny');
[mag, theta] = orientedFilterMagnitude(im);
bmap = zeros(size(mag));

for y = 1:im_size(1)
    for x = 1:im_size(2)
        if binary_edge(y, x) == 1
            bmap(y, x) = mag(y, x);
        end
    end
end

% figure;
% subplot(1, 2, 1);
% imshow(im);
% subplot(1, 2, 2);
% imshow(bmap);
%imshow(bmap);