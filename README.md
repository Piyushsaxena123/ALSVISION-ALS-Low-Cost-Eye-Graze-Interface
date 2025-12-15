````markdown
<div align="center">

  <h1>👁️ VISION-ALS</h1>
  <h3>Low-Cost Eye-Gaze Control Interface</h3>

  <p>
    <b>Empowering hands-free communication through computer vision.</b><br>
    Hardware-independent. Open Source. Accessible.
  </p>

  <p>
    <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status" />
    <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python" />
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
    <img src="https://img.shields.io/badge/Made%20with-MediaPipe-orange?style=for-the-badge" alt="MediaPipe" />
  </p>

  <br />

  <img src="https://via.placeholder.com/800x400?text=Insert+Demo+GIF+or+Screenshot+Here" alt="Project Demo" width="800">

</div>

<br />

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [How to Use](#-how-to-use)
- [Troubleshooting](#-troubleshooting)

---

## 📘 Overview
**VISION-ALS** is an affordable, AI-powered eye-tracking system designed to assist individuals with ALS (Amyotrophic Lateral Sclerosis) and motor impairments. By using a standard webcam, it translates eye movements into mouse cursor commands, allowing users to communicate via a specialized interface without any physical interaction.

---

## 🚀 Key Features

| Feature | Description |
| :--- | :--- |
| **👁️ AI Gaze Tracking** | Powered by **MediaPipe Face Mesh** for high-precision iris tracking without expensive sensors. |
| **🖱️ Smart Cursor** | Optimized with a **0.15 smoothing factor** and **Side-Sitting Compensation** (X:1.4, Y:2.0) for natural control. |
| **⏱️ Dwell-Click** | "Look to Click" technology. Stare at any button for **3 seconds** to trigger an action. |
| **🎯 9-Point Calibration** | A guided calibration wizard adapts the system to the user's specific range of motion. |
| **🗣️ Communication UI** | Pre-built accessibility screens for **Food**, **Water**, **Medicine**, and **Emergency**. |

---

## 🛠 Tech Stack

This project is built using robust Python libraries for computer vision and GUI development.

* ![Python](https://img.shields.io/badge/Python-FFD43B?style=flat-square&logo=python&logoColor=blue) **Core Logic**
* ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white) **Image Processing**
* ![MediaPipe](https://img.shields.io/badge/MediaPipe-0099CC?style=flat-square&logo=google&logoColor=white) **Face & Iris Landmarks**
* ![PyQt5](https://img.shields.io/badge/PyQt5-41CD52?style=flat-square&logo=qt&logoColor=white) **Graphical User Interface**
* ![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-3776AB?style=flat-square&logo=python&logoColor=white) **Cursor Control**

---

## 📂 Project Structure

```plaintext
VISION-ALS/
├── calibration_ui.py           # 🔴 STEP 1: Run this to calibrate
├── main_interface.py           # 🟢 STEP 2: Run this to start the app
├── gaze_tracker.py             # 🧠 Logic: Eye tracking & smoothing math
├── calibration_data.json       # 💾 Data: Stores your calibration profile
├── requirements.txt            # 📦 Setup: Project dependencies
├── README.md                   # 📄 Documentation
└── screens/                    # 🎨 UI: Individual interface screens
    ├── main_menu.py
    ├── food_screen.py
    ├── water_screen.py
    ├── tablets_screen.py
    ├── washroom_screen.py
    └── final_message.py
````

-----

## ⚡ Getting Started

### 1\. Clone the Repository

```bash
git clone [https://github.com/Piyushsaxena123/ALSVISION-ALS-Low-Cost-Eye-Graze-Interface.git](https://github.com/Piyushsaxena123/ALSVISION-ALS-Low-Cost-Eye-Graze-Interface.git)
cd ALSVISION-ALS-Low-Cost-Eye-Graze-Interface
```

### 2\. Install Dependencies

Ensure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

-----

## 🎮 How to Use

### Step 1: Calibration (Crucial)

Before using the interface, the system must learn your eye movements.

```bash
python calibration_ui.py
```

  * **Instructions:** Follow the **Red Dot** moving across the screen.
  * **Action:** Press **`ENTER`** to capture each point.
  * **Finish:** Press **`q`** to save and exit.

### Step 2: Launch Interface

Start the main communication board.

```bash
python main_interface.py
```

  * **Action:** Look at a button (e.g., "Water").
  * **Trigger:** Hold your gaze for **3 seconds**. The system will click automatically.

-----

## 🔧 Troubleshooting

  * **Cursor is shaky?**
      * Ensure good lighting on your face. Avoid strong backlighting.
  * **Can't reach the corners?**
      * The system includes **Side-Sitting Compensation**. Try recalibrating (`calibration_ui.py`) and ensure you look at the extreme edges of the screen during the process.
  * **Crash on startup?**
      * Make sure `calibration_data.json` exists. If not, run `calibration_ui.py` first.

-----

\<div align="center"\>
\<p\>Made with ❤️ by \<a href="https://www.google.com/search?q=https://github.com/Piyushsaxena123"\>Piyush Saxena\</a\>\</p\>
\</div\>

```