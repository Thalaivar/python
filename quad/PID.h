#pragma once

#ifndef PID_H
#define PID_H

#include "mbed.h"
#include "PPM.h" 
#include "PERIPHERALS.h"
#include "TELEMETRY.h"

#define setpointScaler       12.575
#define yawSetpointScaler    12.575
#define heightSetpointScaler 200
#define MAX_THRUST_VAL       2000
#define MIN_THRUST_VAL       1000

float roll_prev, roll_integ, roll_kp, roll_ki, roll_kd;
float pitch_prev, pitch_integ, pitch_kp, pitch_ki, pitch_kd;
float yaw_prev, yaw_integ, yaw_kp, yaw_ki, yaw_kd;

float*   controlQuad(uint8_t print, float roll_prev, float roll_integ, float pitch_prev, float pitch_integ, float yaw_prev, float yaw_integ, float deltat);       //set print to 1: thrust vals  2: PID vals 3: proportional errors 4: derivative errors 5: integral errors 0: no print
float  setpoints[6];
float  calculateErrInt(float err_int, float err, float errPrev, float deltat);
void   convertToSetpoints();

float* controlQuad(uint8_t print, float roll_prev, float roll_integ, float pitch_prev, float pitch_integ, float yaw_prev, float yaw_integ, float detat){
        //calculate errors
        //first proportional error
        
        convertToSetpoints();
        float rollErr   =   setpoints[0] - roll;
        float pitchErr  =   setpoints[1] - pitch;
        float yawErr    =   setpoints[3] - gz*180.0f/PI;  
        
        float rollErrDot     =     -gx;
        float pitchErrDot    =     -gy;
        float yawErrDot      =     0;
        
        //calculate integral error
        roll_integ    = calculateErrInt(roll_integ, rollErr, roll_prev, deltat);
        pitch_integ   = calculateErrInt(pitch_integ, pitchErr, pitch_prev, deltat);
        yaw_integ     = calculateErrInt(yaw_integ, yawErr, yaw_prev, deltat);
        
        float PID_roll =  roll_kp*rollErr   +   roll_kd*rollErrDot       +    roll_ki*roll_integ;
        float PID_pitch = pitch_kp*pitchErr +   pitch_kd*pitchErrDot     +    pitch_ki*pitch_integ;
        float PID_yaw =   yaw_kp*yawErr     +   yaw_kd*yawErrDot         +    yaw_ki*yaw_integ;
        
        //convertToMicroseconds(); need to convert PID outputs to esc microseconds
        
        int thrust1 = channelVal[2] - PID_pitch - PID_roll + PID_yaw;
        int thrust2 = channelVal[2] + PID_pitch - PID_roll - PID_yaw;
        int thrust3 = channelVal[2] + PID_pitch + PID_roll + PID_yaw;
        int thrust4 = channelVal[2] - PID_pitch + PID_roll - PID_yaw;
        
        if(thrust1 < MIN_THRUST_VAL) thrust1 = MIN_THRUST_VAL;
        if(thrust1 > MAX_THRUST_VAL) thrust1 = MAX_THRUST_VAL;
        if(thrust2 < MIN_THRUST_VAL) thrust2 = MIN_THRUST_VAL;
        if(thrust2 > MAX_THRUST_VAL) thrust2 = MAX_THRUST_VAL;
        if(thrust3 < MIN_THRUST_VAL) thrust3 = MIN_THRUST_VAL;
        if(thrust3 > MAX_THRUST_VAL) thrust3 = MAX_THRUST_VAL;
        if(thrust4 < MIN_THRUST_VAL) thrust4 = MIN_THRUST_VAL;
        if(thrust4 > MAX_THRUST_VAL) thrust4 = MAX_THRUST_VAL;
         
        esc1.pulsewidth_us(thrust1);
        esc2.pulsewidth_us(thrust2);
        esc3.pulsewidth_us(thrust3);
        esc4.pulsewidth_us(thrust4);
        
        if(t3.read_ms() >= 35){
            if(print == 1)      sendThrustData(thrust1,thrust2,thrust3, thrust4);
            else if(print == 2)   sendPIDData(PID_roll, PID_pitch, PID_yaw);
            else if(print == 3)   sendAngleData();
            else if(print == 4)   sendData(PID_roll, PID_pitch, PID_yaw);
            t3.reset();
         }
                
        static float errorVals[6] = {rollErr, roll_integ, pitchErr, pitch_integ, yawErr, yaw_integ};
        float* pointerToVals;
        
        pointerToVals = errorVals;
        return pointerToVals;
    }

float calculateErrInt(float err_int, float err, float errPrev, float deltat){ //calculate integral of error for all three at omce else timer will fuck up
        
        //calculate addition to err_int
        float deltae = (deltat/2)*(errPrev + err);//reset t1
        
        //add to err_int
        return err_int + deltae;
    }

void convertToSetpoints(){
        for(int i = 0; i < 5; i++){
                if(i != 2 && i != 3){ //height setpoint will come from channel 3 and yaw setpoint to 40 dps
                    if(channelVal[i] >= 1497 && channelVal[i] <= 1503){
                         setpoints[i] = 0;
                    }
                    
                    else{
                        setpoints[i] = (channelVal[i] - 1495)/setpointScaler; //to get max setpoint of 20 degrees
                    }
                }
                
                else if(i == 2) setpoints[i] = (channelVal[i] - 1003)/heightSetpointScaler; //to get max height of 5 meters
                
                else if(i == 3) setpoints[i] = (channelVal[i] - 1495)/yawSetpointScaler; // to get max yaw rate setpoint of 40 dps   
        }
    }


//introduce dead band for yaw
#endif

//need to view data for yawErrDot and yaw_e.integ
