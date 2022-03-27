function [cost] = testFunction(KP,KI,KD)
%TESTFUNCTION Summary of this function goes here
%   Detailed explanation goes here
assignin('base',"P",KP)
assignin('base',"I",KI)
assignin('base',"D",KD)


out = sim("untitled1.slx");
response = out.yout;
info = stepinfo(response);
cost = info.Overshoot;
if(cost ==0)
    cost = 99999999;
end

end

