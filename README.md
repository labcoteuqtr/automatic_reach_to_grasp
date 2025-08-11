# automatic_reach_to_grasp

#Project design and implementation of a semi-automatic rotary dispensing system that allows for 
both manual and automatic control of the motor through sensors and buttons. The 
system will serve as a base for feeding rodents or for other controlled behavior 
experiments.
# Stepper Motor Automation – 28BYJ-48 + ULN2003 + Arduino

Control a **28BYJ-48** 5V stepper motor using an **Arduino** and two push buttons.  
Each button press moves the motor **one fifteenth of a full revolution** (1/15 turn).

---

##  Bill of Materials
- **Arduino** (Uno, Mega, Nano or compatible)
- **28BYJ-48** 5V, 4-phase stepper motor
- **ULN2003** driver board
- **2× Momentary push buttons**
- **Jumper wires** (male–female for Arduino ↔ ULN2003)
- *(Optional)* Breadboard
- *(Power)* Arduino 5V or regulated external 5V

---

##  Wiring

### Stepper Motor (ULN2003 ↔ Arduino)
| ULN2003 Pin | Arduino Pin |
|-------------|-------------|
| IN1         | D13         |
| IN2         | D11         |
| IN3         | D12         |
| IN4         | D10         |
| +5V         | 5V          |
| GND         | GND         |

> Motor plugs directly into the ULN2003 board via its white JST connector.  
> The IN1–IN4 order matches the code:  
> `Stepper(stepsPerRevolution, 13, 11, 12, 10)`

### Buttons (with internal pull-ups)
- **Forward Button**: one leg → D2, other leg → GND
- **Backward Button**: one leg → D3, other leg → GND

---

## ⚙️ How It Works
- `stepsPerRevolution = 2048` (typical for 28BYJ-48 with gearbox)
- Each press moves `2048 / 15 ≈ 136.5` steps → **24° per press**
- Uses `delay(100)` for simple debounce
- Forward and backward moves triggered on button press **(falling edge detection)**

---

##  Arduino Code

```cpp
#include <Stepper.h>

// --- GLOBAL CONFIG ---
const int stepsPerRevolution = 2048;
Stepper myStepper(stepsPerRevolution, 13, 11, 12, 10); // IN1..IN4

// Buttons
const int btnForward = 2;
const int btnBackward = 3;
bool lastBtnFwd = HIGH;
bool lastBtnBwd = HIGH;

void setup() {
  myStepper.setSpeed(10); // RPM

  pinMode(btnForward, INPUT_PULLUP);
  pinMode(btnBackward, INPUT_PULLUP);

  Serial.begin(9600);
  Serial.println("System ready. Use the buttons to rotate the motor.");
}

void loop() {
  bool currentBtnFwd = digitalRead(btnForward);
  bool currentBtnBwd = digitalRead(btnBackward);

  // Forward
  if (lastBtnFwd == HIGH && currentBtnFwd == LOW) {
    Serial.println("Forward: 1/15 turn");
    myStepper.step(stepsPerRevolution / 15);
  }

  // Backward
  if (lastBtnBwd == HIGH && currentBtnBwd == LOW) {
    Serial.println("Backward: 1/15 turn");
    myStepper.step(-stepsPerRevolution / 15);
  }

  lastBtnFwd = currentBtnFwd;
  lastBtnBwd = currentBtnBwd;

  delay(100); // Debounce
}
