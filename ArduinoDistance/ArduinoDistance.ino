#include <EVShield.h>
#include <EVs_EV3Ultrasonic.h>
#include <LiquidCrystal.h>
#include <Wire.h>

EVShield evshield(0x34, 0x36);
EVs_EV3Ultrasonic ultrasonicSensor;
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

void setup() {
  evshield.init(SH_HardwareI2C);
  ultrasonicSensor.init(&evshield, SH_BAS1);
  ultrasonicSensor.setMode(MODE_Sonar_CM);
  lcd.clear();
  Serial.begin(115200);
}

void loop() {
  double distance = ultrasonicSensor.getDist();
  lcd.clear();
  lcd.print("Distance:");
  lcd.print(distance);
  Serial.print("[Distance:");
  Serial.print(distance);
  Serial.println("]");
  delay(1000);
}
