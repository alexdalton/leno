load s1.mat;
load s2.mat;

[alpha1, R, error] = LPC(s1);
[alpha2, ~] = LPC(s2);

