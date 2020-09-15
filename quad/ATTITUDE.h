#pragma once
#ifndef ATTITUDE_H
#define ATTITUDE_H

#include "PERIPHERALS.h"
#include "math.h"

void getAngles(float deltat);

void getAngles(float deltat) {
      
     imu.readAccelData(accelCount); 
     ax = (float)accelCount[0]*aRes - accelBias[0];  
     ay = (float)accelCount[1]*aRes - accelBias[1];   
     az = (float)accelCount[2]*aRes - accelBias[2];  
   
     imu.readGyroData(gyroCount);  
     gx = (float)gyroCount[0]*gRes - gyroBias[0];  
     gy = (float)gyroCount[1]*gRes - gyroBias[1];  
     gz = (float)gyroCount[2]*gRes - gyroBias[2];   
  
     imu.readMagData(magCount); 
     mx = (float)magCount[0]*mRes*magCalibration[0] - magbias[0];  
     my = (float)magCount[1]*mRes*magCalibration[1] - magbias[1];  
     mz = (float)magCount[2]*mRes*magCalibration[2] - magbias[2];
                            
     float G = sqrt(ax*ax + ay*ay + az*az);
     
     float pitchAcc = asin(-ax/G)*180.0f/PI;
     float rollAcc = asin(ay/(G*cos(pitch*PI/180.0f)))*180.0f/PI;
     float yawAcc = atan2(my, mx);
     yawAcc*=180.0f/PI;     
     
     pitch = ((gx*deltat)*180.0f/PI + pitch)*0.98 + pitchAcc*0.02;
     roll = ((gy*deltat)*180.0f/PI + roll)*0.98 + rollAcc*0.02;
     yaw = ((gz*deltat)*180.0f/PI + yaw)*0.98 + yawAcc*0.02;
     
}

    
#endif
