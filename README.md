# 👁️ VISION-ALS: Low-Cost Eye-Gaze Control Interface

## 📘 Overview

**VISION-ALS** is a hardware-independent, computer-vision-based eye-gaze control system designed for hands-free interaction with graphical user interfaces. Built for accessibility and ease-of-use, it enables users to control the mouse pointer and interface elements using just their eye movements.

---

## 🚀 Key Features

- 👁️ Eye-gaze tracking using **MediaPipe Face Mesh**
- 🎯 9-point **calibration** interface with **PyQt5**
- 🖱️ **Dwell-time-based auto-clicking** (2-second focus triggers mouse click)
- 🧭 **Real-time cursor control** with **OpenCV + PyAutoGUI**
- ⚙️ **Smooth movement algorithm** for jitter-free tracking
- 🧩 Modular design with accessibility-first screens for:
  - Food
  - Water
  - Emergency requests

---

## 🧰 Technologies Used

- Python  
- MediaPipe (Face Mesh)  
- OpenCV  
- PyAutoGUI  
- PyQt5

---

## 📂 Project Structure
├── screens/ # Accessibility screens (Food, Water, Emergency)
├── calibration_data/ # Saved data for 9-point calibration
├── calibration_ui/ # PyQt5-based calibration interface
├── evaluation_summary/ # Results from system usability testing
├── gaze_tracker/ # Gaze detection logic and smoothing algorithm
├── main_interface/ # Main navigation and interaction screen
├── requirements.txt # Python dependencies
├── README.md # Project documentation

---

🖥️ How to Run & Download
1. Download the Project
You can clone this repository directly from GitHub:

Bash

git clone [https://github.com/Piyushsaxena123/ALSVISION-ALS-Low-Cost-Eye-Graze-Interface.git](https://github.com/Piyushsaxena123/ALSVISION-ALS-Low-Cost-Eye-Graze-Interface.git)
cd ALSVISION-ALS-Low-Cost-Eye-Graze-Interface
2. Install dependencies
Bash

pip install -r requirements.txt
3. Run Calibration (First Time Only)
To teach the system your eye range, run the calibration tool and follow the red dot:

Bash

python calibration_ui.py
4. Start the Interface
Launch the main application:

Bash

python main_interface.py
<div align="center"> <p>Made with ❤️ by <a href="https://www.google.com/search?q=https://github.com/Piyushsaxena123">Piyush Saxena</a></p> </div>