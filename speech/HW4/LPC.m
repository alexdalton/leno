function [alpha, R, error] = LPC(S)
N = 300;
M = 100;
p = 10;
alpha = 0.95;
sLength = length(S);
numFrames = ceil(sLength / 100);

window = 0.54 - 0.46 * cos(2 * pi * (0:N - 1) / (N - 1));
window = window';

% preemphasis process
S_tilda = zeros(size(S));
S_tilda(1) = S(1);
for i = 2:sLength
    S_tilda(i) = S(i) - alpha * S(i - 1);
end

R = zeros(numFrames, p + 1);
alpha = zeros(numFrames, p + 1);
error = zeros(numFrames, N);
for i = 1:M:sLength
    frameNum = floor(i / M) + 1;
    if (i + N - 1) > sLength
        xFrame = [S_tilda(i:end); zeros(N - sLength + i - 1, 1)];
    else
        xFrame = S_tilda(i:i + N - 1);
    end
    
    xFrame_tilda = xFrame .* window;
    xFrame_corr = xcorr(xFrame_tilda, p);      % get autocorrelation
    R(frameNum, :) = xFrame_corr(p + 1:end);
    alpham = levinson(R(frameNum, :), 10);
    alpha(frameNum, :) = alpham; % durbin recursion
    
    alpham = alpham(2:end); % reverse for easy multiplication
    error(frameNum, 1) = xFrame(1);
    for j = 2:N
        if j > p
            error(frameNum, j) = xFrame(j) - sum(alpham' .* xFrame(j - p: j -1));
        else
            error(frameNum, j) = xFrame(j) - sum(alpham(1: j - 1)' .* xFrame(1: j - 1));
        end
    end
end

alpha = alpha(:, 2:end);
R = R(:, 2:end);

s_hat_frames = zeros(numFrames, N);
s_hat = zeros(size(S_tilda));
for frameNum = 1:numFrames
    alphak = alpha(frameNum, :);
    s_hat_frames(frameNum, 1) = error(frameNum, 1);
    for j = 2:N
        if j > p
            s_hat_frames(frameNum, j) = sum(alphak .* s_hat_frames(frameNum, j - p: j -1)) + error(frameNum, j);
        else
            s_hat_frames(frameNum, j) = sum(alphak(1: j - 1) .* s_hat_frames(frameNum, 1: j -1)) + error(frameNum, j);
        end
    end
    s_hat((frameNum - 1) * M + 1: (frameNum - 1) * M + 100) = s_hat_frames(frameNum, 1:100);
end

excitation = zeros(size(S));
for i = 1:sLength-100
    if mod(i - 1, 100) == 0
        excitation(i) = mean(S_tilda(i+1:i+100).^2);
    else
        excitation(i) = 0;
    end
end

s_hat_frames = zeros(numFrames, N);
s_hat = zeros(size(S_tilda));
for i = 1:M:sLength
    frameNum = floor(i / M) + 1;
    if (i + N - 1) > sLength
        error = [excitation(i:end); zeros(N - sLength + i - 1, 1)];
    else
        error = excitation(i:i + N - 1);
    end
    alphak = alpha(frameNum, :);
    s_hat_frames(frameNum, 1) = error(1);
    for j = 2:N
        if j > p
            s_hat_frames(frameNum, j) = sum(alphak .* s_hat_frames(frameNum, j - p: j -1)) + error(j);
        else
            s_hat_frames(frameNum, j) = sum(alphak(1: j - 1) .* s_hat_frames(frameNum, 1: j -1)) + error(j);
        end
    end
    s_hat((frameNum - 1) * M + 1: (frameNum - 1) * M + 100) = s_hat_frames(frameNum, 1:100);
end

end