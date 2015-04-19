%[im, person, number, subset] = readFaceImages('faces');
% 
% evalSet = 5;
% 
% trainingImages = im(subset==1 );%| subset==5);
% evalImages = im(subset==evalSet);
% trainingLabels = person(subset==1 );%| subset==5);
% evalLabels = person(subset==evalSet);
% fisherfaces(trainingImages,trainingLabels, 10, evalImages, evalLabels);

error = zeros(2, 5);
k = 1;
for c = 10:21:31
    for i = 1:5
        % call fisherfaces to recognize faces
        trainingImages = im(subset==1 );%| subset==5);
        evalImages = im(subset==i);
        trainingLabels = person(subset==1 );%| subset==5);
        evalLabels = person(subset==i);
        error(k, i) = fisherfaces(trainingImages,trainingLabels, c, evalImages, evalLabels);
    end;
    k = k + 1;
end

error