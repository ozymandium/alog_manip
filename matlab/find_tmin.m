function tmin = find_tmin(myData)
% For use with createAlog.m
% Robert cofield, 7/31/2012

for v = 1:nvar
    if cont_var(v)
        for t=1:length(myData(v).Time)
            if (myData(v).Time(t) < tmin) && (~isnan(myData(v).Time(t)))
               tmin = myData(v).Time(t); 
            end
        end
    end
end

end