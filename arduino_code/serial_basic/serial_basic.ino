int servos[2] = {0};
#include <Servo.h> 

Servo ser_out1;
Servo ser_out2;


void setup() {
  ser_out1.attach(9);
  ser_out2.attach(10);
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
       Serial.println(servos[0]);
       Serial.println(servos[1]);
       ser_out1.writeMicroseconds(servos[0] + 1000);
       ser_out2.writeMicroseconds(servos[1] + 1000);
    }
    
}

