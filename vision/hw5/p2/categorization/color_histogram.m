function joint_hist = color_histogram(image, numBins)
    [height, width, ~] = size(image);
    red_vector = reshape(image(:,:,1), [height * width, 1]);
    blue_vector = reshape(image(:,:,2), [height * width, 1]);
    green_vector = reshape(image(:,:,3), [height * width, 1]);
    
    red_hist = hist(double(red_vector), numBins);
    blue_hist = hist(double(blue_vector), numBins);
    green_hist = hist(double(green_vector), numBins);
    
    joint_hist = zeros(numBins, numBins, numBins);
    for i = 1:numBins
        for j = 1:numBins
            for k = 1:numBins
                joint_hist(i, j, k) = red_hist(i) + blue_hist(j) + green_hist(k);
            end
        end
    end
    joint_hist = reshape(joint_hist, [numBins^3, 1]);
end
