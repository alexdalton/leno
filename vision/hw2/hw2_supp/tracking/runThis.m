warning('off','all')
[keyXs, keyYs] = getKeypoints(im2double(imread('images\hotel.seq0.png')), .0000005);

newXs = zeros(50, size(keyXs, 2));
newYs = zeros(50, size(keyYs, 2));
newXs(1, :) = keyXs;
newYs(1, :) = keyYs;

for i = 1:50
    im0_name = sprintf('images\\hotel.seq%d.png', i - 1);
    im1_name = sprintf('images\\hotel.seq%d.png', i);
    im0 = im2double(imread(im0_name));
    im1 = im2double(imread(im1_name));
    [newXs(i + 1, :), newYs(i + 1, :)] = predictTranslationAll(newXs(i, :), newYs(i, :), im0, im1);
end

figure;
imshow(imread('images\hotel.seq0.png'));
hold on;
rands = randi([1,size(keyXs, 2)], 1, 20);
for i = 1:size(keyXs, 2) - 1
    plot(newXs(1:51, rands(i)), newYs(1:51, rands(i)));
end

figure;
imshow(imread('images\hotel.seq0.png'));
hold on;
for i = 1:size(keyXs, 2) - 1
    for j = 1:51
        if (newXs(j, i) < 10) || (newXs(j, i) > 502) || (newYs(j, i) < 10) || (newYs(j, i) > 470)
            plot(newXs(1,i), newYs(1, i), 'g.', 'linewidth', 3);
        end
    end
end