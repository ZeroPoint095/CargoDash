/*
Example of a slave node using the CanOpen library based on Canfestivino
Attach a potentiometer to A0
Attach a Servo to pin 9
Attach a MCP-2515 board using pin 10 as CS (you can change this in CO_can_Arduino.cpp if you need to)
Upload sketch and open Serial Monitor (made sure baud is set to 115200
Run canopen_master_example.py on another system attached to canbus network
 */



#include "canfestival.h" //#TODO move canfesival/canfestivino to a subfolder or something
#include "slave_node_example.h" //generated using objdictedit.py
// These all need to be included because canfestival needs them <= according to original canfestivino
// commenting out does not result in compile errors, but may cause runtime errors
//#include <avr/io.h>
//#include <Arduino.h>
#include <SPI.h>
#include "mcp_can.h"
//#include "Timer.h"
//#include "digitalWriteFast.h"
//#include "BlinkPattern.h"
#include <Servo.h>

CO<3, 4> co;

// Setup the potentiometer to analog pin 0, servo to pin 9
#define POT_PIN A0
#define SERVO_PIN 9

UNS32 readSensorCallback(const subindex * OD_entry, UNS16 bIndex, UNS8 bSubindex, UNS8 writeAccess) {
  Serial.print("Reading sensor: ");
  Serial.println(analogRead(POT_PIN));

  if (!writeAccess)
    delay(10);
  Sensor = analogRead(POT_PIN);
  ObjDict_PDO_status[ObjDict_Data.currentPDO].event_trigger = 1;

  return 0;
}



Servo myservo; //initialise the actuator used in this example
int val;

UNS32 writeActuatorCallback(const subindex * OD_entry, UNS16 bIndex, UNS8 bSubindex, UNS8 writeAccess) {
  Serial.print("Writing actuator:");
  Serial.println(Actuator);
  val = map(Actuator, 0, 1023, 0, 254); //maps the value of the sensor (0-1023) to a relative value between 0-254
  myservo.write(val);
  delay(2);
  return 0;
}

void setup() {
  co.CO_Init(); //intialise canopen via canbus

  //analogReference(INTERNAL); //not sure what this is, was in original Canfestivino example .ino. It caused the analog read to go all funky though
  pinMode(POT_PIN, INPUT); //setup potmeter pin
  myservo.attach(SERVO_PIN); //attach datapin of servo

  Serial.begin(115200);

  Serial.println("\nIf the following numbers are not 0, check OD callbacks and/or OD file");
  Serial.println(RegisterSetODentryCallBack(0x2001, 0, writeActuatorCallback), HEX);
  Serial.println((RegisterSetODentryCallBack(0x2000, 0, readSensorCallback)), HEX);
  Serial.println("Setup Complete");
}

void loop() {
  co.CO_Cycle();
}
