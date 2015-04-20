function pyramid = spatial_pyramid(image, levels, numBins)
[height, width, ~] = size(image);

histSize = numBins^3;
numRegions = 0;
for i = 1:levels
    numRegions = numRegions + 4^(i - 1);
end
pyramid = zeros(numRegions * (histSize), 1);

i = 0;
for level = 1:levels
    numSteps = (2^(level-1));
    for y = 0:height/numSteps:height-1
        for x = 0:width/numSteps:width-1
            pyramid(i*histSize + 1:(i+1)*histSize) = color_histogram(image(y+1:y+height/numSteps,x+1:x+width/numSteps,:), numBins);
            i = i + 1;
        end
    end
end
end