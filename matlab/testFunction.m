function [cost,t,response] = testFunction(KP,KI,KD)
%TESTFUNCTION Summary of this function goes here
%   Detailed explanation goes here
assignin('base',"P",KP)
assignin('base',"I",KI)
assignin('base',"D",KD)

time_of_simulation=10; %[s]

out = sim("untitled1.slx");
response = out.yout;
t = response.time;

info = stepinfo(response.signals.values);

Overshoot = info.Overshoot; %OS

regulation_time=info.SettlingTime; %t

if regulation_time>=time_of_simulation
    r_time=response.time;
    last_index_=length(r_time);
    regultion_time=time_of_simulation;
else
    r_time=response.time;                    %choosing only regulation time
    index=find(regulation_time<r_time);
    last_index_=index(length(index));
end

signals_=response.signals.values(1:last_index_);
time_=response.time(1:last_index_);
end_value=signals_(last_index_);

ex=abs(signals_-end_value); %e(x)
ex2=ex.^2;                  %e(x)^2
tex=time_.*ex;              %t*e(x)
tex2=time_.*ex2;            %t*e(x)^2

f_ex=0;
f_ex2=0;
f_tex=0;
f_tex2=0;

for i=1:length(ex)-1
    t1=time_(i);
    t2=time_(i+1);
    a1=ex(i);
    a2=ex(i+1);
    b1=ex2(i);
    b2=ex2(i+1);
    c1=tex(i);
    c2=tex(i+1);
    d1=tex2(i);
    d2=tex2(i+1);
    f_ex=f_ex+(0.5*(t2-t1)*(a1+a2));
    f_ex2=f_ex2+(0.5*(t2-t1)*(b1+b2));
    f_tex=f_tex+(0.5*(t2-t1)*(c1+c2));
    f_tex2=f_tex2+(0.5*(t2-t1)*(d1+d2));
end

cost=f_ex2+Overshoot+regulation_time;
