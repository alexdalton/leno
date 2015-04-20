function pyramid = spatial_pyramid_bag(imageDesc, levels, meta, centroids)
height = 256;
width = 256;

histSize = size(centroids, 2);
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
            pyramid(i*histSize + 1:(i+1)*histSize) = visual_words_histogram(y+1,y+height/numSteps,x+1,x+width/numSteps, imageDesc, meta(1,:), meta(2,:), centroids);
            i = i + 1;
        end
    end
end
end