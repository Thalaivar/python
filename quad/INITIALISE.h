#pragma once

#ifndef INITIALISE_H
#define INITIALISE_H

#include "PERIPHERALS.h"
#include "PPM.h"
#include "PID.h"


#define MAGBIAS_X 98.89
#define MAGBIAS_Y 181.041
#define MAGBIAS_Z -20.38

float KP_ROLL = 1.5;
float KP_PITCH = 1.4;
float KP_YAW = 0;
float KD_ROLL = 0.0775;
float KD_PITCH = 0.0755;
float KD_YAW = 0;
float KI_ROLL = 0.0;
float KI_PITCH = 0.0;
float KI_YAW = 0;
     
void initialiseIMU();
void initialisePeripherals(); //call first
void initialiseErrInt(float* roll_integ, float* pitch_integ, float* yaw_integ);
void initialiseTimers(); //call before main loop
void initialiseGains(float* roll_kp, float* pitch_kp, float* yaw_kp, float* roll_kd, float* pitch_kd, float* yaw_kd, float* roll_ki, float* pitch_ki, float* yaw_ki);
void initialiseMagBias();

void initialiseIMU(){
            
            uint8_t address = imu.readByte(MPU9250_ADDRESS, WHO_AM_I_MPU9250);
            pc.printf("%x\n",address);
            if(address == 0x73){
                pc.printf("Resetting IMU....");
                imu.resetMPU9250();
                myled=!myled;
                wait(1);
                myled=!myled;
                pc.printf("Calibrating IMU...");
                imu.calibrateMPU9250(gyroBias, accelBias);
                myled=!myled;
                wait(1);
                myled=!myled;
                imu.initMPU9250();
                pc.printf("IMU initialised!\n");
                myled=!myled;
                wait(2);
                myled=!myled;
                imu.initAK8963(magCalibration);
                myled=!myled;
                wait(1);
                myled=!myled;
                pc.printf("AK8963 initialized for active data mode....\n\r");
                imu.getAres();
                imu.getGres();
                imu.getMres();
            }
            
            else{
                while(1){
                    myled = !myled;
                    wait(0.5);
                   }
                }                            
    }

void initialisePeripherals() {
        pc.baud(57600);
        //pc2.baud(57600);
        myled=!myled;
        wait(1);
        myled=!myled;
        wait(1);
        myled=!myled;
        ppmPin.rise(&measureChannel);
    }

void initialiseErrInt(float* roll_integ, float* pitch_integ, float* yaw_integ){
        *roll_integ = 0;
        *pitch_integ = 0;
        *yaw_integ = 0;
        roll = 0;
        pitch = 0;
        yaw = 0;
    }

void initialiseGains(float* roll_kp, float* pitch_kp, float* yaw_kp, float* roll_kd, float* pitch_kd, float* yaw_kd, float* roll_ki, float* pitch_ki, float* yaw_ki){
        *roll_kp  = KP_ROLL;
        *pitch_kp = KP_PITCH;
        *yaw_kp   = KP_YAW;
        *roll_kd  = KD_ROLL;
        *pitch_kd = KD_PITCH;
        *yaw_kd   = KD_YAW;
        *roll_ki  = KI_ROLL;
        *pitch_ki = KI_PITCH;
        *yaw_ki   = KI_YAW;  
}

void initialiseTimers(){
        t.reset();
        //t1.stop();
        t.start();
        t1.start();
        t3.start();
    }

void initialiseMagBias(){
        magbias[0]  = MAGBIAS_X;
        magbias[1]  = MAGBIAS_Y;
        magbias[2]  = MAGBIAS_Z;
    }
//add optional magnetometer calibration func.
#endif
