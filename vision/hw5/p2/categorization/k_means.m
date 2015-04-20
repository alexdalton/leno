function [centroids, labels] = k_means(descriptors, k)
[descSize, numDesc] = size(descriptors);
maxIterations = 25;
labels = zeros(1, numDesc);

% r = randi([1, numDesc], k, 1);
% centroids = descriptors(:, r);
descriptors = double(descriptors);
labels = randi([1, k], 1, numDesc);
for i =1:k
    centroids(:, i) = mean(descriptors(:, labels==i), 2);
end

labelsChanged = inf;
count = 0;
while (labelsChanged > 0)
    labelsChanged = 0;
    count = count + 1;
    for i=1:numDesc
        distances = sum((repmat(descriptors(:, i), 1, k) - centroids).^2);
        prevLabel = labels(i);
        [~, labels(i)] = min(distances);
        if labels(i) ~= prevLabel
            labelsChanged = labelsChanged + 1;
        end
    end
    labelsChanged
    for i =1:k
        centroids(:, i) = mean(descriptors(:, labels==i), 2);
    end
    if count > maxIterations
        break;
    end
end
end