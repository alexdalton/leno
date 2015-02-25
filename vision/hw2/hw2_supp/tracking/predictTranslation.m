function [newX, newY] = predictTranslation(startX, startY, Ix, Iy, im0, im1)

wsize = 7;  
numIterations = 40;
threshold = .1;

[xCoords, yCoords] = meshgrid(startX - wsize : startX + wsize, startY - wsize : startY + wsize);

im0_interp = interp2(im0, xCoords, yCoords);
im1_interp = interp2(im1, xCoords, yCoords);

Ix_interp = interp2(Ix, xCoords, yCoords);
Iy_interp = interp2(Iy, xCoords, yCoords);

sumIxIx = sum(sum(Ix_interp.^2));
sumIxIy = sum(sum(Ix_interp.*Iy_interp));
sumIyIy = sum(sum(Iy_interp.^2));
M = [sumIxIx, sumIxIy;sumIxIy, sumIyIy];

oldVal = sum(sum((im1_interp - im0_interp).^2));
stopVal = 3000;

newX = 0;
newY = 0;

for i = 1:numIterations
    if stopVal < threshold
        break
    end

    im1_interp_new = interp2(im1, xCoords, yCoords);
    It = im1_interp_new - im0_interp;

    uv = inv(M) * -[sum(sum(Ix_interp.*It));sum(sum(Iy_interp.*It))];
    u = uv(1);
    v = uv(2);
    
    xCoords = xCoords + u;
    yCoords = yCoords + v;
    
    newVal = sum(sum((im1_interp - im1_interp_new).^2));
    stopVal = abs(oldVal - newVal);
    oldVal = newVal;

    newX = newX + u;
    newY = newY + v;
end

if abs(newX) < wsize && abs(newY) < wsize
    newX = startX + newX;
    newY = startY + newY;
else
    newX = startX;
    newY = startY;
end