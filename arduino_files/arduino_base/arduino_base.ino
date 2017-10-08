
int motor = 0;
int m1 = 6;
int m2 = 7;

void setup() {
  

  pinMode(m1, OUTPUT);
  digitalWrite(m1, LOW);
  pinMode(m2, OUTPUT);
  digitalWrite(m2, LOW);
  
  Serial.begin(9600);
 
}

void loop() {
  if(Serial.available()){
   motor = Serial.parseInt();
  }
  set_motor();
  //delay(5);
}

void set_motor(){
   analogWrite(m1, max(motor, 0));
   analogWrite(m2, abs(min(motor, 0)));
}

