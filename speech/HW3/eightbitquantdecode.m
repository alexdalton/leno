function y_hat = eightbitquantdecode(c, delta)
    y_hat = zeros(size(c));
    N = length(c);
    
    for n = 1:N
        y_hat(n) = (c(n) - 128) * delta;
    end
end