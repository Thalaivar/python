#pragma once

#include "mbed.h"
#include "MPU9250.h"

#define ESC_MOTOR3 PA_11
#define ESC_MOTOR1 PC_5
#define ESC_MOTOR2 PC_4
#define ESC_MOTOR4 PB_9
#define PPM_PIN PA_8
#define TX_PIN PB_6
#define RX_PIN PA_10

Serial pc(TX_PIN, RX_PIN);
//Serial pc(USBTX, USBRX);
Timer t, t1, t3;
MPU9250 imu;
InterruptIn ppmPin(PPM_PIN);
PwmOut esc1(ESC_MOTOR1);
PwmOut esc2(ESC_MOTOR2);
PwmOut esc3(ESC_MOTOR3);
PwmOut esc4(ESC_MOTOR4);
DigitalOut myled(LED1);


