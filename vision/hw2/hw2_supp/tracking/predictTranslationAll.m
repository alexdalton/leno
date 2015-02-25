function [newXs, newYs] = predictTranslationAll(startXs, startYs, im0, im1)

[Ix, Iy] = gradient(im0);

newXs = zeros(size(startXs));
newYs = zeros(size(startYs));

for ptNum = 1:size(startXs, 2)
    [newXs(ptNum), newYs(ptNum)] = predictTranslation(startXs(ptNum), startYs(ptNum), Ix, Iy, im0, im1);
end