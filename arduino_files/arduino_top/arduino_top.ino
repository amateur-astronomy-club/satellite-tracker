
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
#include <Servo.h>

Servo servo; 

/* Assign a unique ID to this sensor at the same time */
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

int servo_microseconds = 1450;

void setup() {
  Serial.begin(9600);
  mag.begin();
  servo.attach(9);
}

void loop() {
  send_mag();
  set_servo();
  delay(50);
}

void set_servo()
{
  if(Serial.available()){
    servo_microseconds = parseInt(Serial.readStringUntil('!'));
    //Serial.println(servo_microseconds);
    Serial.flush();
  }
  servo.writeMicroseconds(servo_microseconds);  // range found to 550 to 2350
}

void send_mag(){
  sensors_event_t event; 
  mag.getEvent(&event);

  float heading = atan2(event.magnetic.z, event.magnetic.x); // Remeber to correct for magnetic declination
  
  // Correct for when signs are reversed.
  if(heading < 0)
    heading += 2*PI;
    
  // Check for wrap due to addition of declination.
  if(heading > 2*PI)
    heading -= 2*PI;
   
  // Convert radians to degrees for readability.
  float headingDegrees = heading * 180/M_PI; 
   
  Serial.println(headingDegrees);
  
}

int parseInt(String str) // I don't like the Arduino parseInt Function
{
    int res = 0; // Initialize result
  
    // Iterate through all characters of input string and
    // update result
    for (int i = 0; i < 4; ++i)
        res = res*10 + str[i] - '0';
  
    // return result.
    return res;
}
