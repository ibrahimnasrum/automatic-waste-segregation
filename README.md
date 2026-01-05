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

## Repository Contents (Recommended Structure)
You can structure the repo like this (clean & professional):

