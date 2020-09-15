#pragma once

#include<ARMING.h>
#include<PERIPHERALS.h>
#include<PID.h>
#include<ATTITUDE.h>
#include<INITIALISE.h>
#include<MPU9250.h>
#include<PPM.h>

#define CONNECT_TO_BOARD 0XDD
#define CONNECTION_OK 0X7C

void sendAngleData();
void sendPIDData(float PID_roll, float PID_pitch, float PID_yaw);
void sendThrustData(int thrust1, int thrust2, int thrust3, int thrust4);
void sendData(float PID_roll, float PID_pitch, float PID_yaw);
uint8_t option;
bool connectToGCS();
bool connect;

void sendAngleData(){
    char data[1];
    sprintf(data, "sa%fr%fp%fy\n", roll, pitch, yaw);
    pc.printf(data);
        }

void sendThrustData(int thrust1, int thrust2, int thrust3, int thrust4){
        char data[2];
        sprintf(data, "sf%db%dl%dr%de\n", thrust1, thrust2, thrust3, thrust4);
        pc.printf(data);
    }

void sendPIDData(float PID_roll, float PID_pitch, float PID_yaw){
        char data[1];
        sprintf(data, "so%fr%fp%fy\n", PID_roll, PID_pitch, PID_yaw);
        pc.printf(data);
    } 

void sendData(float PID_roll, float PID_pitch, float PID_yaw){
        char data[33];
        sprintf(data, "sf%fr%fp%fy%fq%fw%fe\n", PID_roll, PID_pitch, PID_yaw, roll, pitch, yaw);
        pc.printf(data);
    } 

bool connecToGCS(){
    bool connect;
    connect = false;
    char connectionReq[1];
    char recvdMsg[7];
    sprintf(connectionReq, "s%xe", CONNECT_TO_BOARD);
        while(!connect){
                myled = 1;
                pc.printf(connectionReq);
                myled = 0;
                myled = 1;
                wait(1);
                myled = 0;
                if(pc.readable()){
                    while(pc.readable()){
                        pc.gets(recvdMsg, 7);
                       // pc2.printf
                     }       
                 }
            }
    }
