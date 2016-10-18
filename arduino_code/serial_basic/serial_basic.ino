#include <Servo.h> 
#include <Stepper.h>

int servos[2] = {0};

Servo ser_out1;
Stepper ser_out2(200, 3, 4, 5, 6);


void setup() {
  ser_out1.attach(9);
  Serial.begin(9600);
}

bool read_input() {
    if (Serial.available() >= 6) {
        String data = Serial.readStringUntil('!');

        for (int i = 0; i < 2; i++) {
            servos[i] = 0;

            for (int j = 0; j < 3; j++) {
                servos[i] *= 10;
                servos[i] += data[i * 3 + j] - '0';
            }

        }

        //Serial.println("received!");

        return 1;
    }
    else {
        return 0;
    }
}

void loop () {
  if (read_input()) {
       //Serial.println(servos[0]);
       //Serial.println(servos[1]);
       ser_out1.write(servos[0]);
       ser_out2.step(servos[1] - 10);
    }
    
}

