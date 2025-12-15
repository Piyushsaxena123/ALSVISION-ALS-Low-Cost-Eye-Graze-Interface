import sys
import json
import math
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QTimer

# Import your tracker
from gaze_tracker import GazeTracker 

# Ensure plots don't try to open a GUI window (prevents freezing)
plt.switch_backend('Agg')

# --- CONFIGURATION: KEY MAPPINGS ---
# This dictionary controls which key corresponds to which screen location.
# Format: "Name": (X_Position_%, Y_Position_%, 'KEY_TO_PRESS')
positions = {
    "Top-Left":      (0.1, 0.1, 'q'),
    "Top":           (0.5, 0.1, 'w'),
    "Top-Right":     (0.9, 0.1, 'e'),
    "Left":          (0.1, 0.5, 'a'),
    "Center":        (0.5, 0.5, 'c'),
    "Right":         (0.9, 0.5, 'd'),
    "Bottom-Left":   (0.1, 0.85, 'z'),
    "Bottom":        (0.5, 0.85, 's'),
    "Bottom-Right":  (0.9, 0.85, 'x')
}

class CalibrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gaze Calibration Suite")
        self.setWindowState(Qt.WindowFullScreen) # Full screen
        self.setAutoFillBackground(True)

        # Set White Background
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)

        self.gaze_tracker = GazeTracker()
        self.current_step = 0
        self.keys_map = list(positions.items())
        self.is_processing = False 

        # --- UI ELEMENTS ---
        
        # 1. Red Target Dot (With Key Letter Inside)
        self.dot_label = QLabel(self)
        self.dot_label.setFixedSize(90, 90) # Slightly larger for visibility
        self.dot_label.setStyleSheet("""
            background-color: red; 
            border-radius: 45px; 
            border: 4px solid black;
            color: white;
            font-weight: bold;
            font-size: 40px;
        """)
        self.dot_label.setAlignment(Qt.AlignCenter)
        self.dot_label.setVisible(False)

        # 2. Blue Replay Dot (Cursor)
        self.cursor_label = QLabel(self)
        self.cursor_label.setFixedSize(30, 30)
        self.cursor_label.setStyleSheet("""
            background-color: blue; 
            border-radius: 15px; 
            border: 2px solid white;
        """)
        self.cursor_label.setVisible(False)

        # 3. Instruction Bar
        self.instruction_label = QLabel(self)
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.update_instruction_style("normal")

        self.init_ui()
        
        # Begin Sequence
        self.instruction_label.setText("Calibration Starting... Please wait.")
        QTimer.singleShot(1000, self.show_next_marker)

    def init_ui(self):
        screen_w = self.width()
        screen_h = self.height()
        # Place instruction at bottom initially
        self.instruction_label.setGeometry(0, screen_h - 100, screen_w, 100)

    def update_instruction_style(self, mode):
        """Updates the look of the text bar based on what is happening."""
        if mode == "normal":
            self.instruction_label.setStyleSheet("font-size: 32px; color: black; background-color: rgba(240, 240, 240, 0.9); font-weight: bold;")
        elif mode == "alert":
            self.instruction_label.setStyleSheet("font-size: 34px; color: white; background-color: red; font-weight: bold;")
        elif mode == "success":
            self.instruction_label.setStyleSheet("font-size: 30px; color: black; background-color: #ccffcc;")

    def show_next_marker(self):
        if self.current_step >= len(self.keys_map):
            self.finish_calibration_phase()
            return

        name, (x_frac, y_frac, key) = self.keys_map[self.current_step]

        screen_w = self.width()
        screen_h = self.height()
        dot_w = self.dot_label.width()
        dot_h = self.dot_label.height()

        # Calculate exact pixel position
        x = int(screen_w * x_frac - dot_w / 2)
        y = int(screen_h * y_frac - dot_h / 2)

        # Update Dot: Put the KEY letter inside the dot
        self.dot_label.setText(key.upper())
        self.dot_label.move(x, y)
        self.dot_label.setVisible(True)
        self.dot_label.raise_()

        # Move text out of the way (if dot is low, put text high)
        if y > screen_h / 2:
            self.instruction_label.setGeometry(0, 0, screen_w, 100)
        else:
            self.instruction_label.setGeometry(0, screen_h - 100, screen_w, 100)

        self.update_instruction_style("normal")
        
        # --- HERE IS THE TEXT UPDATE YOU ASKED FOR ---
        self.instruction_label.setText(f"Look at the DOT and Press '{key.upper()}'")
        
        print(f"\n➡️ Step {self.current_step + 1}: Waiting for '{key.upper()}' at {name}")
        self.is_processing = False

    def keyPressEvent(self, event):
        # Ignore if busy or finished
        if self.current_step >= len(self.keys_map) or self.is_processing:
            return

        user_key = event.text().lower()
        expected_key = self.keys_map[self.current_step][1][2].lower()

        # Allow Escape to quit
        if event.key() == Qt.Key_Escape:
            self.close()
            return

        # CHECK IF USER PRESSED THE CORRECT KEY
        if user_key == expected_key:
            name = self.keys_map[self.current_step][0]
            
            # Lock input
            self.is_processing = True
            
            # --- VISUAL FEEDBACK FOR 1.5s WAIT ---
            self.update_instruction_style("alert")
            self.instruction_label.setText(f"HOLD GAZE on '{name}' ... Calibrating (1.5s)")
            
            # Force UI update
            QApplication.processEvents() 
            print(f"⏳ Holding for 1.5 seconds for '{name}'...")

            # Wait 1.5 Seconds, then Capture
            QTimer.singleShot(1500, lambda: self.perform_calibration_capture(name, user_key))

    def perform_calibration_capture(self, name, user_key):
        """Called after the 1.5 second delay"""
        
        # Capture Data
        features_before = len(self.gaze_tracker.calibration_data.get('features', []))
        self.gaze_tracker.calibrate_point(name, key_char=user_key)
        features_after = len(self.gaze_tracker.calibration_data.get('features', []))
        
        captured_count = features_after - features_before

        if captured_count == 0:
            print(f"⚠️ No eyes detected for {name}. Retrying.")
            self.instruction_label.setStyleSheet("font-size: 28px; color: yellow; background-color: black; font-weight: bold;")
            self.instruction_label.setText(f"⚠️ NO EYES FOUND! Try again. Press '{user_key.upper()}'")
            self.is_processing = False # Allow retry
            return 

        print(f"✅ Captured {captured_count} frames for {name}")
        self.dot_label.setVisible(False)
        self.current_step += 1
        
        # Short delay before showing next dot
        QTimer.singleShot(500, self.show_next_marker)

    def finish_calibration_phase(self):
        print("✅ Calibration Data Collection Complete.")
        self.update_instruction_style("success")
        self.instruction_label.setText("Processing Data & Training Model...")
        self.dot_label.setVisible(False)
        QApplication.processEvents()

        # Train Model
        self.gaze_tracker.train()

        # Save Data
        with open("calibration_data.json", "w") as f:
            json.dump(self.gaze_tracker.calibration_points, f, indent=4)
        
        self.gaze_tracker.start_tracking()

        # Start Visual Verification
        self.run_visual_replay()

    # ---------------------------------------------------------
    #  VISUAL REPLAY (Blue Dot)
    # ---------------------------------------------------------
    def run_visual_replay(self):
        print("📊 Starting Visual Replay...")
        self.instruction_label.setText("Verification: Blue Dot shows where the model thinks you looked.")
        
        self.predicted_points = []
        self.ground_truth_points = []
        screen_w, screen_h = self.width(), self.height()
        
        # Generate predictions based on stored calibration data
        for name, values in self.gaze_tracker.calibration_points.items():
            if name in positions:
                x_frac, y_frac, _ = positions[name]
                gx = x_frac * screen_w
                gy = y_frac * screen_h
                
                # Retrieve offsets stored by tracker
                # Assuming format: [frames, key, dx, dy, w]
                if len(values) >= 5:
                    dx, dy, w = values[2], values[3], values[4]
                    px = gx + dx * w
                    py = gy + dy * w
                    
                    self.predicted_points.append((px, py))
                    self.ground_truth_points.append((gx, gy))

        self.replay_index = 0
        self.cursor_label.setVisible(True)
        self.cursor_label.raise_()

        self.replay_timer = QTimer(self)
        self.replay_timer.timeout.connect(self.move_replay_cursor)
        self.replay_timer.start(800) # Move every 0.8 seconds

    def move_replay_cursor(self):
        if self.replay_index >= len(self.predicted_points):
            self.replay_timer.stop()
            self.cursor_label.setVisible(False)
            self.generate_statistical_report() # Run the math now
            return

        x, y = self.predicted_points[self.replay_index]
        self.cursor_label.move(int(x), int(y))
        print(f"📍 Replay Point {self.replay_index}: {int(x)}, {int(y)}")
        self.replay_index += 1

    # ---------------------------------------------------------
    #  STATISTICAL REPORT (Graphs & JSON)
    # ---------------------------------------------------------
    def generate_statistical_report(self):
        self.instruction_label.setText("Generating accuracy graphs... Please wait.")
        QApplication.processEvents()

        if not self.predicted_points:
            print("❌ No data to evaluate.")
            self.close()
            return

        pred = np.array(self.predicted_points)
        gt = np.array(self.ground_truth_points)
        
        # 1. Euclidean Distance
        euclidean = np.linalg.norm(pred - gt, axis=1)
        mean_euc = np.mean(euclidean)

        # 2. Angular Error (Assumption: Screen is 1000 arbitrary units away)
        def ang_err(p, g):
            p3 = np.array([p[0], p[1], 1000])
            g3 = np.array([g[0], g[1], 1000])
            norm_p = np.linalg.norm(p3)
            norm_g = np.linalg.norm(g3)
            if norm_p == 0 or norm_g == 0: return 0
            cos = np.clip(np.dot(p3, g3) / (norm_p * norm_g), -1, 1)
            return math.degrees(math.acos(cos))

        angular = [ang_err(p, g) for p, g in zip(pred, gt)]
        mean_ang = np.mean(angular) if angular else 0

        # 3. Generate Plots
        try:
            # Scatter Plot
            plt.figure(figsize=(10, 6))
            pred_x, pred_y = zip(*self.predicted_points)
            gt_x, gt_y = zip(*self.ground_truth_points)
            plt.scatter(gt_x, gt_y, label="Target (Real)", color="green", s=150, marker='o')
            plt.scatter(pred_x, pred_y, label="Predicted (Gaze)", color="red", s=100, marker='x')
            
            # Draw lines connecting them
            for i in range(len(gt_x)):
                plt.plot([gt_x[i], pred_x[i]], [gt_y[i], pred_y[i]], color="gray", linestyle="--", alpha=0.5)

            plt.gca().invert_yaxis()
            plt.legend()
            plt.title(f"Gaze Accuracy (Mean Error: {mean_euc:.1f}px)")
            plt.savefig("calibration_accuracy_scatter.png")
            plt.close()

            print("✅ 'calibration_accuracy_scatter.png' saved.")

        except Exception as e:
            print(f"⚠️ Error plotting: {e}")

        # 4. Save Summary
        summary = {
            "mean_euclidean_error_px": round(mean_euc, 2),
            "mean_angular_error_deg": round(mean_ang, 2),
            "points_evaluated": len(pred)
        }
        with open("evaluation_summary.json", "w") as f:
            json.dump(summary, f, indent=4)

        self.instruction_label.setText("Done! Results saved. Closing...")
        QTimer.singleShot(2000, self.close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalibrationWindow()
    window.show()
    sys.exit(app.exec_())