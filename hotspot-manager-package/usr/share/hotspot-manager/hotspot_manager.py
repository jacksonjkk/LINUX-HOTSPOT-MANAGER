import sys
import subprocess
import tempfile
import os
from PyQt5 import QtWidgets, QtCore, QtGui

# Configuration will be loaded from /etc/hotspot-manager/config.conf
CONFIG_FILE = "/etc/hotspot-manager/config.conf"

def load_config():
    """Load configuration from file or use defaults"""
    config = {
        "HOTSPOT_NAME": "ParrotHotspot",
        "HOTSPOT_PASSWORD": "Parrot123",
        "INTERNET_ADAPTER": "wlo1", 
        "HOTSPOT_ADAPTER": "wlx20235199be72"
    }
    
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            config[key.strip()] = value.strip()
    except Exception as e:
        print(f"Warning: Could not load config: {e}")
    
    return config

config = load_config()
HOTSPOT_NAME = config["HOTSPOT_NAME"]
HOTSPOT_PASSWORD = config["HOTSPOT_PASSWORD"]
INTERNET_ADAPTER = config["INTERNET_ADAPTER"]
HOTSPOT_ADAPTER = config["HOTSPOT_ADAPTER"]

class CircularButton(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(120, 120)
        self.is_running = False
        self.hovered = False
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Draw outer circle with gradient
        gradient = QtGui.QRadialGradient(60, 60, 60)
        
        if self.is_running:
            # Red gradient for running state
            gradient.setColorAt(0, QtGui.QColor(255, 80, 80))
            gradient.setColorAt(0.7, QtGui.QColor(220, 50, 50))
            gradient.setColorAt(1, QtGui.QColor(180, 30, 30))
        else:
            # Blue gradient for stopped state
            gradient.setColorAt(0, QtGui.QColor(80, 150, 255))
            gradient.setColorAt(0.7, QtGui.QColor(50, 120, 220))
            gradient.setColorAt(1, QtGui.QColor(30, 100, 180))
            
        if self.hovered:
            # Create a new gradient for hover effect
            if self.is_running:
                gradient.setColorAt(0, QtGui.QColor(255, 100, 100))
                gradient.setColorAt(0.7, QtGui.QColor(240, 70, 70))
                gradient.setColorAt(1, QtGui.QColor(200, 50, 50))
            else:
                gradient.setColorAt(0, QtGui.QColor(100, 170, 255))
                gradient.setColorAt(0.7, QtGui.QColor(70, 140, 240))
                gradient.setColorAt(1, QtGui.QColor(50, 120, 200))
        
        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen(QtGui.QColor(50, 50, 50), 2))
        painter.drawEllipse(5, 5, 110, 110)
        
        # Draw inner circle for depth
        inner_gradient = QtGui.QRadialGradient(60, 60, 40)
        if self.is_running:
            inner_gradient.setColorAt(0, QtGui.QColor(255, 120, 120))
            inner_gradient.setColorAt(1, QtGui.QColor(200, 60, 60))
        else:
            inner_gradient.setColorAt(0, QtGui.QColor(120, 180, 255))
            inner_gradient.setColorAt(1, QtGui.QColor(80, 140, 220))
            
        painter.setBrush(QtGui.QBrush(inner_gradient))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(25, 25, 70, 70)
        
        # Draw text
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
        painter.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        text = "STOP" if self.is_running else "START"
        painter.drawText(self.rect(), QtCore.Qt.AlignCenter, text)
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
            
    def enterEvent(self, event):
        self.hovered = True
        self.update()
        
    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        
    clicked = QtCore.pyqtSignal()

class AdvancedSettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Advanced Settings")
        self.setFixedSize(400, 300)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()
        
        # Title
        title_label = QtWidgets.QLabel("Hotspot Configuration")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # SSID input
        ssid_layout = QtWidgets.QHBoxLayout()
        ssid_label = QtWidgets.QLabel("SSID:")
        ssid_label.setFixedWidth(80)
        self.ssid_input = QtWidgets.QLineEdit()
        self.ssid_input.setText(HOTSPOT_NAME)
        self.ssid_input.setPlaceholderText("Enter hotspot name")
        ssid_layout.addWidget(ssid_label)
        ssid_layout.addWidget(self.ssid_input)
        layout.addLayout(ssid_layout)
        
        # Password input
        password_layout = QtWidgets.QHBoxLayout()
        password_label = QtWidgets.QLabel("Password:")
        password_label.setFixedWidth(80)
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setText(HOTSPOT_PASSWORD)
        self.password_input.setPlaceholderText("Enter hotspot password")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # Show password checkbox
        self.show_password_check = QtWidgets.QCheckBox("Show password")
        self.show_password_check.toggled.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_check)
        
        layout.addSpacing(20)
        
        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.save_btn = QtWidgets.QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QtWidgets.QLabel("")
        self.status_label.setStyleSheet("color: #ff6666; margin-top: 10px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def toggle_password_visibility(self, checked):
        if checked:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
    
    def save_settings(self):
        new_ssid = self.ssid_input.text().strip()
        new_password = self.password_input.text().strip()
        
        if not new_ssid:
            self.status_label.setText("SSID cannot be empty")
            return
        
        if not new_password:
            self.status_label.setText("Password cannot be empty")
            return
        
        if len(new_password) < 8:
            self.status_label.setText("Password must be at least 8 characters")
            return
        
        # Create script to update configuration
        script_content = f"""#!/bin/bash
# Update hotspot configuration
echo "Updating hotspot configuration..."
echo "HOTSPOT_NAME={new_ssid}" > {CONFIG_FILE}
echo "HOTSPOT_PASSWORD={new_password}" >> {CONFIG_FILE}
echo "INTERNET_ADAPTER={INTERNET_ADAPTER}" >> {CONFIG_FILE}
echo "HOTSPOT_ADAPTER={HOTSPOT_ADAPTER}" >> {CONFIG_FILE}
echo "Configuration updated successfully"
"""
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
                f.write(script_content)
                script_path = f.name
            
            os.chmod(script_path, 0o755)
            result = self.parent.run_as_root([script_path])
            
            # Clean up
            try:
                os.unlink(script_path)
            except:
                pass
            
            if result.returncode == 0:
                # Update global variables
                global HOTSPOT_NAME, HOTSPOT_PASSWORD
                HOTSPOT_NAME = new_ssid
                HOTSPOT_PASSWORD = new_password
                
                # Update parent's status if hotspot is running
                if self.parent.circular_btn.is_running:
                    QtWidgets.QMessageBox.information(self, "Restart Required", 
                                                    "Hotspot configuration updated.\n"
                                                    "Please restart the hotspot for changes to take effect.")
                
                self.accept()
            else:
                self.status_label.setText(f"Failed to update configuration: {result.stderr}")
                
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

class HotspotManager(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parrot OS Hotspot Manager")
        self.setGeometry(300, 300, 500, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: Arial;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QTableWidget {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 5px;
                gridline-color: #555555;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #555555;
            }
            QTableWidget::item:selected {
                background-color: #505050;
            }
            QHeaderView::section {
                background-color: #404040;
                color: #ffffff;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            QPushButton {
                background-color: #404040;
                color: #ffffff;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #606060;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px;
            }
            QCheckBox {
                color: #ffffff;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #3c3c3c;
                border: 1px solid #555555;
            }
            QCheckBox::indicator:checked {
                background-color: #66aaff;
                border: 1px solid #555555;
            }
        """)
        self.setup_ui()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_devices)
        self.timer.start(5000)

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title_label = QtWidgets.QLabel("Hotspot Manager")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        # Circular button container
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QVBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        
        self.circular_btn = CircularButton()
        self.circular_btn.clicked.connect(self.toggle_hotspot)
        button_layout.addWidget(self.circular_btn)
        
        button_container.setLayout(button_layout)
        main_layout.addWidget(button_container)

        # Status display
        status_container = QtWidgets.QWidget()
        status_layout = QtWidgets.QVBoxLayout()
        
        self.status_label = QtWidgets.QLabel("Hotspot Status: Stopped")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        status_layout.addWidget(self.status_label)
        
        status_container.setLayout(status_layout)
        main_layout.addWidget(status_container)

        # Connected devices section
        devices_label = QtWidgets.QLabel("Connected Devices")
        devices_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        main_layout.addWidget(devices_label)

        self.devices_table = QtWidgets.QTableWidget()
        self.devices_table.setColumnCount(2)
        self.devices_table.setHorizontalHeaderLabels(["IP Address", "MAC Address"])
        self.devices_table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.devices_table)

        # Advanced settings button
        self.advanced_btn = QtWidgets.QPushButton("Advanced ⚙️")
        self.advanced_btn.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #ffffff;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
        """)
        self.advanced_btn.clicked.connect(self.show_advanced_settings)
        main_layout.addWidget(self.advanced_btn)

        self.setLayout(main_layout)

    def show_advanced_settings(self):
        dialog = AdvancedSettingsDialog(self)
        dialog.exec_()

    def toggle_hotspot(self):
        if self.circular_btn.is_running:
            self.stop_hotspot()
        else:
            self.start_hotspot()

    def run_as_root(self, command):
        """Run a command using Polkit (graphical root prompt)."""
        full_command = ["pkexec"] + command
        return subprocess.run(full_command, capture_output=True, text=True)

    def create_stop_script(self):
        """Create a temporary shell script that ONLY stops processes without touching the interface"""
        script_content = f"""#!/bin/bash
echo "Stopping hotspot processes..."

# Method 1: Stop by adapter name (primary method) - this is the safest
create_ap --stop {HOTSPOT_ADAPTER} 2>/dev/null || true
sleep 2

# Method 2: Stop by SSID
create_ap --stop {HOTSPOT_NAME} 2>/dev/null || true
sleep 1

# Method 3: Kill create_ap processes gently
pkill -f create_ap 2>/dev/null || true
sleep 1

# Method 4: Kill related services gently
pkill -f hostapd 2>/dev/null || true
pkill -f dnsmasq 2>/dev/null || true
sleep 1

# Method 5: Only if still running, force kill
if pgrep -f create_ap > /dev/null; then
    pkill -9 -f create_ap 2>/dev/null || true
    pkill -9 -f hostapd 2>/dev/null || true
    pkill -9 -f dnsmasq 2>/dev/null || true
fi

# DO NOT TOUCH THE INTERFACE - leave it as is
echo "Hotspot processes stopped - interface left untouched"
"""
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write(script_content)
            script_path = f.name
        
        # Make script executable
        os.chmod(script_path, 0o755)
        return script_path

    def start_hotspot(self):
        # Start create_ap in daemon mode
        result = self.run_as_root(["create_ap", "--daemon", INTERNET_ADAPTER, HOTSPOT_ADAPTER, HOTSPOT_NAME, HOTSPOT_PASSWORD])
        if result.returncode == 0:
            self.circular_btn.is_running = True
            self.status_label.setText("Hotspot Status: Running")
            self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; color: #ff6666;")
        else:
            # Show error message if starting failed
            err = result.stderr.strip() if result.stderr else ""
            self.status_label.setText(f"Hotspot Status: Failed to start ({err})")
            self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; color: #ff6666;")
        
        self.circular_btn.update()

    def stop_hotspot(self):
        """Stop hotspot using a single script to avoid multiple authentication prompts"""
        try:
            # Create the stop script
            script_path = self.create_stop_script()
            
            # Execute the script with root privileges (only one authentication required)
            result = self.run_as_root([script_path])
            
            # Clean up the temporary script
            try:
                os.unlink(script_path)
            except:
                pass
            
            # Check if stop was successful
            QtCore.QTimer.singleShot(3000, self.verify_stop_status)
            
            # Show immediate feedback
            self.status_label.setText("Hotspot Status: Stopping...")
            self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; color: #ffaa66;")
            
        except Exception as e:
            self.show_stop_error([("script_execution", -1, "", str(e))])

    def verify_stop_status(self):
        """Verify if hotspot actually stopped after the script execution"""
        still_running = self.is_hotspot_running()
        
        if not still_running:
            self.circular_btn.is_running = False
            self.status_label.setText("Hotspot Status: Stopped")
            self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; color: #66aaff;")
            self.devices_table.setRowCount(0)
        else:
            # If still running, try alternative method
            self.fallback_stop_method()
        
        self.circular_btn.update()

    def fallback_stop_method(self):
        """Fallback method if the script approach fails - uses safe commands only"""
        logs = []
        
        # Try the most reliable single command (safe version)
        r = self.run_as_root(["pkill", "-9", "-f", "create_ap"])
        logs.append(("force_kill_create_ap", r.returncode, r.stdout, r.stderr))
        
        # Wait and check again
        QtCore.QTimer.singleShot(2000, lambda: self.final_stop_verification(logs))

    def final_stop_verification(self, logs):
        """Final verification after fallback method"""
        still_running = self.is_hotspot_running()
        
        if not still_running:
            self.circular_btn.is_running = False
            self.status_label.setText("Hotspot Status: Stopped")
            self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; color: #66aaff;")
            self.devices_table.setRowCount(0)
        else:
            self.show_stop_error(logs)
        
        self.circular_btn.update()

    def show_stop_error(self, logs):
        """Display detailed error information when stopping fails"""
        detailed = []
        for tag, rc, out, err in logs:
            entry = f"--- {tag} (return code: {rc}) ---"
            if out:
                entry += f"\nstdout: {out}"
            if err:
                entry += f"\nstderr: {err}"
            detailed.append(entry)

        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("Failed to Stop Hotspot")
        dlg.setIcon(QtWidgets.QMessageBox.Critical)
        dlg.setText("The hotspot could not be stopped. This might be due to:\n\n"
                   "• create_ap process not responding\n"
                   "• Network interface busy\n\n"
                   "Try stopping it manually from terminal with:\n"
                   f"sudo create_ap --stop {HOTSPOT_ADAPTER}\n\n"
                   "or\n\n"
                   "sudo pkill -9 -f create_ap")
        dlg.setDetailedText("\n\n".join(detailed) or "No additional output")
        dlg.exec_()

    def is_hotspot_running(self):
        """Check if hotspot is running by looking for processes only"""
        try:
            # Check for create_ap process
            p1 = subprocess.run(["pgrep", "-f", "create_ap"], capture_output=True, text=True)
            if p1.stdout.strip():
                return True

            # Check for hostapd process (used by create_ap)
            p2 = subprocess.run(["pgrep", "-f", "hostapd"], capture_output=True, text=True)
            if p2.stdout.strip():
                return True

        except Exception as e:
            print(f"Error checking hotspot status: {e}")
            
        return False

    def update_devices(self):
        # Refresh status label based on actual running state
        current_status = self.is_hotspot_running()
        
        # Update UI only if status changed
        if current_status != self.circular_btn.is_running:
            self.circular_btn.is_running = current_status
            self.circular_btn.update()
            
        if current_status:
            self.status_label.setText("Hotspot Status: Running")
            self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; color: #ff6666;")
            devices = self.get_connected_devices()
            self.devices_table.setRowCount(len(devices))
            for row, device in enumerate(devices):
                self.devices_table.setItem(row, 0, QtWidgets.QTableWidgetItem(device["IP"]))
                self.devices_table.setItem(row, 1, QtWidgets.QTableWidgetItem(device["MAC"]))
        else:
            self.status_label.setText("Hotspot Status: Stopped")
            self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; color: #66aaff;")
            self.devices_table.setRowCount(0)

    def get_connected_devices(self):
        devices = []
        try:
            with open("/proc/net/arp", "r") as f:
                for line in f.readlines()[1:]:
                    parts = line.split()
                    if len(parts) >= 4:
                        ip = parts[0]
                        mac = parts[3]
                        if mac != "00:00:00:00:00:00":  # Filter out incomplete entries
                            devices.append({"IP": ip, "MAC": mac})
        except FileNotFoundError:
            pass
        return devices

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HotspotManager()
    window.show()
    sys.exit(app.exec_())