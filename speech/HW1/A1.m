function y = A1(x)
    y = zeros(size(x));
    y(x <= 3) = x(x <= 3) + 1;
    y(x > 3 & x <= 6) = -x(x > 3 & x <= 6) + 7;
    y(x > 6) = (9 / 11) * x(x > 6) - (43 / 11);
end