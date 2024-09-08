import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import Qt

class NordVPNGui(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NordVPN GUI")
        self.setGeometry(100, 100, 500, 600)

        # Set up the main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Apply dark theme styles
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #E0E0E0;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #E0E0E0;
                font-size: 18px;
                padding: 10px;
            }
            QComboBox {
                background-color: #3C3C3C;
                color: #E0E0E0;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
            }
            QComboBox::drop-down {
                border-left: 1px solid #444;
                border-radius: 5px;
            }
            QPushButton {
                color: #E0E0E0;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                background-color: #0033A0;  /* Default color for Connect button */
                position: relative;
            }
            QPushButton:hover {
                background-color: #0056A0;
            }
            QPushButton:pressed {
                background-color: #003A7F;
            }
            QPushButton#disconnect_button {
                background-color: #A00000;
            }
            QPushButton#disconnect_button:hover {
                background-color: #D00000;
            }
            QPushButton#disconnect_button:pressed {
                background-color: #700000;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
                border: 1px solid #666666;
            }
            QPushButton::indicator {
                width: 0px;
                height: 0px;
            }
        """)

        # Status Label
        self.status_label = QLabel("Status: Disconnected")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        # Server Info Label
        self.server_info_label = QLabel("")
        self.server_info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.server_info_label)

        # Country Info Label
        self.country_info_label = QLabel("")
        self.country_info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.country_info_label)

        # Server Type Selection
        self.server_type_combo = QComboBox(self)
        self.server_type_combo.addItems(['Auto', 'Double VPN', 'P2P', 'Onion Over VPN', 'Obfuscated_Servers'])
        self.server_type_combo.currentTextChanged.connect(self.update_server_list)
        self.layout.addWidget(QLabel("Select Server Type:"))
        self.layout.addWidget(self.server_type_combo)

        # Country Selection
        self.country_combo = QComboBox(self)
        self.country_combo.addItems(['Select Country'] + ['Albania', 'Algeria', 'Andorra', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bangladesh', 'Belgium', 'Belize', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia_And_Herzegovina', 'Brazil', 'Brunei_Darussalam', 'Bulgaria', 'Cambodia', 'Canada', 'Cayman_Islands', 'Chile', 'Colombia', 'Costa_Rica', 'Croatia', 'Cyprus', 'Czech_Republic', 'Denmark', 'Dominican_Republic', 'Ecuador', 'Egypt', 'El_Salvador', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Guam', 'Guatemala', 'Honduras', 'Hong_Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Ireland', 'Isle_Of_Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Kazakhstan', 'Kenya', 'Lao_Peoples_Democratic_Republic', 'Latvia', 'Lebanon', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malaysia', 'Malta', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Myanmar', 'Nepal', 'Netherlands', 'New_Zealand', 'Nigeria', 'North_Macedonia', 'Norway', 'Pakistan', 'Panama', 'Papua_New_Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto_Rico', 'Romania', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'South_Africa', 'South_Korea', 'Spain', 'Sri_Lanka', 'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Trinidad_And_Tobago', 'Turkey', 'Ukraine', 'United_Arab_Emirates', 'United_Kingdom', 'United_States', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam'])
        self.country_combo.currentTextChanged.connect(self.update_city_list)
        self.layout.addWidget(QLabel("Select Country:"))
        self.layout.addWidget(self.country_combo)

        # City Selection
        self.city_combo = QComboBox(self)
        self.city_combo.addItems(['Auto'])
        self.layout.addWidget(QLabel("Select City:"))
        self.layout.addWidget(self.city_combo)

        # Connect Button
        self.connect_button = QPushButton('Connect', self)
        self.connect_button.setObjectName('connect_button')
        self.connect_button.clicked.connect(self.connect_vpn)
        self.layout.addWidget(self.connect_button)

        # Disconnect Button
        self.disconnect_button = QPushButton('Disconnect', self)
        self.disconnect_button.setObjectName('disconnect_button')
        self.disconnect_button.clicked.connect(self.disconnect_vpn)
        self.layout.addWidget(self.disconnect_button)

        # Check VPN status on startup
        self.check_vpn_status()

    def check_vpn_status(self):
        try:
            result = subprocess.run("nordvpn status", shell=True, text=True, capture_output=True)
            if "Connected" in result.stdout:
                self.status_label.setText("Status: Connected")
                self.server_info_label.setText(self.extract_info(result.stdout, "Server:"))
                self.country_info_label.setText(self.extract_info(result.stdout, "Country:"))
            else:
                self.status_label.setText("Status: Disconnected")
        except subprocess.CalledProcessError:
            self.status_label.setText("Failed to check status")

    def extract_info(self, output, keyword):
        lines = output.strip().split('\n')
        return next((line for line in lines if keyword in line), f"{keyword} Not available")

    def update_server_list(self):
        self.city_combo.clear()
        self.city_combo.addItem('Auto')

    def update_city_list(self):
        country = self.country_combo.currentText()
        if country != 'Select Country':
            try:
                result = subprocess.run(f"nordvpn cities {country}", shell=True, text=True, capture_output=True)
                cities = result.stdout.strip().split()
                self.city_combo.clear()
                self.city_combo.addItem('Auto')
                for city in cities:
                    if city.strip():  # Skip empty lines
                        self.city_combo.addItem(city.strip())
            except subprocess.CalledProcessError:
                self.city_combo.clear()
                self.city_combo.addItem('Error fetching cities')

    def connect_vpn(self):
        self.connect_button.setText('Connecting...')
        self.connect_button.setDisabled(True)
        server_type = self.server_type_combo.currentText()
        country = self.country_combo.currentText()
        city = self.city_combo.currentText()

        # Jeśli wybrano kraj i miasto jest ustawione na 'Auto', użyj nordvpn c <country>
        if country != 'Select Country' and city == 'Auto':
            command = f"nordvpn c {country}"
        elif server_type == 'Auto' and city != 'Auto':
            command = f"nordvpn connect {city}"
        elif server_type == 'Auto':
            command = "nordvpn connect"
        elif city != 'Auto':
            command = f"nordvpn c {country} {city}"
        elif server_type != 'Auto':
            command = f"nordvpn c {server_type}"

        try:
            subprocess.run(command, shell=True, check=True)
            self.status_label.setText(f"Status: Connected to {server_type} {country} {city}")
            self.update_vpn_info()
        except subprocess.CalledProcessError:
            self.status_label.setText("Failed to connect")
        finally:
            self.connect_button.setText('Connect')
            self.connect_button.setEnabled(True)

    def disconnect_vpn(self):
        self.connect_button.setText('Connecting...')
        self.connect_button.setDisabled(True)
        try:
            subprocess.run("nordvpn disconnect", shell=True, check=True)
            self.status_label.setText("Status: Disconnected")
            self.server_info_label.setText("")
            self.country_info_label.setText("")
        except subprocess.CalledProcessError:
            self.status_label.setText("Failed to disconnect")
            self.server_info_label.setText("")
            self.country_info_label.setText("")
        finally:
            self.connect_button.setText('Connect')
            self.connect_button.setEnabled(True)

    def update_vpn_info(self):
        try:
            result = subprocess.run("nordvpn status", shell=True, text=True, capture_output=True)
            self.server_info_label.setText(self.extract_info(result.stdout, "Server:"))
            self.country_info_label.setText(self.extract_info(result.stdout, "Country:"))
        except subprocess.CalledProcessError:
            self.server_info_label.setText("")
            self.country_info_label.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NordVPNGui()
    window.show()
    sys.exit(app.exec_())
