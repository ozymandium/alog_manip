function [] = createAlog(myData,sensorString,filename)
%data is row of timeseries data
%get number of variables for asynch log
[dim1,dim2] = size(myData);

cont = 1;

count = zeros(1,dim2)%count for keeping track of location in each variable

count = count + 1;%matlab index start at 1

%open a file with filename for name
%open or create new file
%native bit ordering
%US ASCII encoding
fileID = fopen(filename, 'w', 'n', 'US-ASCII')

while(cont)%keep going till all time done
    %get time data and put in A
    for i = 1:dim2%i specifies which variable we are talking about
        if(isnan(count(i)) ~= 1)%says that sensor has no more data
            A = myData(i);
            %get next data in variable and save in matrix
            newData(i) = A.Time(count(i));        
        else
            newData(i) = NaN;%min ignores NaN
            
            %check to see if all counts are NaN (we're done)
            flag = 0;
            for i = 1:dim2
                if(isnan(count(i)) == 1)
                    flag = flag + 1;
                end    
            end
            
            if(flag == dim2)
                cont = 0; %done
            end
            
        end
        
    end
    
    if(cont) %dont' process if done (stupid)
        %find minimum time
        
        [y index] = min(newData);
        
        %get timeseries
        A = myData(index);
        time = A.Time(count(index));%time
        varName = A.Name;%variable name
        
        %get sensor name
        sensorName = sensorString(index);
        
        %get data
        var = A.Data(count(index));%variable
        
        %write to file
        fprintf(fileID,'%-6.3f    %s     %s       %6.5f\n',time,char(varName),char(sensorName),var);

        %increment count
        count(index) = count(index) + 1;        
    end
    
    %check for sensors being done
    for i = 1:dim2
        A = myData(i);
        if(count(i) == length(A.Time))
             count(i) = NaN;
        end
    end    
end

status = fclose(fileID);

if(status == -1)
    fclose('all')
    
end

