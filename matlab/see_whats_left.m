function tvec = see_whats_left(myData)
% slave to createAlog.m

tvec = [];
for v=1:length(myData)
    tvec(v,:) = myData(v).Time;
end