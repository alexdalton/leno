function error = fisherfaces(trainingFaces, trainingLabels, c, evalFaces, evalLabels)

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

% get eigenvectors of covariance matrix
[U, lambda] = eig(A' * A);
V = A * U;

% normalize each V
for i=1:size(V, 2)
   V(:, i) = V(:, i) ./ sqrt(sum(V(:, i).^2));
end
 
% keep numTraining - c eigenvectors with largest eigenvalues
[~, largestIndices] = sort(diag(lambda), 'descend');
eigenvectors = V(:, largestIndices(1:numTraining - 10));


% compute weight coefficients
Wpca = eigenvectors' * A;

meanWpca = mean(Wpca, 2);
Sw = zeros(numTraining - 10, numTraining - 10);
Sb = zeros(numTraining - 10, numTraining - 10);
for i =1:10
    Xi = Wpca(:, (i - 1) * (numTraining / 10) + 1:i * (numTraining / 10));
    n = size(Xi, 2);
    mu_i = mean(Xi, 2);
    Xi = Xi - repmat(mu_i, 1, n);
    Sw = Sw + Xi * Xi';
    Sb = Sb + n * (mu_i - meanWpca) * (mu_i - meanWpca)';
end

[U, lambda] = eig(Sb, Sw);
[~, largestIndices] = sort(diag(lambda), 'descend');
fisher_eigenvectors = U(:, largestIndices(1:c-1));

weights = fisher_eigenvectors' * Wpca;

B = zeros(imHeight * imWidth, numEval);
for i=1:numEval
    x = evalFaces{i} - meanImg;
    B(:,i) = x(:);
end
evalWeights = fisher_eigenvectors' * (eigenvectors' * B);

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