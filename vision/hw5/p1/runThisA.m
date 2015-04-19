%[im, person, number, subset] = readFaceImages('faces');

error = zeros(2, 5);
figure;
for d = 1:2
    for i = 1:5
        % call eigenfaces to recognize faces
        trainingImages = im(subset==1 );%| subset==5);
        evalImages = im(subset==i);
        trainingLabels = person(subset==1 );%| subset==5);
        evalLabels = person(subset==i);
        [weights, evalWeights, eigenVectors, labels, mean, error(d, i)] = eigenfaces(trainingImages,trainingLabels, 21 * d - 12, evalImages, evalLabels);
 
        subplot(2, 5, (d - 1) * 5 + i)
        x = reshape(mean, [2500, 1]);
        for k = 1:21 * d - 12
            x = x + evalWeights(k, 1) .* eigenVectors(:, k);
        end
        
        imagesc([evalImages{1}, reshape(x, [50, 50])])
        axis image;
        axis off;
        colormap gray;

    end
end

error
