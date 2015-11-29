function f0 = pitchDetection(x, fs)

Cl = .30 * max(x);
for i = 1:length(x)
    if x(i) >= Cl
        x(i) = x(i) - Cl;
    elseif abs(x(i)) < Cl
        x(i) = 0;
    elseif x(i) <= -Cl
        x(i) = x(i) + Cl;
    end
end

N = length(x);         % number of samples
stepSize = 5;          % step 5 samples each iteration
frameSize = .015 * fs; % 15 ms frames

figure;

w = hamming(frameSize);
s = zeros(floor((N - frameSize) / stepSize), 128);
f0 = zeros(floor((N - frameSize) / stepSize), 1);

for i = 1:stepSize:N - frameSize
   xFrame = x(i:i + frameSize - 1);
   wX = w .* xFrame;
   a = xcorr(wX, 160, 'coef');
   a = a(160 + 1: 320 + 1);
   for j = 1:length(a)
       if abs(a(j)) < .05
           a(j) = 0;
       end
   end
   [~, locs] = findpeaks(a);
   if i > 1
       f0_frame = f0(floor(i / 5));
   else
       f0_frame = 0;
   end
   if ~isempty(locs)
       f0_frame = fs / locs(1);
   end
   f0(floor(i / 5) + 1) = f0_frame; 
%    plot(a);
%    drawnow;
   FwX = fft(wX, 256);
   z = log(abs(FwX) .^ 2);
   s(floor(i / 5) + 1, :) = z(1:128);
end

% figure;
% hold on;
% imagesc(flipud(s));
% set(gca, 'YDir', 'normal');

end