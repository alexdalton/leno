load sentence3.mat

[yEncoded, delta, error] = encodeLDM(y, .9, 2);

x_hat = decodeLDM(yEncoded, delta, .9);

figure;
subplot(3, 1, 1);
plot(y);
title('Original input signal');

subplot(3, 1, 2);
plot(error);
title('Error signal e(n)');

subplot(3, 1, 3);
plot(x_hat);
title('Decoded signal after LDM encoding');

10 * log10(sum(y.^2) / sum(error.^2))