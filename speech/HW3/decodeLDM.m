function x_hat_prime = decodeLDM(c, delta, alpha)

x_hat_prime = zeros(size(c));
N = length(c);

for n = 1:N
    if c(n) == 0
        d_hat_prime = delta;
    else
        d_hat_prime = -delta;
    end
    
    if n > 1
        x_hat_prime(n) = d_hat_prime + alpha * x_hat_prime(n - 1);
    else
        x_hat_prime(n) = d_hat_prime;
    end

end

end