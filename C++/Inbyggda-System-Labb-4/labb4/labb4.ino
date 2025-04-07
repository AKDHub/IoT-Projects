#include<Servo.h>
#include<EEPROM.h>
Servo myServo;


// Rename ports
#define GREEN_LED 12
#define RED_LED 11
#define YELLOW_LED 10

#define BTN_1 5
#define BTN_2 4
#define BTN_3 3
#define BTN_4 2

// Rename port to change passcode
#define BTN_PROGRAM 6

// Rename port to control servo
#define SERVO 9


// Original passcode
int passcode[] = {BTN_4, BTN_2, BTN_1, BTN_4};
const int passcodeLength = 4;

int input_passcode[4] = {0};
int currentIndex = 0;
bool passcodeEntered = false;

bool PASSWORD_CHANGE_MODE = false;

//Servo variable
int angle = 0;

void setup() {
  // LED
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);

  // Buttons
  pinMode(BTN_1, INPUT_PULLUP);
  pinMode(BTN_2, INPUT_PULLUP);
  pinMode(BTN_3, INPUT_PULLUP);
  pinMode(BTN_4, INPUT_PULLUP);
  pinMode(BTN_PROGRAM, INPUT_PULLUP);

  //Servo
  myServo.attach(SERVO);
  myServo.write(angle);
  Serial.begin(9600);  // Initialize serial communication for debugging

  Serial.print("PASSWORD CHANGE MODE: ");
  Serial.println(PASSWORD_CHANGE_MODE);
}

void loop() {
  // Turn on RED_LED and turn off GREEN_LED
  digitalWrite(RED_LED, HIGH);
  digitalWrite(GREEN_LED, LOW);

  // Read button presses
  if (digitalRead(BTN_1) == LOW) {
    storeButtonPress(BTN_1);
    delay(200);  // Add a small delay to debounce the button
  } 
  
  else if (digitalRead(BTN_2) == LOW) {
    storeButtonPress(BTN_2);
    delay(200);
  } 
  
  else if (digitalRead(BTN_3) == LOW) {
    storeButtonPress(BTN_3);
    delay(200);
  } 
  
  else if (digitalRead(BTN_4) == LOW) {
    storeButtonPress(BTN_4);
    delay(200);
  }

  // Button 5 to change the passcode
  else if (digitalRead(BTN_PROGRAM) == LOW) {
    digitalWrite(YELLOW_LED, HIGH);
    PASSWORD_CHANGE_MODE = !PASSWORD_CHANGE_MODE;
    Serial.print("PASSWORD CHANGE MODE: ");
    Serial.println(PASSWORD_CHANGE_MODE);

    Serial.print("EEPROM PASSWORD: ");
    Serial.println(EEPROM[0]);
    Serial.println(EEPROM[1]);
    Serial.println(EEPROM[2]);
    Serial.println(EEPROM[3]);
    Serial.println(EEPROM[4]);
    delay(200);
  }

  // Check for a passcode match if not in Passwor change mode
  if(!PASSWORD_CHANGE_MODE){
    digitalWrite(YELLOW_LED, LOW);
    if (!passcodeEntered) {
      if (checkPasscode()) {
        digitalWrite(GREEN_LED, HIGH); // Correct passcode entered, turn on GREEN_LED
        digitalWrite(RED_LED, LOW);
        passcodeEntered = true;
        unlockDoor(true);
        delay(5000);
        unlockDoor(false);
        resetPasscode();
      }
    }
  }
}

void storeButtonPress(int button) {
  // Shift existing inputs (FIFO)
  for (int i = 1; i < passcodeLength; i++) {
    if (PASSWORD_CHANGE_MODE){
      EEPROM[i-1] = EEPROM[i];
    } else {
      input_passcode[i - 1] = input_passcode[i];
    }
  }

  if (PASSWORD_CHANGE_MODE){
    EEPROM[passcodeLength -1] = button;
    EEPROM[passcodeLength] = 50;
  } else {
    input_passcode[passcodeLength - 1] = button; // Store the new input at the last index
  }
  Serial.print("Button pressed: ");
  Serial.println(button);
}

// Check the button input to see if it matches the saved passcode
bool checkPasscode() {
  for (int i = 0; i < passcodeLength; i++) {
    if (EEPROM[passcodeLength] == 50){
      if (input_passcode[i] != EEPROM[i]) {
        return false;
      }
    } else {
      if (input_passcode[i] != passcode[i]) {
        return false;
      }
    }
  }
  return true;
}

// Reset all saved variables after the password matches
void resetPasscode() {
  for (int i = 0; i < passcodeLength; i++) {
    input_passcode[i] = 0;
  }
  currentIndex = 0;
  passcodeEntered = false;
}

//Lock control
void unlockDoor(bool unlocked){
  if (!unlocked){
    angle = 0;
  }
  else if (unlocked) {
    angle = 90;
    }
  myServo.write(angle);
  delay(15);
}
