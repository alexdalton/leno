function p = Webster(A, deltaX, P_zero, P_min1, k_delta_w)
C = 35000;

p = zeros(size(k_delta_w));

pressureWaves = zeros(length(k_delta_w), length(A));
zeroIndices = [];

for k = 1:size(k_delta_w, 2)
    omega = k_delta_w(k);
    P_curr = P_zero;
    P_prev = P_min1;
    m = 1 - ((omega * deltaX / C) ^ 2);
    pressures = zeros(size(A));
    pressures(1) = P_zero;
    for i = 2:length(A)
        areaRatio = A(i - 1) / A(i);
        p(k) = (m + areaRatio) * P_curr - areaRatio * P_prev;
        P_prev = P_curr;
        P_curr = p(k);
        pressures(i) = p(k);
    end
    if abs(p(k)) < .2
        zeroIndices = horzcat(zeroIndices, k);
    end
    pressureWaves(k, :) = pressures;
end

figure;
for i = 1:size(zeroIndices, 2)
    subplot(1, size(zeroIndices, 2), i);
    hold on;
    title(sprintf('P(x) for constant area function, f = %0.1f Hz', k_delta_w(zeroIndices(i)) / (2 * pi)));
    xlabel('x distance');
    ylabel('Pressure');
    plot(0:deltaX:17, pressureWaves(zeroIndices(i), :));
    plot(0:deltaX:17, zeros(1, 1701), 'color', 'r');
    hold off;
end

end
% for i = 1:size(resonances, 1)
%     plot(resonances(i, :));
% end