
#include "ARMING.h"                                                             //Header for SafeGaurds
#include "ATTITUDE.h"                                                           //Header for Calculating Attitude             
#include "PID.h"                                                                //Headere for computing and implementing Corrections
#include "INITIALISE.h"                                                         //Definition for Gains and setup functions
#include "MPU9250.h"                                                            //IMU Header file
#include "PERIPHERALS.h"                                                        //Declaration for ESC output and Initialisation        
#include "PPM.h"                                                                //Radio Signal setup and reading 
#include "TELEMETRY.h"

int main(){
        initialisePeripherals();
        //pc.printf("HI I AM ALIVE!");
        //wait(3);
        initialiseIMU();
        initialiseErrInt(&roll_integ, &pitch_integ, &yaw_integ);
        initialiseGains(&roll_kp, &pitch_kp, &yaw_kp, &roll_kd, &pitch_kd, &yaw_kd, &roll_ki, &pitch_ki, &yaw_ki);
        initialiseMagBias();
        
        armCheck=false;                                                             
        if(!quadTestMode(false)) armQuad();                                                    //Set this true only when testing in room else arm Quad,pull down channel 2 and 3 for 2 seconds            
        
        //send = true;
        
        initialiseTimers();                                                     //setup for timer
        
        float *errorVals;
        float deltat;
        
        while(armCheck){
            
            deltat = t1.read_us()/1000000.0f;                                                //functional loop of quad when running
            
            if(imu.readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01) getAngles(deltat);  //Getting attitude Feedback  

            //Implementing control, input of function is serial monitor control               
            errorVals = controlQuad(2, roll_prev, roll_integ, pitch_prev, pitch_integ, yaw_prev, yaw_integ, deltat);
            
            //assign previous and integral values
            roll_prev = errorVals[0];
            roll_integ = errorVals[1];
            pitch_prev = errorVals[2];
            pitch_integ = errorVals[3];
            yaw_prev = errorVals[4];
            yaw_integ = errorVals[5];
            
            disarmCheck();                                                    //disarm guard to powerdown the aerial vehicle as precaution
            t1.reset();
        }
}

