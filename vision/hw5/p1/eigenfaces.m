function [weights, evalWeights, eigenvectors, labels, meanImg, error] = eigenfaces(trainingFaces, trainingLabels, d, evalFaces, evalLabels)

numTraining = size(trainingFaces, 2);
numEval = size(evalFaces, 2);

[imHeight, imWidth] = size(trainingFaces{1});

% compute mean image
meanImg = zeros(imHeight, imWidth);
for i=1:numTraining
    meanImg = meanImg + (1 / numTraining) * trainingFaces{i};
end

% remove mean image from each training image
% and create A where covariance matrix C = A' * A
A = zeros(imHeight * imWidth, numTraining);
for i=1:numTraining
    trainingFaces{i} = trainingFaces{i} - meanImg;
    A(:,i) = trainingFaces{i}(:);
end

% create covariance matrix C
C = A' * A;

% get eigenvectors of covariance matrix
[U, lambda] = eig(C);
V = A * U;

% normalize each V
for i=1:size(V, 2)
    V(:, i) = V(:, i) ./ sqrt(sum(V(:, i).^2));
end

% keep d eigenvectors with largest eigenvalues
[~, largestIndices] = sort(diag(lambda), 'descend');
eigenvectors = V(:, largestIndices(1:d));

% if d >= 9
%     figure;
%     for i=1:9
%         subplot(3, 3, i);
%         imagesc(reshape(eigenvectors(:, i), [50, 50]));
%         axis image;
%         axis off;
%         colormap gray;
%     end
%     print('eigenfaces', '-dpng');
% end

% compute weight coefficients
weights = eigenvectors' * A;

% compute weight coefficients for eval set
B = zeros(imHeight * imWidth, numEval);
for i=1:numEval
    x = evalFaces{i} - meanImg;
    B(:,i) = x(:);
end

evalWeights = eigenvectors' * B;

% calculate distance in d-space
distances = zeros(numTraining, numEval);
for i = 1:numEval
    for j = 1:numTraining
        distances(j, i) = sqrt(sum((evalWeights(:, i) - weights(:, j)).^2));
    end
end

labels = zeros(1, numEval);
for i=1:numEval
    [~, minI] = min(distances(:, i));
    labels(i) = trainingLabels(minI);
end

error = sum(labels ~= evalLabels) / numEval;




end