const int inputPinPIR = 2;
const int inputPinDist = 0; //Analog Pin 0 
int currPIR = LOW;
int currDist = 0;

void setup() {
  pinMode(inputPinPIR, INPUT);
  Serial.begin(9600);
}

void loop() {

  if (commandIssued()) {
    updateAndOutput();
  }
  
  delay(100);
  
}

boolean commandIssued() {
  if(Serial.available()) {
    if(commandValid()) {
      return true;
    }
  }
  return false;
}

boolean commandValid() {
  int cmdByte = Serial.read() - '0';
  return cmdByte == 3;
}

void updateAndOutput() {
  updateValues();
  outputValues();
}

void updateValues() {
  updatePIR();
  updateDist();
}

void updatePIR() {
  currPIR = digitalRead(inputPinPIR);
}

void updateDist() {
  currDist = analogRead(inputPinDist);
}

void outputValues() {
  outputPIR();
  outputDist();
}

void outputPIR() {
  Serial.println(currPIR);
}

void outputDist() {
  Serial.println(currDist);
}  

