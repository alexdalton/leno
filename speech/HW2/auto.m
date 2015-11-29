
% This function calculates the autocorrelation function for the 
% data set "origdata" for a lag timescale of 0 to "endlag" and outputs 
% the autocorrelation function in to "a".
%function a = auto( origdata, endlag);

function a = auto(data, endlag);

N=length(data);

%now solve for autocorrelation for time lags from zero to endlag
for lag=0:endlag
  data1=data(1:N-lag);
   data1=data1-mean(data1);
  data2=data(1+lag:N);
   data2=data2-mean(data2);
  a(lag+1) = sum(data1.*data2)/sqrt(sum(data1.^2).*sum(data2.^2));
  clear data1
  clear data2
end