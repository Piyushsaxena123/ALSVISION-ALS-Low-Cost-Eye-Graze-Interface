````markdown
# 👁️ VISION-ALS: Low-Cost Eye-Gaze Control Interface

**VISION-ALS** is an affordable, hardware-independent eye-gaze control system designed to help individuals with ALS (Amyotrophic Lateral Sclerosis) or motor impairments communicate hands-free. Using standard webcams and computer vision, it translates eye movements into mouse cursor commands.

![Project Banner](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Python-3.x-blue) ![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Key Features

* **👁️ Advanced Gaze Tracking:** Uses **MediaPipe Face Mesh** for real-time iris tracking without expensive infrared hardware.
* **🖱️ Smart Cursor Control:**
    * **"Normal" Computer Feel:** Optimized smoothing algorithm (factor 0.15) for responsive yet stable movement.
    * **Side-Sitting Compensation:** Specialized sensitivity tuning ensures users can reach screen corners even if sitting at an angle.
* **⏱️ Dwell-Click Technology:** Simply stare at a button for **3 seconds** to trigger a click (no blinking or hardware switch required).
* **🎯 9-Point Calibration:** A guided `calibration_ui.py` module adapts the system to the user's specific eye range.
* **🗣️ Communication Boards:** Pre-built PyQt5 screens for essential needs:
    * 💧 Water
    * 🍲 Food
    * 💊 Medicine
    * 🚑 Emergency / Washroom

---

## 📂 Project Structure

```plaintext
VISION-ALS/
├── calibration_data.json       # Stores user calibration results (Auto-generated)
├── calibration_ui.py           # Run this FIRST to calibrate your eyes
├── main_interface.py           # Run this SECOND to start the communication app
├── gaze_tracker.py             # Core logic for tracking eyes and smoothing data
├── requirements.txt            # List of required Python libraries
├── screens/                    # Folder containing UI screens
│   ├── main_menu.py
│   ├── food_screen.py
│   ├── water_screen.py
│   ├── tablets_screen.py
│   ├── washroom_screen.py
│   └── final_message.py
└── README.md                   # Documentation
````

-----

## ⚙️ How It Works

1.  **Face Detection:** The system detects the user's face and isolates the iris landmarks.
2.  **Calibration:** The user looks at 9 specific points on the screen. The system records the eye position for each point to understand the user's range of motion.
3.  **Mapping:** The code maps the relative eye movement to the screen coordinates.
      * *Correction:* It applies specific "Dampeners" (X=1.4, Y=2.0) to boost sensitivity for users who might be looking from an angle or have limited eye range.
4.  **Smoothing:** A math formula reduces camera jitter, making the mouse move fluidly rather than shaking.
5.  **Interaction:** When the cursor hovers over a button (e.g., "Water"), a timer starts. If the gaze remains for 3 seconds, the system triggers a "Click" event and announces the command.

-----

## 📥 How to Download & Run

### Method 1: Clone via Git (Recommended)

If you have Git installed, open your terminal or command prompt and run:

```bash
git clone [https://github.com/Piyushsaxena123/ALSVISION-ALS-Low-Cost-Eye-Graze-Interface.git](https://github.com/Piyushsaxena123/ALSVISION-ALS-Low-Cost-Eye-Graze-Interface.git)
cd ALSVISION-ALS-Low-Cost-Eye-Graze-Interface
```

### Method 2: Download ZIP

1.  Scroll to the top of this GitHub page.
2.  Click the green **\<\> Code** button.
3.  Select **Download ZIP**.
4.  Extract the ZIP folder to your Desktop.

-----

## 🛠️ Setup & Usage

**1. Install Dependencies**
Open your terminal inside the project folder and run:

```bash
pip install -r requirements.txt
```

**2. Calibrate (Crucial Step)**
Before using the interface, you must teach the system your eye range.

```bash
python calibration_ui.py
```

  * *Instructions:* Follow the red dot with your eyes. Press `Enter` to capture each point. Press `q` to save and quit when finished.

**3. Run the Interface**
Start the main communication board:

```bash
python main_interface.py
```

  * *Usage:* Look at the button you want to press. Hold your gaze for 3 seconds. The system will click and log the command (e.g., "COMMAND TRIGGERED: Water").

-----

## 🤝 Contributing

Contributions are welcome\! Please fork this repository and submit a pull request.

**Author:** [Piyush Saxena](https://www.google.com/search?q=https://github.com/Piyushsaxena123)

```
```