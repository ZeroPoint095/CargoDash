#ifndef BLINKPATTERN_h
#define BLINKPATTERN_h

#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif


class BlinkPattern
{
  public:
    BlinkPattern() : nextPattern(-1), savePattern(-1), currPattern(-1), newPattern(false) {}
    
    void setPattern(int16_t pattern);
    boolean nextState();
    boolean patternStarted();
    
    static const int16_t ON= -1;
    static const int16_t OFF= 0;
    static const int16_t Flash1= 0xFFFD;
    static const int16_t Flash2= 0xFFF3;
    static const int16_t Flash4= 0xFF0F;
    static const int16_t Flash8= 0x80FF;
    static const int16_t Flash14= 0xBFFF;

    static const int16_t Blink1= 0x5555;
    static const int16_t Blink2= 0x3333;
    static const int16_t Blink4= 0x0F0F;
    static const int16_t Blink8= 0x00FF;
    static const int16_t Blink31= 0x7777;
    static const int16_t Blink62= 0x3F3F;
    static const int16_t Blink14= 0x3FFF;
    
  private:
    volatile int16_t nextPattern;
    int16_t savePattern;
    int16_t currPattern;
    volatile boolean newPattern;
    uint8_t c;
    boolean state;
};

#endif
