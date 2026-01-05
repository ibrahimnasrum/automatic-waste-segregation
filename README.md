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
```
# Create venv (Windows)
python -m venv venv
venv\Scripts\activate

# Install deps
pip install pyserial opencv-python numpy pillow roboflow gspread google-auth

## How to Run (Step-by-step)

### Step 1 — Upload Arduino Code
1. Open `arduino/main_arduino_lcd.ino` in **Arduino IDE**
2. Select the correct **Board** and **Port**
3. Click **Upload**
4. (Optional) Open **Serial Monitor** at **9600 baud** for debugging

**Arduino expects serial commands:**
- `a` = Glass  
- `b` = Metal  
- `c` = Plastic  
- `d` = Paper  

---

### Step 2 — Run the Python GUI
1. Connect Arduino to your PC via **USB**
2. Run the GUI:

```bash
python python/main_AWS.py
```

### Step 2 - In the GUI:

1. Click Refresh Ports

2. Select the correct COM Port

3. Click Connect

 You should see a message like:
_Connected to COMx at 9600 baud._

### Using the GUI

**Manual Mode**

 1. Click Glass / Metal / Plastic / Paper

2. GUI sends the serial command to Arduino

3. Buttons are disabled until Arduino replies i (movement finished)

4. Google Sheet updates with material + timestamp

**Automatic Mode (Camera + AI)**

1. Click Capture and Classify

2. Webcam captures an image

3. Roboflow returns top_class + confidence

4. Python maps class → sends command (a/b/c/d) to Arduino

5. Google Sheet updates with material + confidence + timestamp


## Troubleshooting

### No COM port shows

1. Click Refresh Ports

2. Ensure Arduino USB driver is installed

3. Try a different USB cable/port

4. Confirm Arduino appears in Device Manager (Windows)

### LCD not showing

1. Check I2C address (0x27 vs 0x3F)

2. Check SDA/SCL wiring

3. Arduino Mega: SDA=20, SCL=21

### Roboflow classification fails

1. Check internet connection

2. Verify Roboflow API key is correct

3. Confirm the model project/version exists

### Google Sheet update fails

1. Share the Google Sheet with your service account email

2. Verify your credential_api.json file path is correct

3. Ensure Google Sheets API is enabled in Google Cloud

## Credits / Team

Integrated Design Project (IDP) — Automatic Waste Segregation

**Section: 1 Group 7:**

1) Ibrahim Bin Nasrum ( 2116467 )
2) Ahmad Zarady Bin Zulkefly (2111837 )
3) Abdallah Mahamat Abacar Maeyd (2117777)   
4) Almasri Suhail Jihad ( 2128771 )
