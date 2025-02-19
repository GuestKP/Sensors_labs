void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(A0, INPUT);
}

float cur = 0;
float k = 0.4;

void loop() {
  cur = (float)analogRead(A0) * k + (cur * (1. - k));
  Serial.println(cur);
  delay(10);
}
