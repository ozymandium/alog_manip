clear all
close all
clc

load gSeptentrio_PVT.mat
load gSeptentrio_ATT.mat

zNED_Att = gSeptentrio_ATT.zATT_NED;

roll = zNED_Att(1,:);
pitch = zNED_Att(2,:);
yaw = zNED_Att(3,:);


%u1.
% figure
% plot(roll);
% 
% figure
% plot(pitch);
% 
%  figure
%  plot(yaw*180/pi);

zNED_Pos = gSeptentrio_PVT.zNED_Pos;

N = zNED_Pos(1,:);
E = zNED_Pos(2,:);
D = zNED_Pos(3,:);

n = length(N);

%%

%simulate Penn State data
%data is mainly longitudinal data
%worse case - scenario situation
error =  .6 + .01*randn(1,n);

for i = 1:n
   
    %get current point
    N1 = N(i);
    E1 = E(i);
    D1 = D(i);
    
    %get next point
%     N2 = N(i+1);
%     E2 = E(i+1);
%     D2 = D(i+1);
    
    if(yaw(i) < -pi/2)
        
    Nx(i) = N1 + error(i)*sin(yaw(i) + pi/2);
    Ex(i) = E1 + error(i)*cos(yaw(i) - pi/2);
    else
    if(yaw(i) > pi/2)
    Nx(i) = N1 + error(i)*sin(yaw(i) + pi/2);
    Ex(i) = E1 + error(i)*cos(yaw(i) - pi/2);
    
    else
    
    if(yaw(i) >= -pi/2 && yaw(i) < 0)
        Nx(i) = N1 + error(i)*cos(yaw(i));
        Ex(i) = E1 - error(i)*sin(yaw(i));
    else

    if(yaw(i) <= pi/2 && yaw(i) >= 0)
        Nx(i) = N1 + error(i)*cos(yaw(i));
        Ex(i) = E1 + error(i)*sin(yaw(i));
    
    end
    
    end
    end
    end
    
    
end

figure
hold on;
plot(Ex,Nx,'b*');
plot(E,N,'r*');
title('Comparison')

%%
%%yaw data



%%
%simulate kapsch data

%kapsch data is ranges

%assume first gps point is location of radio (can change later)

rN = N(1);
rE = E(1);
rD = D(1);

%get distance from gps position to radio
%D is too noisy - don't use (meter level error)

 for i = 1:n
   
    d(i) = sqrt((rN - N(i))^2 + (rE - E(i))^2);
    
end

figure
plot(d)

% add error to distance

range = d + .01*randn(1,n);


%%
%simulate Sarnoff data
%Sarnoff data is a drifting ECEF solution (when no gps is available)

noise = .01;
dt = 1; 
tau = .1;

Ns = N;
Es = E;
Ds = D;

for i = 1:n-12
    
%         Ns(i+1) = N(i)+1*randn(1,1);
%         Es(i+1) = E(i) + randn(1,1);



    Ns(i+1) = N(i) - (i*i)/(n-1);%+ 1*randn(1,1);
    Es(i+1) = E(i) - (i*i)/(n-1);% + 1*randn(1,1);
    
end

figure
hold on;
plot(Es,Ns,'*');
plot(E,N,'r*');

% figure
% hold on;
% %plot(N)
% plot(Ns,'r')
% 
% figure
% plot(N-Ns);
% 
% figure
% plot(E-Es);

%    Ns(i+1) = exp((1/-tau)*dt)*Ns(i) + 1*randn(1,1);
%    Es(i+1) = exp((1/-tau)*dt)*Es(i) + noise; 
%    Ds(i+1) = exp((1/-tau)*dt)*Ds(i) + noise; 

%%
%save data and write to asych log

%Penn State: Ex,Nx
%SRI: Es,Ns
%Kapsch: range

%make fake time data
time = 2:(n+1);

%create time synch
ESRI = timeseries(Es,time,'Name','zE_SRI');
NSRI = timeseries(Ns,time,'Name','zN_SRI');

%tscSRI = tscollection({count1 count2},'name', 'count_coll')

gXbow440 = load('gXbow440.mat');
yawRate = gXbow440.gXbow440.zGyroX;
longAcc = gXbow440.gXbow440.zAccelX;
latAcc = gXbow440.gXbow440.zAccelY;
imuTime = gXbow440.gXbow440.time;

zGyroX = timeseries(yawRate,imuTime,'Name','zGyroX');
zAccelX = timeseries(longAcc,imuTime,'Name','zAccelX');
zAccelY = timeseries(latAcc,imuTime,'Name','zAccelY');


%make fake time data
time = 5:(n+4);

EPenn = timeseries(Ex,time,'Name','zE_Penn');
NPenn = timeseries(Nx,time,'Name','zN_Penn');

%make fake time data
time = 9:(n+8);

RKapsch = timeseries(range,time,'Name','zR_Kapsch');
  
GPSN = timeseries(N,time,'Name','zN_GPS');

GPSE = timeseries(E,time,'Name','zE_GPS');

GPSYaw = timeseries(yaw,time,'Name','zYaw_GPS');

%NKapsch = timeseries(Ns,time,'Name','KapschN');

%save timeseries in timeseries array
%s = [ESRI,NSRI,EPenn,NPenn,RKapsch,GPSN,GPSE,zGyroX,zAccelX,zAccelY];
s = [ESRI,NSRI,EPenn,NPenn,RKapsch,GPSN,GPSYaw,GPSE,zGyroX,zAccelX,zAccelY];

%save sensors that they correspond to
sensor = {'SRI', 'SRI', 'Penn', 'Penn', 'Kapsch','GPS','GPS','GPS','IMU','IMU','IMU'};
sensor(1)

createAlog(s,sensor,'EKFTesting.alog')