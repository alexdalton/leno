function [c, delta] = eightbitquant(y)

delta = max(abs(y)) / 256;
N = length(y);
c = zeros(size(y));

for n = 1:N
    c(n) = floor(y(n) / delta) + 128;
end

end