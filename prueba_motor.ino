#include <Stepper.h>

// Motor paso a paso
const int stepsPerRevolution = 2048;
Stepper myStepper(stepsPerRevolution, 13, 11, 12, 10); // IN1-IN4 orden correcto

// Botones
const int btnForward = 2;
const int btnBackward = 3;
bool lastBtnFwd = HIGH;
bool lastBtnBwd = HIGH;

// Sensor TCRT5000
const int sensorA0 = A0;
const int ledIR = 5;
const int umbralCercania = 500;

// Beam sensor y LED indicador
const int beamPin = 4;
const int ledBeam = 6;

void setup() {
  // Motor
  myStepper.setSpeed(10);

  // Botones
  pinMode(btnForward, INPUT_PULLUP);
  pinMode(btnBackward, INPUT_PULLUP);

  // Sensor IR
  pinMode(ledIR, OUTPUT);

  // Beam sensor
  pinMode(beamPin, INPUT); // Prueba con INPUT_PULLUP si no detecta
  pinMode(ledBeam, OUTPUT);

  // Comunicación serial
  Serial.begin(9600);
  Serial.println("✅ Sistema listo con pines actualizados.");
}

void loop() {
  // --- SENSOR TCRT5000 ---
  int lectura = analogRead(sensorA0);
  Serial.print("Sensor A0: ");
  Serial.print(lectura);

  if (lectura > umbralCercania) {
    Serial.print(" --> 🟢 LIBRE   ");
    digitalWrite(ledIR, LOW);
  } else {
    Serial.print(" --> 🔴 CERCA   ");
    digitalWrite(ledIR, HIGH);
  }

  // --- BEAM SENSOR ---
  int beamState = digitalRead(beamPin);
  if (beamState == LOW) {
    digitalWrite(ledBeam, HIGH);
    Serial.println("🌑 HAZ INTERRUMPIDO -> LED ENCENDIDO");
  } else {
    digitalWrite(ledBeam, LOW);
    Serial.println("☀️ HAZ LIBRE -> LED APAGADO");
  }

  // --- BOTONES (Flanco descendente) ---
  bool currentBtnFwd = digitalRead(btnForward);
  bool currentBtnBwd = digitalRead(btnBackward);

  if (lastBtnFwd == HIGH && currentBtnFwd == LOW) {
    Serial.println("➡️ Avanzando 1/16 de vuelta");
    myStepper.step(stepsPerRevolution / 16);
  }

  if (lastBtnBwd == HIGH && currentBtnBwd == LOW) {
    Serial.println("⬅️ Retrocediendo 1/16 de vuelta");
    myStepper.step(-stepsPerRevolution / 16);
  }

  lastBtnFwd = currentBtnFwd;
  lastBtnBwd = currentBtnBwd;

  delay(500);
}
