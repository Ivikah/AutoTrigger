import sys
import time
import math
from typing import Tuple

import keyboard
import mss
import pydirectinput
from PySide6.QtCore import (QObject, QRunnable, QSize, Qt, QThreadPool, Signal,
                            Slot, QTimer, QRect, QPoint)
from PySide6.QtGui import QFont, QPainter, QPen, QColor, QScreen, QCursor
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QMainWindow, 
                               QPushButton, QSlider, QWidget, QComboBox, QLabel, 
                               QLineEdit, QStackedWidget, QHBoxLayout, QVBoxLayout, QSpinBox,
                               QDialog, QListWidget, QDialogButtonBox, QMessageBox)


class DetectionBox(QWidget):
    """A movable, semi-transparent box for visual detection area feedback."""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(20, 20)  # Increased to 20x20 to avoid border overlap
        
        # For dragging
        self.dragging = False
        self.drag_position = QPoint()
        self.locked = False  # Lock state for the box
        
        # Center on screen initially
        screen_geometry = QApplication.instance().primaryScreen().geometry()
        center = screen_geometry.center()
        self.move(center.x() - 10, center.y() - 10)  # Center the 20x20 box
        
    def paintEvent(self, event):
        """Draw the detection box with border and nearly-invisible fill for mouse events."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw a nearly-invisible fill (alpha=1) so the entire box area receives mouse events
        # This won't interfere with detection since we offset by 2 pixels
        painter.fillRect(self.rect(), QColor(255, 0, 0, 1))
        
        # Draw the solid border (red if unlocked, yellow if locked)
        border_color = QColor(255, 255, 0, 255) if self.locked else QColor(255, 0, 0, 255)
        pen = QPen(border_color, 2)
        painter.setPen(pen)
        painter.drawRect(1, 1, 18, 18)  # Draw border around the 20x20 box
        
    def mousePressEvent(self, event):
        """Start dragging the box (if not locked)."""
        if event.button() == Qt.LeftButton and not self.locked:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Move the box while dragging (if not locked)."""
        if self.dragging and not self.locked:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Stop dragging the box."""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
    
    def get_detection_rect(self) -> QRect:
        """Returns the inner 16x16 detection area (excluding the border)."""
        pos = self.pos()
        # Offset by 2 pixels to get the inner 16x16 area, avoiding the 2-pixel border
        return QRect(pos.x() + 2, pos.y() + 2, 16, 16)
    
    def set_locked(self, locked: bool):
        """Set the lock state of the box."""
        self.locked = locked
        self.update()  # Redraw to show color change
    
    def is_locked(self) -> bool:
        """Check if the box is locked."""
        return self.locked
    
    def get_position(self) -> QPoint:
        """Get the current position of the box."""
        return self.pos()
    
    def set_position(self, position: QPoint):
        """Set the position of the box."""
        self.move(position)
    
    def reset_to_center(self):
        """Reset the box to the center of the screen."""
        screen_geometry = QApplication.instance().primaryScreen().geometry()
        center = screen_geometry.center()
        self.move(center.x() - 10, center.y() - 10)


class PositionManagerDialog(QDialog):
    """Dialog for managing saved detection box positions."""
    
    # ==================== DEFAULT POSITIONS ====================
    # Add your default positions here in the format: "Name": QPoint(x, y)
    DEFAULT_POSITIONS = {
        # Example: "Top Left": QPoint(100, 100),
        # Example: "Center": QPoint(960, 540),
    }
    # ===========================================================
    
    def __init__(self, parent=None, current_position: QPoint = None):
        super().__init__(parent)
        self.setWindowTitle("Manage Positions")
        self.setModal(True)
        self.setMinimumSize(400, 300)
        
        self.current_position = current_position
        self.saved_positions = dict(self.DEFAULT_POSITIONS)  # Start with defaults
        self.selected_position = None
        
        self.init_ui()
        
        # Apply dark theme
        self.setStyleSheet(parent.styleSheet() if parent else "")
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Saved Positions")
        title_font = QFont("Segoe UI", 11, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # List of saved positions
        self.position_list = QListWidget()
        self.position_list.itemDoubleClicked.connect(self.load_selected_position)
        self.refresh_position_list()
        layout.addWidget(self.position_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save Current")
        save_button.clicked.connect(self.save_current_position)
        button_layout.addWidget(save_button)
        
        load_button = QPushButton("Load Selected")
        load_button.clicked.connect(self.load_selected_position)
        button_layout.addWidget(load_button)
        
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_selected_position)
        button_layout.addWidget(delete_button)
        
        layout.addLayout(button_layout)
        
        # Dialog buttons
        dialog_buttons = QDialogButtonBox(QDialogButtonBox.Close)
        dialog_buttons.rejected.connect(self.reject)
        layout.addLayout(button_layout)
        layout.addWidget(dialog_buttons)
        
        self.setLayout(layout)
    
    def refresh_position_list(self):
        """Refresh the list of saved positions."""
        self.position_list.clear()
        for name, pos in self.saved_positions.items():
            self.position_list.addItem(f"{name} ({pos.x()}, {pos.y()})")
    
    def save_current_position(self):
        """Save the current position with a user-provided name."""
        from PySide6.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, "Save Position", "Enter a name for this position:")
        if ok and name:
            if name in self.saved_positions:
                reply = QMessageBox.question(
                    self, "Overwrite?",
                    f"Position '{name}' already exists. Overwrite?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply != QMessageBox.Yes:
                    return
            
            self.saved_positions[name] = QPoint(self.current_position)
            self.refresh_position_list()
            QMessageBox.information(self, "Saved", f"Position '{name}' saved successfully!")
    
    def load_selected_position(self):
        """Load the selected position."""
        current_item = self.position_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a position to load.")
            return
        
        # Extract name from the list item text (format: "Name (x, y)")
        item_text = current_item.text()
        name = item_text.split(" (")[0]
        
        if name in self.saved_positions:
            self.selected_position = self.saved_positions[name]
            self.accept()
    
    def delete_selected_position(self):
        """Delete the selected position."""
        current_item = self.position_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a position to delete.")
            return
        
        # Extract name from the list item text
        item_text = current_item.text()
        name = item_text.split(" (")[0]
        
        # Don't allow deleting default positions
        if name in self.DEFAULT_POSITIONS:
            QMessageBox.warning(self, "Cannot Delete", "Cannot delete default positions.")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            del self.saved_positions[name]
            self.refresh_position_list()
    
    def get_selected_position(self) -> QPoint:
        """Get the position that was selected to load."""
        return self.selected_position


class ColorPickerOverlay(QWidget):
    """Full-screen overlay for picking a color from anywhere on screen."""
    color_picked = Signal(tuple)
    cancelled = Signal()
    
    def __init__(self):
        super().__init__()
        geometry = QApplication.instance().primaryScreen().geometry()
        self.setGeometry(geometry)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CrossCursor)
        self.show()
        self.activateWindow()
        self.raise_()
    
    def mousePressEvent(self, event):
        """Pick the color at the clicked position."""
        pos = event.globalPosition().toPoint()
        
        # Capture a single pixel at the clicked position
        with mss.mss() as sct:
            region = {"top": pos.y(), "left": pos.x(), "width": 1, "height": 1}
            img = sct.grab(region)
            r, g, b = img.pixel(0, 0)
            self.color_picked.emit((r, g, b))
        
        self.close()
    
    def keyPressEvent(self, event):
        """Cancel on Escape key."""
        if event.key() == Qt.Key_Escape:
            self.cancelled.emit()
            self.close()


class WorkerSignals(QObject):
    """Defines the signals available from a running worker thread."""
    detection_changed = Signal(bool)


class DetectionWorker(QRunnable):
    """Worker thread for background change detection."""
    
    def __init__(self, base_color: Tuple[int, int, int], tolerance: int, detection_rect: QRect):
        super().__init__()
        self.signals = WorkerSignals()
        self.is_running = True
        self.base_r, self.base_g, self.base_b = base_color
        self.tolerance = tolerance
        self.detection_rect = detection_rect
    
    @staticmethod
    def color_distance(r1, g1, b1, r2, g2, b2):
        """Calculates the Euclidean distance between two RGB colors."""
        return math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)
    
    @Slot()
    def run(self):
        """Main worker loop for screen capture and analysis."""
        with mss.mss() as sct:
            while self.is_running:
                start_time = time.time()
                
                # Capture the 16x16 detection area
                region = {
                    "top": self.detection_rect.top(),
                    "left": self.detection_rect.left(),
                    "width": self.detection_rect.width(),
                    "height": self.detection_rect.height()
                }
                
                img = sct.grab(region)
                
                mismatch_count = 0
                for x in range(img.width):
                    for y in range(img.height):
                        r, g, b = img.pixel(x, y)
                        if self.color_distance(r, g, b, self.base_r, self.base_g, self.base_b) > self.tolerance:
                            mismatch_count += 1
                
                # If more than 5 pixels are mismatched, trigger detection
                if mismatch_count > 5:
                    self.signals.detection_changed.emit(True)
                else:
                    self.signals.detection_changed.emit(False)
                
                # Maintain a consistent loop frequency
                elapsed = time.time() - start_time
                if elapsed < 0.03:  # Target ~33 FPS
                    time.sleep(0.03 - elapsed)
    
    def stop(self):
        self.is_running = False
        # Emit False on stop to ensure spamming ceases
        self.signals.detection_changed.emit(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto-Trigger")
        self.setFixedSize(QSize(440, 480))  # Increased to accommodate new features
        
        # Apply dark theme
        self.apply_dark_theme()
        
        self.threadpool = QThreadPool()
        self.worker = None
        self.color_picker_overlay = None
        
        # --- App State ---
        self.base_color = (0, 0, 0)
        self.is_running = False
        
        # --- Detection Box ---
        self.detection_box = DetectionBox()
        self.detection_box.show()
        
        # --- Spam Timer ---
        self.spam_timer = QTimer(self)
        self.spam_timer.setInterval(30)  # 30ms delay between clicks
        self.spam_timer.timeout.connect(self.perform_click)
        
        # --- Auto Reload Timer ---
        self.reload_timer = QTimer(self)
        self.reload_timer.setInterval(1000)  # 1 second default
        self.reload_timer.timeout.connect(self.perform_reload)
        
        # --- Build UI ---
        self.build_ui()
        
        # Set default color
        self.update_base_color((0, 0, 0))
        self.setup_hotkey()
    
    def apply_dark_theme(self):
        """Apply a modern dark theme to the application."""
        dark_stylesheet = """
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #2d2d30;
                color: #e0e0e0;
                border: 1px solid #3f3f46;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #3e3e42;
                border: 1px solid #007acc;
            }
            QPushButton:pressed {
                background-color: #007acc;
            }
            QPushButton:disabled {
                background-color: #2d2d30;
                color: #656565;
            }
            QCheckBox {
                color: #e0e0e0;
                font-size: 10pt;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #3f3f46;
                border-radius: 3px;
                background-color: #2d2d30;
            }
            QCheckBox::indicator:checked {
                background-color: #007acc;
                border: 1px solid #007acc;
            }
            QCheckBox::indicator:hover {
                border: 1px solid #007acc;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #2d2d30;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #007acc;
                width: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #1e8ad6;
            }
            QComboBox {
                background-color: #2d2d30;
                color: #e0e0e0;
                border: 1px solid #3f3f46;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 10pt;
            }
            QComboBox:hover {
                border: 1px solid #007acc;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d30;
                color: #e0e0e0;
                selection-background-color: #007acc;
                border: 1px solid #3f3f46;
            }
            QLineEdit {
                background-color: #2d2d30;
                color: #e0e0e0;
                border: 1px solid #3f3f46;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 1px solid #007acc;
            }
            QSpinBox {
                background-color: #2d2d30;
                color: #e0e0e0;
                border: 1px solid #3f3f46;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 10pt;
            }
            QSpinBox:focus {
                border: 1px solid #007acc;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #3e3e42;
                border: 1px solid #3f3f46;
                border-radius: 2px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #007acc;
            }
        """
        self.setStyleSheet(dark_stylesheet)
    
    def build_ui(self):
        """Build the main UI layout."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Auto-Trigger Configuration")
        title_font = QFont("Segoe UI", 12, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Enable Toggle and Click Delay
        enable_layout = QHBoxLayout()
        self.enable_toggle = QCheckBox("Enable Detection (F6)")
        self.enable_toggle.toggled.connect(self.handle_toggle)
        enable_layout.addWidget(self.enable_toggle)
        
        enable_layout.addStretch()
        
        delay_label = QLabel("Click Delay (ms):")
        enable_layout.addWidget(delay_label)
        
        self.click_delay_input = QSpinBox()
        self.click_delay_input.setMinimum(10)
        self.click_delay_input.setMaximum(1000)
        self.click_delay_input.setValue(30)
        self.click_delay_input.setSuffix(" ms")
        self.click_delay_input.setToolTip("Delay between clicks in milliseconds")
        self.click_delay_input.valueChanged.connect(self.on_click_delay_changed)
        enable_layout.addWidget(self.click_delay_input)
        
        main_layout.addLayout(enable_layout)
        
        # Tolerance Slider
        tolerance_layout = QVBoxLayout()
        tolerance_layout.setSpacing(5)
        tolerance_label = QLabel("Tolerance:")
        self.tolerance_value_label = QLabel("20")
        tolerance_header = QHBoxLayout()
        tolerance_header.addWidget(tolerance_label)
        tolerance_header.addStretch()
        tolerance_header.addWidget(self.tolerance_value_label)
        tolerance_layout.addLayout(tolerance_header)
        
        self.tolerance_slider = QSlider(Qt.Horizontal)
        self.tolerance_slider.setMinimum(1)
        self.tolerance_slider.setMaximum(100)
        self.tolerance_slider.setValue(20)
        self.tolerance_slider.setToolTip("How different a color must be to trigger detection.\nLower is more sensitive.")
        self.tolerance_slider.valueChanged.connect(self.on_tolerance_changed)
        tolerance_layout.addWidget(self.tolerance_slider)
        main_layout.addLayout(tolerance_layout)
        
        # Detection Box Controls
        box_layout = QVBoxLayout()
        box_layout.setSpacing(5)
        box_label = QLabel("Detection Box:")
        box_layout.addWidget(box_label)
        
        # First row of buttons
        box_buttons_row1 = QHBoxLayout()
        self.toggle_box_button = QPushButton("Hide Box")
        self.toggle_box_button.clicked.connect(self.toggle_detection_box)
        box_buttons_row1.addWidget(self.toggle_box_button)
        
        self.lock_box_button = QPushButton("Lock Box")
        self.lock_box_button.setCheckable(True)
        self.lock_box_button.clicked.connect(self.toggle_lock_box)
        box_buttons_row1.addWidget(self.lock_box_button)
        box_layout.addLayout(box_buttons_row1)
        
        # Second row of buttons
        box_buttons_row2 = QHBoxLayout()
        self.reset_box_button = QPushButton("Reset Position")
        self.reset_box_button.clicked.connect(self.reset_detection_box)
        box_buttons_row2.addWidget(self.reset_box_button)
        
        self.manage_positions_button = QPushButton("Save/Load Position")
        self.manage_positions_button.clicked.connect(self.open_position_manager)
        box_buttons_row2.addWidget(self.manage_positions_button)
        box_layout.addLayout(box_buttons_row2)
        
        main_layout.addLayout(box_layout)
        
        # Color Selection Mode
        color_mode_label = QLabel("Color Mode:")
        main_layout.addWidget(color_mode_label)
        
        self.color_mode_combo = QComboBox()
        self.color_mode_combo.addItems(["Enter Hex Value", "Pick from Screen"])
        self.color_mode_combo.currentIndexChanged.connect(self.on_color_mode_changed)
        main_layout.addWidget(self.color_mode_combo)
        
        # Color Input Stack
        self.color_input_stack = QStackedWidget()
        
        # Hex input widget
        self.hex_input = QLineEdit("#000000")
        self.hex_input.textChanged.connect(self.on_hex_input_changed)
        self.color_input_stack.addWidget(self.hex_input)
        
        # Pick color button widget
        self.pick_color_button = QPushButton("Click to Pick Color from Screen")
        self.pick_color_button.clicked.connect(self.start_color_picker)
        self.color_input_stack.addWidget(self.pick_color_button)
        
        main_layout.addWidget(self.color_input_stack)
        
        # Base Color Display
        self.base_color_display = QLabel("Base Color: (Not Set)")
        self.base_color_display.setStyleSheet("padding: 8px; border-radius: 4px;")
        self.base_color_display.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.base_color_display)
        
        # Auto Reload Section
        reload_layout = QVBoxLayout()
        reload_layout.setSpacing(5)
        
        # Reload toggle and delay input
        reload_controls = QHBoxLayout()
        self.auto_reload_toggle = QCheckBox("Auto Reload (Press R)")
        self.auto_reload_toggle.toggled.connect(self.toggle_auto_reload)
        reload_controls.addWidget(self.auto_reload_toggle)
        
        reload_controls.addStretch()
        
        reload_delay_label = QLabel("Delay (s):")
        reload_controls.addWidget(reload_delay_label)
        
        self.reload_delay_input = QSpinBox()
        self.reload_delay_input.setMinimum(1)
        self.reload_delay_input.setMaximum(60)
        self.reload_delay_input.setValue(1)
        self.reload_delay_input.setSuffix(" s")
        self.reload_delay_input.setToolTip("Delay between reload presses in seconds")
        self.reload_delay_input.valueChanged.connect(self.on_reload_delay_changed)
        reload_controls.addWidget(self.reload_delay_input)
        
        reload_layout.addLayout(reload_controls)
        main_layout.addLayout(reload_layout)
        
        # Status Label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_font = QFont("Segoe UI", 10, QFont.Bold)
        self.status_label.setFont(status_font)
        main_layout.addWidget(self.status_label)
        
        main_layout.addStretch()
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
    
    def setup_hotkey(self):
        """Register the F6 hotkey for toggling detection."""
        try:
            keyboard.add_hotkey('f6', self.toggle_detection_hotkey)
            print("F6 hotkey registered successfully.")
        except Exception as e:
            print(f"Failed to register F6 hotkey: {e}")
            print("Please try running the script with administrator privileges.")
            self.status_label.setText("Status: Hotkey failed to register!")
    
    @Slot()
    def toggle_detection_hotkey(self):
        """Toggles the detection state, called by the global hotkey."""
        if self.enable_toggle.isEnabled():
            self.enable_toggle.toggle()
    
    @Slot(int)
    def on_tolerance_changed(self, value):
        """Update the tolerance value label."""
        self.tolerance_value_label.setText(str(value))
    
    @Slot(int)
    def on_click_delay_changed(self, value):
        """Update the spam timer interval when delay changes."""
        if self.spam_timer:
            self.spam_timer.setInterval(value)
    
    @Slot()
    def toggle_detection_box(self):
        """Toggle the visibility of the detection box."""
        if self.detection_box.isVisible():
            self.detection_box.hide()
            self.toggle_box_button.setText("Show Box")
        else:
            self.detection_box.show()
            self.toggle_box_button.setText("Hide Box")
    
    @Slot()
    def reset_detection_box(self):
        """Reset the detection box to the center of the screen."""
        self.detection_box.reset_to_center()
    
    @Slot(bool)
    def toggle_lock_box(self, checked: bool):
        """Toggle the lock state of the detection box."""
        self.detection_box.set_locked(checked)
        if checked:
            self.lock_box_button.setText("Unlock Box")
        else:
            self.lock_box_button.setText("Lock Box")
    
    @Slot()
    def open_position_manager(self):
        """Open the position manager dialog."""
        current_pos = self.detection_box.get_position()
        dialog = PositionManagerDialog(self, current_pos)
        
        if dialog.exec() == QDialog.Accepted:
            selected_pos = dialog.get_selected_position()
            if selected_pos:
                self.detection_box.set_position(selected_pos)
    
    @Slot(bool)
    def toggle_auto_reload(self, checked: bool):
        """Toggle the auto reload feature."""
        if checked:
            self.reload_timer.start()
        else:
            self.reload_timer.stop()
    
    @Slot(int)
    def on_reload_delay_changed(self, value):
        """Update the reload timer interval when delay changes."""
        if self.reload_timer:
            self.reload_timer.setInterval(value * 1000)  # Convert seconds to milliseconds
    
    @Slot()
    def perform_reload(self):
        """Press the R key for reload."""
        pydirectinput.press('r')
    
    @Slot(int)
    def on_color_mode_changed(self, index):
        """Handle color mode selection change."""
        self.color_input_stack.setCurrentIndex(index)
    
    @Slot(str)
    def on_hex_input_changed(self, text: str):
        """Validates hex code and updates the base color."""
        text = text.strip()
        if not text.startswith("#") or len(text) != 7:
            return
        
        try:
            hex_val = text[1:]
            r = int(hex_val[0:2], 16)
            g = int(hex_val[2:4], 16)
            b = int(hex_val[4:6], 16)
            self.update_base_color((r, g, b))
        except (ValueError, IndexError):
            # Invalid hex code, do nothing
            pass
    
    @Slot()
    def start_color_picker(self):
        """Start the color picker overlay."""
        # Clean up any existing overlay first
        if self.color_picker_overlay:
            try:
                self.color_picker_overlay.close()
                self.color_picker_overlay.deleteLater()
            except:
                pass
            self.color_picker_overlay = None
        
        self.status_label.setText("Status: Click anywhere to pick color...")
        self.color_picker_overlay = ColorPickerOverlay()
        self.color_picker_overlay.color_picked.connect(self.on_color_picked)
        self.color_picker_overlay.cancelled.connect(self.on_color_picker_cancelled)
    
    @Slot()
    def on_color_picker_cancelled(self):
        """Handle color picker cancellation."""
        if self.color_picker_overlay:
            try:
                self.color_picker_overlay.close()
                self.color_picker_overlay.deleteLater()
            except:
                pass
            self.color_picker_overlay = None
        self.status_label.setText("Status: Color picking cancelled")
    
    @Slot(tuple)
    def on_color_picked(self, color: Tuple[int, int, int]):
        """Handle the color picked from screen."""
        self.update_base_color(color)
        # Update hex input to reflect the picked color
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        self.hex_input.setText(hex_color)
        
        # Clean up the overlay
        if self.color_picker_overlay:
            try:
                self.color_picker_overlay.close()
                self.color_picker_overlay.deleteLater()
            except:
                pass
            self.color_picker_overlay = None
    
    def update_base_color(self, color: Tuple[int, int, int]):
        """Updates the base color and UI display."""
        self.base_color = color
        self.base_color_display.setText(f"Base Color: RGB{color}")
        
        # Calculate contrast for text color
        luminance = color[0] * 0.299 + color[1] * 0.587 + color[2] * 0.114
        text_color = 'white' if luminance < 140 else 'black'
        
        self.base_color_display.setStyleSheet(
            f"background-color: rgb{color}; "
            f"color: {text_color}; "
            f"padding: 8px; "
            f"border-radius: 4px; "
            f"border: 1px solid #3f3f46;"
        )
        
        if not self.is_running:
            self.enable_toggle.setEnabled(True)
            self.status_label.setText("Status: Ready")
    
    @Slot(bool)
    def handle_toggle(self, checked: bool):
        """Handle the enable/disable toggle."""
        if checked:
            self.start_worker()
        else:
            self.stop_worker()
    
    def start_worker(self):
        """Start the detection worker thread."""
        self.is_running = True
        self.status_label.setText("Status: Running")
        self.color_mode_combo.setEnabled(False)
        self.hex_input.setEnabled(False)
        self.pick_color_button.setEnabled(False)
        self.toggle_box_button.setEnabled(False)
        self.reset_box_button.setEnabled(False)
        self.lock_box_button.setEnabled(False)
        self.manage_positions_button.setEnabled(False)
        self.click_delay_input.setEnabled(False)
        self.reload_delay_input.setEnabled(False)
        
        detection_rect = self.detection_box.get_detection_rect()
        
        self.worker = DetectionWorker(
            base_color=self.base_color,
            tolerance=self.tolerance_slider.value(),
            detection_rect=detection_rect
        )
        self.worker.signals.detection_changed.connect(self.on_detection_changed)
        self.threadpool.start(self.worker)
    
    def stop_worker(self):
        """Stop the detection worker thread."""
        self.is_running = False
        if self.worker:
            self.worker.stop()
        self.spam_timer.stop()
        self.status_label.setText("Status: Stopped")
        self.color_mode_combo.setEnabled(True)
        self.hex_input.setEnabled(True)
        self.pick_color_button.setEnabled(True)
        self.toggle_box_button.setEnabled(True)
        self.reset_box_button.setEnabled(True)
        self.lock_box_button.setEnabled(True)
        self.manage_positions_button.setEnabled(True)
        self.click_delay_input.setEnabled(True)
        self.reload_delay_input.setEnabled(True)
    
    @Slot(bool)
    def on_detection_changed(self, is_changed: bool):
        """Handle detection state changes."""
        if is_changed and self.is_running:
            if not self.spam_timer.isActive():
                self.spam_timer.start()
                self.status_label.setText("Status: SPAMMING")
        else:
            if self.spam_timer.isActive():
                self.spam_timer.stop()
                if self.is_running:
                    self.status_label.setText("Status: Running")
    
    @Slot()
    def perform_click(self):
        """Executes a single mouse click."""
        pydirectinput.click()
    
    def closeEvent(self, event):
        """Clean up when closing the application."""
        self.stop_worker()
        self.reload_timer.stop()
        self.detection_box.close()
        keyboard.remove_all_hotkeys()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())