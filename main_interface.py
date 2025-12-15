import sys
import json
import threading
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPoint, QElapsedTimer
from gaze_tracker import GazeTracker

# Make sure these files exist in your 'screens' folder
from screens.main_menu import MainMenuScreen
from screens.food_screen import FoodScreen
from screens.water_screen import WaterScreen
from screens.tablets_screen import TabletsScreen
from screens.washroom_screen import WashroomScreen
from screens.final_message import FinalMessageScreen

# Hardcoded or loaded calibration values
try:
    with open("calibration_data.json", "r") as f:
        calibration_points = json.load(f)
except FileNotFoundError:
    print("Warning: calibration_data.json not found. Using defaults.")
    calibration_points = {}

class MainInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gaze Controlled Interface")
        self.setWindowState(Qt.WindowFullScreen)

        self.gaze_tracker = GazeTracker()
        threading.Thread(target=self.gaze_tracker.start_tracking, daemon=True).start()

        self.stack = QStackedWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        # --- INITIALIZING SCREENS ---
        # Ensuring (self) is present to prevent crashes
        self.main_menu = MainMenuScreen(self)
        self.food_screen = FoodScreen(self)
        self.water_screen = WaterScreen(self)
        self.tablets_screen = TabletsScreen(self)
        self.washroom_screen = WashroomScreen(self)
        self.final_message_screen = FinalMessageScreen(self)

        # Add to stack
        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.food_screen)
        self.stack.addWidget(self.water_screen)
        self.stack.addWidget(self.tablets_screen)
        self.stack.addWidget(self.washroom_screen)
        self.stack.addWidget(self.final_message_screen)

        self.stack.setCurrentWidget(self.main_menu)
        self.buttons = self.main_menu.buttons

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_gaze)
        self.timer.start(50) # Fast refresh for smooth motion
        self.hovered_button = None
        self.hover_timer = QElapsedTimer()
        self.prev_cursor_pos = pyautogui.position()

    def switch_screen(self, screen_widget):
        self.stack.setCurrentWidget(screen_widget)
        self.buttons = getattr(screen_widget, "buttons", [])

    def show_final_message(self, message):
        self.final_message_screen.set_message(message)
        self.switch_screen(self.final_message_screen)

    def check_gaze(self):
        smoothed_dx, smoothed_dy = self.gaze_tracker.get_latest_offsets()
        screen_w, screen_h = pyautogui.size()
        CENTER_X, CENTER_Y = screen_w // 2, screen_h // 2
        pyautogui.FAILSAFE = False

        # Direction configuration
        INVERT_X = True
        INVERT_Y = False
        dir_x = -1 if INVERT_X else 1
        dir_y = -1 if INVERT_Y else 1

        all_dx = [val[2] for val in calibration_points.values()]
        all_dy = [val[3] for val in calibration_points.values()]

        if not all_dx: all_dx = [0]
        if not all_dy: all_dy = [0]

        dx_range = max(all_dx) - min(all_dx)
        dy_range = max(all_dy) - min(all_dy)

        dy_range = max(dy_range, 0.01)
        dx_range = max(dx_range, 0.01)

        # --- OPTIMIZATION START: SITTING TO SIDE COMPENSATION ---
        # If a user sits to the right, horizontal eye movement looks "compressed" to the camera.
        # We use a LOWER dampener for X (1.8) to make it MORE sensitive than Y (2.2).
        # This ensures looking Right/Left reaches the edge easily, even from an angle.
        
        DAMPENER_X = 1.8  # Lower = More Sensitive (Easier to move Left/Right)
        DAMPENER_Y = 2.2  # Higher = More Stable (Precise Up/Down)
        
        SCALE_X = min(screen_w / (dx_range * DAMPENER_X), 40000)
        SCALE_Y = min(screen_h / (dy_range * DAMPENER_Y), 40000)
        # --- OPTIMIZATION END ---

        # Calculate Center
        if 'Center' in calibration_points:
            center_dx = calibration_points['Center'][2]
            center_dy = calibration_points['Center'][3]
        elif len(all_dx) > 0:
            center_dx = sum(all_dx) / len(all_dx)
            center_dy = sum(all_dy) / len(all_dy)
        else:
            center_dx = 0
            center_dy = 0

        dx_relative = smoothed_dx - center_dx
        dy_relative = smoothed_dy - center_dy

        screen_x = CENTER_X + int(dir_x * dx_relative * SCALE_X)
        screen_y = CENTER_Y + int(dir_y * dy_relative * SCALE_Y)
        screen_x = max(0, min(screen_w - 1, screen_x))
        screen_y = max(0, min(screen_h - 1, screen_y))

        prev_x, prev_y = self.prev_cursor_pos

        # --- SPEED SETTING ---
        # 0.15 is the "Normal" computer cursor feel
        SMOOTHING_FACTOR = 0.15
        
        smooth_x = int(prev_x + SMOOTHING_FACTOR * (screen_x - prev_x))
        smooth_y = int(prev_y + SMOOTHING_FACTOR * (screen_y - prev_y))
        
        pyautogui.moveTo(smooth_x, smooth_y)
        self.prev_cursor_pos = (smooth_x, smooth_y)

        for btn in self.buttons:
            btn_pos = btn.mapToGlobal(QPoint(0, 0))
            btn_rect = btn.geometry()
            btn_rect.moveTopLeft(btn_pos)

            if btn_rect.contains(QPoint(smooth_x, smooth_y)):
                if self.hovered_button != btn:
                    self.hovered_button = btn
                    self.hover_timer.restart()
                else:
                    # --- DWELL TIME SETTING ---
                    # 3000 ms = 3 seconds
                    if self.hover_timer.hasExpired(3000):
                        try:
                            btn_text = btn.text()
                            print(f"COMMAND TRIGGERED: {btn_text}") 
                        except:
                            print("COMMAND TRIGGERED: Unknown Button")
                        
                        btn.click()
                        self.hovered_button = None
                        self.hover_timer.invalidate()
                break
        else:
            self.hovered_button = None
            self.hover_timer.invalidate()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainInterface()
    window.show()
    sys.exit(app.exec_())