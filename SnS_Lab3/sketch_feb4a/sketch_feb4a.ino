float cur = 0;
float k = 1;

#define PERIOD (1000)

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(A0, INPUT);


  uint32_t last_time = micros();
  while(1) {
    if(micros() - last_time >= PERIOD) {
      cur = (float)analogRead(A0);// * k + (cur * (1. - k));
      Serial.println(cur);
      last_time += PERIOD;
    }
  }
}

void loop() {}
