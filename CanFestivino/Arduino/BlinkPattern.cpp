#include "BlinkPattern.h"

void BlinkPattern::setPattern(int16_t pattern) {
  nextPattern= pattern;
  newPattern= true;
}

boolean BlinkPattern::nextState() {
  
  if(((currPattern==-1) || (!state && (currPattern&1))) && newPattern) {
    newPattern= false;
    if(nextPattern==0) {
      currPattern= -1;
      state= false;
    } else {
      currPattern= nextPattern;
      savePattern= nextPattern;
      state= true;
      c= 0;
    }
  }
  if(currPattern==-1)
    return state;
  
  state= currPattern & 1;
  
  currPattern>>= 1;
  if(currPattern!=-1 && ++c==16) {
    currPattern= savePattern;
    c= 0;
  }
  return state;
}

boolean BlinkPattern::patternStarted() {
  return newPattern==false;
}