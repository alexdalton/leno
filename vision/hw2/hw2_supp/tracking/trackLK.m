function [Xpts, Ypts] = trackLK(PTHD, numframes)

for i=1:numframes
    file = sprintf('%s\\hotel.seq%d.png',PTHD,i-1);
    imgArr{i} = imread(file);
end

numPoints = 94;


wsize = 7;  

[Xpts, Ypts] = getKeypoints(im2double(imread('images\hotel.seq0.png')), .0000015);
Xpts = Xpts.';
Ypts = Ypts.';


for i=1:numframes-1 %number of images to go through
    img1 = double(imgArr{i});    
    img2 = double(imgArr{i+1});
    [dx, dy] = gradient(img1);
    for j=1:numPoints       %number of points to consider
        %find window around feature point
        x_center = Xpts(j,i);
        y_center = Ypts(j,i);
        xr = x_center-wsize:x_center+wsize;
        yr = y_center-wsize:y_center+wsize;

        [xrange, yrange] = meshgrid(xr,yr);
        %interpolate images
        W1 = interp2(img1, xrange, yrange);
        W2 = interp2(img2, xrange, yrange);
        %Construct Matrix to find u,v
        dx1 = interp2(dx,xrange,yrange);
        dy1 = interp2(dy,xrange,yrange);
        I1x = dx1.^2;
        I1y = dy1.^2;
        I1xy = dx1.*dy1;
        SigX1 = sum(sum(I1x));
        SigY1 = sum(sum(I1y));
        SigXY1 = sum(sum(I1xy));

        old_xrange = xrange;
        old_yrange = yrange;
        new_xrange = xrange;
        new_yrange = yrange;
        oldscore = sum(sum((W2-W1).^2));
        stopscore = 9999;
        count = 1;
        xtemp = 0;
        ytemp = 0;
        while stopscore > .1 && count < 40;  %iterate until convergence on a point
            %recompute window, matrix, u,v
            Wprime = interp2(img2, new_xrange, new_yrange);
            It = Wprime-W1;
            SigXIT = sum(sum(dx1.*It));
            SigYIT = sum(sum(dy1.*It));

            UVMat = inv(M)*-[SigXIT;SigYIT];
            u(j,i) = UVMat(1);
            v(j,i) = UVMat(2);
            
            new_xrange = old_xrange + u(j,i);
            new_yrange = old_yrange + v(j,i);
            newscore = sum(sum((W2-Wprime).^2));
            
            stopscore = abs(oldscore-newscore);
            oldscore = newscore;
            old_xrange = new_xrange;
            old_yrange = new_yrange;
            %keep track of path
            xtemp = xtemp + u(j,i);
            ytemp = ytemp + v(j,i);
            count = count+1;
        end

        if abs(xtemp)<wsize && abs(ytemp)<wsize
            Xpts(j,i+1) = Xpts(j,i) + xtemp;
            Ypts(j,i+1) = Ypts(j,i) + ytemp;
        else
            Xpts(j,i+1) = Xpts(j,i);
            Ypts(j,i+1) = Ypts(j,i);
        end

    end
end

imshow(imread('images\hotel.seq0.png')); hold on;
for i = 1:93
plot(Xpts(i,:), Ypts(i, :));
end
