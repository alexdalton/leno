gs = load('gs.mat');

levels = 3;
bins = 16;

train_gs = gs.train_gs;
test_gs = gs.test_gs;

numTraining = 1888;
numTest = 800;

for i =1:numTraining
    imageName = sprintf('train\\%d.jpg', i);
    image = imread(imageName);
    neighbors{i} = spatial_pyramid(image, levels, bins);
end

labels = zeros(1, numTest);
for i =1:numTest
    imageName = sprintf('test\\%d.jpg', i);
    image = imread(imageName);
    pyramid = spatial_pyramid(image, levels, bins);
    index = nearest_neighbor(neighbors, pyramid);
    train_gs(index)
    labels(i) = train_gs(index);
end

accuracy = sum(labels==test_gs) / numTest