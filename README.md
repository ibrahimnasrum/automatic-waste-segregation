# Automatic Waste Segregation System (AWS) — AI Vision + Arduino Actuation + Google Sheets Logging
**Roboflow Computer Vision • Python GUI (Tkinter) • Arduino Motion Control • LCD Status • Serial Communication • IoT Logging**

This project is an **automatic waste segregation prototype** that classifies waste into **glass / metal / plastic / paper** using a computer vision model (Roboflow), then sends a command to an Arduino-based mechanism to physically move and sort the item into the correct bin.  
Every classification is also logged to **Google Sheets** with a timestamp (and confidence when available).

---

## What This System Does
### ✅ Two modes
### 1) Manual Mode
- User clicks a category button in the GUI (**Glass / Metal / Plastic / Paper**)
- Python sends a serial command to Arduino (`a/b/c/d`)
- Arduino moves sorting mechanism + updates LCD
- Python logs the material + timestamp to Google Sheets

### 2) Automatic Mode (Camera + AI)
- Webcam captures a frame
- Image is sent to **Roboflow model** for classification
- Top predicted class is mapped to a serial command (`a/b/c/d`)
- Arduino moves sorting mechanism based on that class
- Python logs **material + timestamp + confidence** to Google Sheets

---

## System Architecture
**Python (PC/Laptop)**
- Tkinter GUI
- Webcam capture (OpenCV)
- Roboflow inference API
- Google Sheets logging (gspread)
- Serial communication (pyserial)

⬇ sends command (`a/b/c/d`) over Serial

**Arduino (Hardware)**
- Stepper motor movement (X/Y/Z axis)
- Servo (lid mechanism)
- Servo (door mechanism)
- LCD display shows detected category
- Sends completion signal back to Python (`i`) to re-enable GUI buttons safely

---

## Serial Command Mapping (Python → Arduino)
| Waste Type | Command | Arduino Action |
|----------:|:-------:|----------------|
| Glass     | `a`     | LCD shows **Glass**, servo action, completion signal |
| Metal     | `b`     | Move X+Y stepper path, LCD shows **Metal**, completion signal |
| Plastic   | `c`     | Move Z stepper path, LCD shows **Plastic**, completion signal |
| Paper     | `d`     | Move X+Y stepper path (different direction), LCD shows **Paper**, completion signal |

**Arduino → Python response**
- `i` = movement finished (Python uses this to re-enable buttons)

---


---

## Hardware Required
- Arduino (your code uses high pin numbers, so **Arduino Mega recommended**)
- 3× Stepper motors (X, Y, Z axis) + step/dir drivers
- 2× Servos (lid + door)
- I2C LCD (your Arduino code uses **16x2**, address `0x27`)
- Webcam (PC/Laptop camera or USB webcam)
- Power supply for motors/servos (do not power servos/motors from Arduino 5V directly)

---

## Arduino Pin Mapping (From `main_arduino_lcd.ino`)
### Stepper Motors (Step/Dir)
- X axis: `stepX = 2`, `dirX = 5`
- Y axis: `stepY = 3`, `dirY = 6`
- Z axis: `stepZ = 4`, `dirZ = 7`
- Enable pin: `enPin = 8` *(LOW = enable, typical drivers)*

### Servos
- Main servo (lid): `servoPin = 36`
- Second servo (door): `secondServoPin = 24`

### LCD
- `LiquidCrystal_I2C lcd(0x27, 16, 2);`

> If your LCD address is different (e.g. `0x3F`), change it in the Arduino code.

---

## Software Requirements
### Python Dependencies (from your `main_AWS.py`)
- `pyserial`
- `opencv-python`
- `numpy`
- `Pillow`
- `roboflow`
- `gspread`
- `google-auth`

**Install (recommended):**
```bash
# Create venv (Windows)
python -m venv venv
venv\Scripts\activate

# Install deps
pip install pyserial opencv-python numpy pillow roboflow gspread google-auth


