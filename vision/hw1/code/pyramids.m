im =  im2double(rgb2gray(imread('tiger.jpg')));
filter = fspecial('gaussian', 7, 2);

figure(1);
subplot(2, 5, 1);
imagesc(im);
axis image;

figure(2);
subplot(2, 5, 1);
imagesc(log(abs(fftshift(fft2(im)))));
axis image;
colormap jet;

for n = 2:5
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
    
    subplot(2, 5, n + 4);
    imagesc(laplacian);
    colormap gray;
    axis image;
    
    figure(2);
    subplot(2, 5, n);
    imagesc(log(abs(fftshift(gauss_fft))));
    axis image;
    colormap jet;
    
    figure(2);
    subplot(2, 5, n + 4);
    imagesc(log(abs(fftshift(lap_fft))));
    axis image;
    colormap jet;

end