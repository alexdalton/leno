deltaX = .01;
p_zero = 1.0;
p_minus_one = 0.5;
L = 17.0;

x = 0:deltaX:L;
ah_area_function = A1(x);
ee_area_function = A2(x);

startOmega = 2 * pi * 10; % 10 Hz
endOmega = 2 * pi * 4000; % 4 KHz
k_delta_w = startOmega:2*pi:endOmega;

% figure;
% subplot(2, 3, 1);
% hold on;
% title('/ah/ Area Function');
% xlabel('x distance (cm)');
% ylabel('cross sectional area (cm^2)');
% plot(x, ah_area_function);
% hold off;

% subplot(2, 3, 2);
% hold on;
% title('/ee/ Area Function');
% xlabel('x distance (cm)');
% ylabel('cross sectional area (cm^2)');
% plot(x, ee_area_function);
% hold off;

% subplot(2, 3, 3);
% hold on;
% title('Constant Area Function (dA/dx = 0)');
% xlabel('x distance (cm)');
% ylabel('cross sectional area (cm^2)');
% plot(x, ones(size(x)));
% hold off;

% subplot(2, 3, 4);
% hold on;
% title('P(L=17, w) for /ah/ Area Function');
% xlabel('Frequency (Hz)');
% ylabel('Pressure at L = 17');
%p = Webster(ah_area_function, deltaX, p_zero, p_minus_one, k_delta_w);
% plot(k_delta_w / (2*pi), p);
% plot(k_delta_w / (2*pi), zeros(size(k_delta_w)), 'color', 'r');
% hold off;

% subplot(2, 3, 5);
% hold on;
% title('P(L=17, w) for /ee/ Area Function');
% xlabel('Frequency (Hz)');
% ylabel('Pressure at L = 17');
%p = Webster(ee_area_function, deltaX, p_zero, p_minus_one, k_delta_w);
% plot(k_delta_w / (2*pi), p);
% plot(k_delta_w / (2*pi), zeros(size(k_delta_w)), 'color', 'r');
% hold off;

% subplot(2, 3, 6);
% hold on;
% title('P(L=17, w) for Constant Area Function');
% xlabel('Frequency (Hz)');
% ylabel('Pressure at L = 17');
p = Webster(ones(size(x)), deltaX, p_zero, p_minus_one, k_delta_w);
% plot(k_delta_w / (2*pi), zeros(size(k_delta_w)), 'color', 'r');
% plot(k_delta_w / (2*pi), p)
% hold off;
