function [c, delta, error] = eightbitquant(y)

delta = max(abs(y)) / 256;
N = length(y);
c = zeros(size(y));
error = zeros(size(y));

for n = 1:N
    c(n) = floor(y(n) / delta) + 128;
    error(n) = ((c(n) - 128) * delta) - y(n);
end

end