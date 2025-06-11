#include <Stepper.h>

// Motor
const int stepsPerRevolution = 2048;
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

// Botones
const int btnForward = 6;
const int btnBackward = 7;
bool lastBtnFwd = HIGH;
bool lastBtnBwd = HIGH;

// Sensor TCRT5000
const int sensorA0 = A0;
const int ledPin = 5;
const int umbralCercania = 500;

// Beam sensor y LED indicador
const int beamPin = 4;
const int ledBeam = 3;

void setup() {
  // Motor
  myStepper.setSpeed(10);

  // Botones
  pinMode(btnForward, INPUT_PULLUP);
  pinMode(btnBackward, INPUT_PULLUP);

  // Sensor TCRT5000
  pinMode(ledPin, OUTPUT);

  // Beam sensor y LED externo
  pinMode(beamPin, INPUT);        // Si no funciona prueba INPUT_PULLUP
  pinMode(ledBeam, OUTPUT);

  // Serial
  Serial.begin(9600);
  Serial.println("Sistema combinado listo.");
}

void loop() {
  // --- SENSOR TCRT5000 ---
  int lectura = analogRead(sensorA0);
  Serial.print("Sensor A0: ");
  Serial.print(lectura);

  if (lectura > umbralCercania) {
    Serial.print(" --> 🟢 LIBRE   ");
    digitalWrite(ledPin, LOW);
  } else {
    Serial.print(" --> 🔴 CERCA   ");
    digitalWrite(ledPin, HIGH);
  }

  // --- BEAM SENSOR ---
  int beamState = digitalRead(beamPin);
  if (beamState == LOW) {
    // Haz interrumpido: LED ON
    digitalWrite(ledBeam, HIGH);
    Serial.println("🌑 HAZ INTERRUMPIDO -> LED ENCENDIDO");
  } else {
    // Haz libre: LED OFF
    digitalWrite(ledBeam, LOW);
    Serial.println("☀️ HAZ LIBRE -> LED APAGADO");
  }

  // --- BOTONES CON FLANCO DESCENDENTE ---
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
