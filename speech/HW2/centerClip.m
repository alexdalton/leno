function y = centerClip(x, c)

Cl = c * max(x);
y = zeros(size(x));

for i = 1:length(x)
    if x(i) >= Cl
        y(i) = x(i) - Cl;
    elseif abs(x(i)) < Cl
        y(i) = 0;
    elseif x(i) <= -Cl
        y(i) = x(i) + Cl;
    end
end

figure;
subplot(2, 1, 1);
hold on;
title('Original input signal');
xlabel('Time (s)');
ylabel('Amplitude');
plot((0:length(x) - 1) / 8000, x);
xlim([0, (length(x) - 1) / 8000]);
hold off;
subplot(2, 1, 2);
hold on;
title('Clipped input signal');
xlabel('Time (s)');
ylabel('Amplitude');
plot((0:length(y) - 1) / 8000, y);
xlim([0, (length(y) - 1) / 8000]);
hold off;

end