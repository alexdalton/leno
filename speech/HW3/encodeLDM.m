function [c, delta, error] = encodeLDM(x, alpha, F0)

N = length(x);
delta = sqrt(mean(diff(x).^2)) * log(2 * F0);
c = zeros(size(x));
d = zeros(size(x));
d_hat = zeros(size(x));
x_hat = zeros(size(x));
x_til = zeros(size(x));
error = zeros(size(x));

for n = 1:N
    d(n) = x(n) - x_til(n);
    if d(n) >= 0
        c(n) = 0;
        d_hat(n) = delta;
    else
        c(n) = 1;
        d_hat(n) = -delta;
    end
    
    if n > 1
        x_hat(n) = d_hat(n) + x_til(n - 1);
        x_til(n) = alpha * x_hat(n - 1);
    else
        x_hat(n) = d_hat(n);
        x_til(n) = 0;
    end
    
    error(n) = x_hat(n) - x(n);
end

end