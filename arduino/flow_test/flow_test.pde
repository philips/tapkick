int flowPin = 5;
unsigned long duration;


static unsigned long totalFlow = 0;  // measures how many 1/6100th Litres of fluid have passed since sketch started
static unsigned long totalDur = 0;
void countFlow() 
{
  totalFlow++;
}

void setup()
{
  Serial.begin(9600);
  pinMode(flowPin, INPUT);
  //digitalWrite(flowPin, HIGH);
  //attachInterrupt(0, countFlow, RISING);
}

void loop()
{
  //totalFlow = 0;
  duration = pulseIn(flowPin, HIGH, 20000);
  if (duration > 0) {
    totalFlow++;
    totalDur += 1000000.0/duration;
    Serial.print(duration);
    Serial.print("\t");
    Serial.print(float(totalDur)/float(totalFlow));
    Serial.print("\t");
    Serial.println(float(totalFlow)/float(6100.0));
    Serial.println("");
  }

}
