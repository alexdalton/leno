% x is the input signal
% fs sampling frequency
% c percent to center clip te signal by
function f0 = pitchDetection(x, fs, c)

N = length(x);                    % number of samples
stepSize = 5;                     % step 5 samples each iteration
frameTimeLength = .015;           % set each frame to be 15 ms long
frameSize = frameTimeLength * fs; % 15 ms frames
totalFrames = floor((N - frameSize) / stepSize); % total number of frames that will be examined

x2 = centerClip(x, c);      % center clip signal by (c * 100)% max value

w = hamming(frameSize);      % create a hamming window of size equal to frameSize
s = zeros(totalFrames, 128); % holds values for the spectrogram
f0 = zeros(totalFrames, 1);  % holds values for f0
f1 = zeros(totalFrames, 1);  % holds values for f1
f2 = zeros(totalFrames, 1);  % holds values for f2
f3 = zeros(totalFrames, 1);  % holds values for f3

for i = 1:stepSize:N - frameSize
   a = xcorr(x2(i:i + frameSize - 1), 160, 'coef');   % autocorrelation of xFrame
   a = a(160 + 1: 320 + 1);          % symmetric at 160, so look at 161-321
   
   % some quick smoothing to remove false peaks
   for j = 1:length(a)
       if a(j) < .05
           a(j) = 0;
       end
   end
   
   [~, locs] = findpeaks(a);  % get peaks of autocorrelation
   
   if ~isempty(locs)
      possibleF0s = locs.^-1 * fs; % find all possible F0 values from all peaks
      [~, index] = min(abs(possibleF0s - 100)); % choose peak closest to 100 Hz (bit of a cheat)
      % if the F0 we find is more than 300Hz we know we found no good peaks
      if possibleF0s(index) > 300
        f0(floor(i / 5) + 1) = 0;
      else
        f0(floor(i / 5) + 1) = possibleF0s(index);
      end
   else
      f0(floor(i / 5) + 1) = 0;
   end

   % stuff to calculate the spectrogram
   wX = w .* x(i:i + frameSize - 1);                 
   FwX = fft(wX, 256);
   z = log(abs(FwX) .^ 2);
   z = z(1:128);
   s(floor(i / 5) + 1, :) = z;
   
   % smooth the spectrogram to make finding the max better
   avgFilter = ones(1, 5) / 5;
   zFiltered = filter(avgFilter, 1, z);
   
   % find max values for F1, F2, and F3
   [~, I1] = max(zFiltered(5:28));
   f1(floor(i / 5) + 1) = (I1 + 4) * fs / 256;
   [~, I2] = max(zFiltered(I1 + 20:I1 + 60));
   f2(floor(i / 5) + 1) = (I2 + I1 + 23) * fs / 256;
   [~, I3] = max(zFiltered(I2 + 20:128));
   f3(floor(i / 5) + 1) = (I3 + I2 + I1 + 42) * fs / 256;
   
end

figure;
subplot(5, 1, 1);
x = (0:length(f0)-1) * stepSize / fs;
imagesc(flipud(s'));
title('Spectrogram');
ylabel('Frequency (0 - 4000 Hz)');
xlabel('Time');
axis off;
xlim([0,length(f0)]);
ylim([0,128]);
subplot(5, 1, 2);
plot(x, f0);
title('F0');
ylabel('Frequency (Hz)');
xlabel('Time (s)');
xlim([0, (length(f0) - 1) * stepSize / fs]);
subplot(5, 1, 3);
plot(x, f1);
title('F1');
ylabel('Frequency (Hz)');
xlabel('Time (s)');
xlim([0, (length(f1) - 1) * stepSize / fs]);
subplot(5, 1, 4);
plot(x, f2);
title('F2');
ylabel('Frequency (Hz)');
xlabel('Time (s)');
xlim([0, (length(f2) - 1) * stepSize / fs]);
subplot(5, 1, 5);
plot(x, f3);
title('F3');
ylabel('Frequency (Hz)');
xlabel('Time (s)');
xlim([0, (length(f3) - 1) * stepSize / fs]);


end