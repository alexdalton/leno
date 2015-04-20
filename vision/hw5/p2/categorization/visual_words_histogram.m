function hist = visual_words_histogram(ymin, ymax, xmin, xmax, descriptors, descX, descY, words)
descriptors = double(descriptors);
[~, numWords] = size(words);
hist = zeros(1, numWords);

region = descX >= xmin & descY >= ymin & descX <= xmax & descY <= ymax;
regionDesc = descriptors(:, region);

for i = 1:size(regionDesc, 2)
    distances = sum((repmat(regionDesc(:, i), 1, numWords) - words).^2);
    [~, index] = min(distances);
    hist(index) = hist(index) + 1;
end

%hist = hist/size(regionDesc,2);
end