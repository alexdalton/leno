load sentence1.mat

[yEncoded, delta, error] = encodeLDM(y, .9, 2);

x_hat = decodeLDM(yEncoded, delta, .9);

figure;
subplot(2, 1, 1);
plot(y);
subplot(2, 1, 2);
plot(x_hat);