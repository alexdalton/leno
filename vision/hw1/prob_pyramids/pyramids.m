im =  im2double(rgb2gray(imread('tiger.jpg')));
filter = fspecial('gaussian', 7, 2);

for n = 1:5
    g_smooth = imfilter(im, filter);
    downsample = g_smooth(1:2:end, 1:2:end);
    upsample = imresize(downsample, size(g_smooth));
    l_smooth = imfilter(upsample, filter);
    laplacian = im - l_smooth;
    im = downsample;
    
    gauss_fft = fft2(downsample);
    lap_fft = fft2(laplacian);
    
    figure(1);
    subplot(2, 5, n);
    imagesc(downsample);
    axis image;
    
    subplot(2, 5, n + 5);
    imagesc(laplacian);
    colormap gray;
    axis image;
    
    figure(2);
    subplot(2, 5, n);
    imagesc(log(abs(fftshift(gauss_fft))));
    axis image;
    colormap jet;
    
    figure(2);
    subplot(2, 5, n + 5);
    imagesc(log(abs(fftshift(lap_fft))));
    axis image;
    colormap jet;

end