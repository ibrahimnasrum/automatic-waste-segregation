#include <EEPROM.h>
#include <Servo.h>
#include <LiquidCrystal_I2C.h>

Servo myServo; // FirstServo(in machine)
Servo mySecondServo;  // Second servo(door)
// Defines pins numbers for X-axis
const int stepX = 2; // Step pin for X-axis
const int dirX = 5;  // Direction pin for X-axis

// Defines pins numbers for Y-axis
const int stepY = 3; // Step pin for Y-axis
const int dirY = 6;  // Direction pin for Y-axis

// Defines pins numbers for Z-axis (third motor)
const int stepZ = 4; // Step pin for Z-axis
const int dirZ = 7;  // Direction pin for Z-axis

const int enPin = 8; // Enable pin for motor driver (shared for all motors)
const int servoPin = 36; // Pin where the servo is connected
const int secondServoPin = 24; // Pin where the second servo is connected

// Steps for positions
const int stepsToB = 5000;     // Number of steps from A to B
const int stepsToD = 5000;
const int maxSpeedDelay = 500; // Delay in microseconds for max speed

// Initialize the LCD (use correct I2C address, commonly 0x27 or 0x3F)
LiquidCrystal_I2C lcd(0x27, 16, 2);



/*
  command :
    a = move to A
    b = move to B
    c = move to C
    d = move to D
    s = startup signal
    i = the movement finished signal
    LOW DEKATI, HIGH JAUHI
*/

void setup() {
  // Sets the pins as outputs for X, Y, and Z axes
  pinMode(stepX, OUTPUT);
  pinMode(dirX, OUTPUT);
  pinMode(stepY, OUTPUT);
  pinMode(dirY, OUTPUT);
  pinMode(stepZ, OUTPUT);
  pinMode(dirZ, OUTPUT);
  pinMode(enPin, OUTPUT);

  // Enable motor driver
  digitalWrite(enPin, LOW); // Enable motors (LOW typically enables most drivers)

  myServo.attach(servoPin); // Attach the servo to the pin
  myServo.write(90);        // Set initial position to 90 degrees

  mySecondServo.attach(secondServoPin); // Attach the second servo
  mySecondServo.write(90); // Set initial position of the second servo to 90 degrees

  // Initialize the LCD
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("System Ready");
  delay(2000);
  lcd.clear();

  // Initialize serial communication
  Serial.begin(9600);
  // Instructions for serial commands
  Serial.println("Commands: 'a' - move to A, 'b' - move to B, etc.");
}

void moveToD() {
  // Display initial message
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Paper");

  // Set direction to move to B 
  digitalWrite(dirX, LOW); // Direction for X-axis
  digitalWrite(dirY, LOW); // Direction for Y-axis
  digitalWrite(dirZ, HIGH); // Direction for Y-axis

  for (int x = 0; x < stepsToD; x++) {
    digitalWrite(stepX, HIGH);
    digitalWrite(stepY, HIGH); // Simultaneous step for Y-axis
    digitalWrite(stepZ, HIGH);
    delayMicroseconds(maxSpeedDelay);
    digitalWrite(stepX, LOW);
    digitalWrite(stepY, LOW); // Simultaneous step for Y-axis
    digitalWrite(stepZ, LOW);
    delayMicroseconds(maxSpeedDelay);
  }

  ServoActiveLHS();
  delay(2000);

  // Set direcction to move to A back
  digitalWrite(dirX, HIGH); // Direction for X-axis
  digitalWrite(dirY, HIGH); // Direction for Y-axis
  digitalWrite(dirZ, LOW); // Direction for Z-axis

  for (int x = 0; x < stepsToD; x++) {
    digitalWrite(stepX, HIGH);
    digitalWrite(stepY, HIGH); // Simultaneous step for Y-axis
    digitalWrite(stepZ, HIGH);
    delayMicroseconds(maxSpeedDelay);
    digitalWrite(stepX, LOW);
    digitalWrite(stepY, LOW); // Simultaneous step for Y-axis
    digitalWrite(stepZ, LOW);
    delayMicroseconds(maxSpeedDelay);
  }

  CommunicationSignal();
  lcd.clear();
}

void moveToC(){
  // Display initial message
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Plastic");

  // Set direction to Move C
  digitalWrite(dirZ, HIGH); // Direction for Z motor

  for (int x = 0; x < stepsToB; x++) {
    digitalWrite(stepZ, HIGH);
    delayMicroseconds(maxSpeedDelay);
    digitalWrite(stepZ, LOW);
    delayMicroseconds(maxSpeedDelay);
  }

  ServoActiveLHS();
  delay(2000);

  //Set direction to move back to A back
  digitalWrite(dirZ, LOW); // Direction for Z motor

  for (int x = 0; x < stepsToB; x++) {
    digitalWrite(stepZ, HIGH);
    delayMicroseconds(maxSpeedDelay);
    digitalWrite(stepZ, LOW);
    delayMicroseconds(maxSpeedDelay);
  }

  CommunicationSignal();
  lcd.clear();
}

void moveToB() {
  // Display initial message
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Metal");

  // Set direction to move to B
  digitalWrite(dirX, LOW); // Direction for X-axis
  digitalWrite(dirY, LOW); // Direction for Y-axis

  for (int x = 0; x < stepsToB; x++) {
    digitalWrite(stepX, HIGH);
    digitalWrite(stepY, HIGH); // Simultaneous step for Y-axis
    delayMicroseconds(maxSpeedDelay);
    digitalWrite(stepX, LOW);
    digitalWrite(stepY, LOW); // Simultaneous step for Y-axis
    delayMicroseconds(maxSpeedDelay);
  }

  ServoActiveRHS();
  delay(2000);

  // Set direcction to move to A back
  digitalWrite(dirX, HIGH); // Direction for X-axis
  digitalWrite(dirY, HIGH); // Direction for Y-axis

  for (int x = 0; x < stepsToB; x++) {
    digitalWrite(stepX, HIGH);
    digitalWrite(stepY, HIGH); // Simultaneous step for Y-axis
    delayMicroseconds(maxSpeedDelay);
    digitalWrite(stepX, LOW);
    digitalWrite(stepY, LOW); // Simultaneous step for Y-axis
    delayMicroseconds(maxSpeedDelay);
  }

  CommunicationSignal();
  lcd.clear();
}

void moveToA() {
  // Display initial message
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Glass");

  // Set direction to move to A
  ServoActiveRHS();
  CommunicationSignal();
  lcd.clear();
}

void ServoActiveLHS() { // If the position at the RIGHT so the lid will open to the LEFT
  // Code for servo motor open close lid
  // Let it blank
  myServo.write(0);    // Move to 0 degrees
  Serial.println("Moved to 0 degrees.");
  delay(2000);
  myServo.write(90);    // Move to 0 degrees
  Serial.println("Moved to 90 degrees.");  
}

void ServoActiveRHS() { // If the position at the LEFT so the lid will open to the RIGHT
  // Code for servo motor open close lid
  // Let it blank
  myServo.write(180);  // Move to 180 degrees
  Serial.println("Moved to 180 degrees.");
  delay(2000);
  myServo.write(90);    // Move to 0 degrees
  Serial.println("Moved to 90 degrees.");      

}

void DoorOpen(){
  mySecondServo.write(90);   // Move second servo to 0 degrees
  Serial.println("Door Opened");
}

void DoorClose(){
  mySecondServo.write(0);   // Move second servo to 0 degrees
  Serial.println("Door Closed");
}

void CommunicationSignal() {
  // Send a signal to the computer/raspberry/python
  Serial.println("i");
}


void loop() {
  // Continuously send the startup signal until 'r' is received

  // Check if data is available on the Serial Monitor
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the input character

    if (command == 'b') {
      DoorClose();
      Serial.println("Moving motors to B...");
      moveToB();
      Serial.println("Reached point B.");
      DoorOpen();

    } else if (command == 'a') {
      DoorClose();
      Serial.println("Moving motors to A...");
      moveToA();
      Serial.println("Reached point A.");
      DoorOpen();

    } else if (command == 'c') {
      DoorClose();
      Serial.println("Moving motors to C...");
      moveToC();
      Serial.println("Reached point C.");
      DoorOpen();
    } else if (command == 'd') {
      DoorClose();
      Serial.println("Moving motors to D...");
      moveToD();
      Serial.println("Reached point D.");
      DoorOpen();
    }  else if (command == 'e') {
      DoorClose();
      delay(3000);
      DoorOpen();
    }
  }
}
