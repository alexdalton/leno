function y = A2(x)
    y = zeros(size(x));
    y(x <= 6) = (1 / 2) * x(x <= 6) + 4;
    y(x > 6 & x <= 16) = (-3 / 5) * x(x > 6 & x <= 16) + (53 / 5);
    y(x > 16) = 2 * x(x > 16) - 31;
end