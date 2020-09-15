#pragma once

#ifndef ARMING_H
#define ARMING_H

#include "PERIPHERALS.h"
#include "PPM.h"

void armQuad();             
void disarmCheck();                 //called every loop to check fo disarm
bool quadTestMode(bool enable);     //when testing in room, call this function to avoid uneccesary arming
void shutdown();      
bool armCheck;

void armQuad(){
        myled = 1;
        armCheck = false;
        t.start();
        pc.printf("Awaiting Arming\n");
        while(!armCheck){
                if(channelVal[1] < 1050 && channelVal[2] < 1050){
                        wait(2);
                        if(channelVal[1] < 1050 && channelVal[2] < 1050){
                                armCheck = true;
                                pc.printf("\n");
                                pc.printf("ARMED!\n");
                                esc1.pulsewidth_us(1000);
                                esc2.pulsewidth_us(1000);
                                esc3.pulsewidth_us(1000);
                                esc4.pulsewidth_us(1000);
                                myled=0;
                                wait(1);
                                myled = 1;
                                if(armCheck) pc.printf("QUAD IS ARMED!!!\n");
                                wait(10);
                                myled = 0;
                                break;
                            }
            }
    }
}


void disarmCheck(){
        if(channelVal[1] < 1050 && channelVal[2] < 1050){
            shutdown();
            armCheck = false;
        }
    }


bool quadTestMode(bool enable){
    armCheck = enable;
    esc1.pulsewidth_us(1000);
    esc2.pulsewidth_us(1000);
    esc3.pulsewidth_us(1000);
    esc4.pulsewidth_us(1000);
    return enable;

}

void shutdown() {
        esc1.pulsewidth_us(1000);
        esc2.pulsewidth_us(1000);
        esc3.pulsewidth_us(1000);
        esc4.pulsewidth_us(1000);
        pc.printf("I AM DEAD MAN!");
     }

#endif
