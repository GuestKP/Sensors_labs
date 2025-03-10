
#define SUM_NUM 10

typedef struct _color {
  int r;
  int g;
  int b;
} color;

color readColor() {
  color c = {0, 0, 0};

  digitalWrite(2, 1);
  digitalWrite(3, 0);
  digitalWrite(4, 0);
  delay(10);
  for(int i=0; i<SUM_NUM; i++) {
    c.r += analogRead(A0);
    delay(10);
  }

  digitalWrite(2, 0);
  digitalWrite(3, 1);
  digitalWrite(4, 0);
  delay(10);
  for(int i=0; i<SUM_NUM; i++) {
    c.g += analogRead(A0);
    delay(10);
  }

  digitalWrite(2, 0);
  digitalWrite(3, 0);
  digitalWrite(4, 1);
  delay(10);
  for(int i=0; i<SUM_NUM; i++) {
    c.b += analogRead(A0);
    delay(10);
  }

  c.r = 1024 - c.r / SUM_NUM;
  c.g = 1024 - c.g / SUM_NUM;
  c.b = 1024 - c.b / SUM_NUM;

  int c_min = ((c.r < c.g) && (c.r < c.b)) ? c.r :
              ((c.g < c.r) && (c.g < c.b)) ? c.g : c.b;

  c.b = (float)c.b * 1.27;

  /*c.r -= c_min;
  c.g -= c_min;
  c.b -= c_min;*/

  /*c.r = (float)c.r * 0.85;
  c.b = (float)c.b * 1.75;*/

  /*c.r = (float)c.r * 0.7;
  c.b = (float)c.b * 2;*/

  return c;
}

void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(A0, INPUT);
  Serial.begin(9600);
}

void loop() {
  color res = readColor();
  Serial.print(res.r);
  Serial.print('\t');
  Serial.print(res.g);
  Serial.print('\t');
  Serial.print(res.b);
  Serial.print('\t');
  Serial.print(res.b);
  Serial.print('\t');
  if(max(max(res.r, res.g), res.b) > 80) {
    if((res.r > res.g) && (res.r > res.b)) Serial.print("R\n");
    else if((res.g > res.r) && (res.g > res.b)) Serial.print("G\n");
    else Serial.print("B\n");
  } else {
    Serial.print("-\n");
  }
}
