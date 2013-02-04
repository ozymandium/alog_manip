function []=createAlog(inData, sensorString, filename)
%This version forked from Chris Rose's original
% Robert Cofield, 7/26/2012
% for MOOS *.alog file creation
% inData = [ struct, struct, ... ]
%         struct: Time = [double, double, ... ]
%                 Name = string
%                 Data = {string/double, string/double, ... }
% sensorString = [string, string ... ] same dimension as myData
% !!! Assume that no NaN's exist in the data !!!
myData = inData; % copy so we can delete it incrementally
[~,nvar] = size(myData); %get number of variables for asynch log
% cont_var = ones(1,nvar); % keep track of which var is finished

%open a file with filename for name
%open or create new file
%native bit ordering
%US ASCII encoding
fileID = fopen(filename, 'w', 'n', 'US-ASCII');


% get an arbitrary guess for min time - first in first
tmin = myData(1).Time(1);
whats_left = @(myData) [
while any(~isempty(myData(:).Time))
    % Publish any message from tmin
    for v=1:nvar
        for t=1:length(myData(v).Time)
            if myData(v).Time(t) == tmin
                time = myData(v).Time(t);
                new_time = [time(1:t-1), time(t+1:end)];
                sens = sensorString(v);
                name = myData(v).Name;
                A = struct(); % this will be used to redefine newData(v) without the one we're publishing
                if iscell(myData(v).Data)
                    value = myData(v).Data{t};
                    new_values = [[myData(v).Data{1:t-1}],[myData(v).Data{t+1:end}]];
                    fprintf(fileID,'%-10.3f    %s   \t%s  \t\t\t%s\n', time, name, sens, value);
                else % ASSUME vector of doubles
                    value = myData(v).Data(t);
                    new_values = [myData(v).Data(1:t-1), myData(v).Data(t+1:end)];
                    fprintf(fileID,'%-10.3f    %s   \t%s  \t\t\t%f\n', time, name, sens, value);
                end
                A.Time = [myData.Time(1:t-1), myData.Time(t+1:end)]; 
                myData(v) = A; % replace with just published data omitted
            end
        end
    end
    tmin = find_tmin(myData); % has changed now that we popped
end


% count = zeros(1,dim2); %count for keeping track of location in each variable
% count = count + 1;%matlab index start at 1
% 
%open a file with filename for name
%open or create new file
%native bit ordering
%US ASCII encoding
% fileID = fopen(filename, 'w', 'n', 'US-ASCII');
% newData = [];
% while(cont)%keep going till all time done
%     %get time data and put in A
%     for i = 1:dim2 %i specifies which variable we are talking about
%         if(isnan(count(i)) ~= 1) ||%says that sensor has no more data
%             A = myData(i);
%             %get next data in variable and save in matrix
%             newData(i) = A.Time(count(i));        
%         else
%             newData(i) = NaN;%min ignores NaN
%             
%             %check to see if all counts are NaN (we're done)
%             flag = 0;
%             for i = 1:dim2
%                 if(isnan(count(i)) == 1)
%                     flag = flag + 1;
%                 end    
%             end
%             
%             if(flag == dim2)
%                 cont = 0; %done
%             end 
%         end    
%     end
%     
%     if(cont) %dont' process if done (stupid)
%         %find minimum time
%         [~,index] = min(newData);
%         
%         %get timeseries
%         A = myData(index);
%         time = A.Time(count(index));%time
%         varName = A.Name;%variable name
%         
%         %get sensor name
%         sensorName = sensorString(index);
%         
%         %get data
%         if ischar(A.Data(count(index)))
%             var = A.Data(count(index));
%             fprintf(fileID,'%-6.3f    %s   \t%s  \t\t\t%s\n',time,char(varName),char(sensorName),var);
%         else
%             var = A.Data{count(index)};
%             fprintf(fileID,'%-6.3f    %s   \t%s  \t\t\t%12.5f\n',time,char(varName),char(sensorName),var);
%         end
%         
%         %increment count
%         count(index) = count(index) + 1;        
%     end
%     
%     %check for sensors being done
%     for i = 1:dim2
%         A = myData(i);
%         if(count(i) == length(A.Time))
%              count(i) = NaN;
%         end
%     end    
% end
% 
% status = fclose(fileID);
% 
% if(status == -1)
%     fclose('all')
%     
% end

