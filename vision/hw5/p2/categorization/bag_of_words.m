% sift_desc = load('sift_desc.mat');
% gs = load('gs.mat');
% train_gs = gs.train_gs;
% test_gs = gs.test_gs;
% test_D = sift_desc.test_D;
% test_F = sift_desc.test_F;
% train_D = sift_desc.train_D;
% train_F = sift_desc.train_F;
% 
% numTraining = 1888;
% numTest = 800;
% 
% descriptors = [];
% descIndex = [];
% for i=1:numTraining
%    imageDesc = train_D{i};
%    [~, numDesc] = size(imageDesc);
%    randSet = randi([1, numDesc], 1, 8);
%    descriptors = [descriptors, imageDesc(:,randSet) ];
%    descIndex = [descIndex, randSet];
% end
% 
% [centroids, ~] = k_means(descriptors, 100);

% neighbors = [];
% for i = 1:numTraining
%     imageDesc = train_D{i};
%     meta = train_F{i};
%     neighbors(:, i) = spatial_pyramid_bag(imageDesc, 2, meta, centroids);
%     i
% end

numTest = 800;
labels = zeros(1, numTest);
confusionMatrix = zeros(8);
for i =1:numTest
    imageDesc = test_D{i};
    meta = test_F{i};
    pyramid = spatial_pyramid_bag(imageDesc, 2, meta, centroids);
    index = knnsearch(neighbors', pyramid');
    labels(i) = train_gs(index);
    confusionMatrix(labels(i), test_gs(i)) = confusionMatrix(labels(i), test_gs(i)) + 1;
    i
end

accuracy = sum(labels==test_gs) / numTest