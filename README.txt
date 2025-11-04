# Hotspot Manager for Parrot OS
A beautiful graphical interface for managing WiFi hotspots with real-time device monitoring.

## 📦 Installation

### Method 1: Install from .deb package (Recommended)
1. Open terminal in the folder containing `hotspot-manager-package.deb`
2. Run: `sudo dpkg -i hotspot-manager-package.deb`
3. If you get dependency errors, run: `sudo apt-get install -f`

### Method 2: Build from source
1. Ensure you have the complete `hotspot-manager` folder
2. Open terminal in the `hotspot-manager` directory
3. Run: `./build-package.sh` to build the .deb package
4. Then install using Method 1 above
NOTE: BEFORE BUILDING TAKE NOTE THAT IN THE CODES THERE ARE MY ADAPTERS ["INTERNET_ADAPTER": "wlo1", 
"HOTSPOT_ADAPTER": "wlx20235199be72"]
SO CHANGE TO YOUR OWN ADAPTERS

## 🚀 Usage

### Launching the Application
- **GUI Method**: Look for "Hotspot Manager" in your application menu under "Network"
- **Terminal Method**: Run `hotspot-manager` from any terminal

### Using the Hotspot
1. Click the circular button to start/stop the hotspot
   - 🔵 Blue = Stopped (shows "START")
   - 🔴 Red = Running (shows "STOP")
2. View connected devices in the table below
3. Use "Advanced" button to change SSID and password

## ⚙️ Configuration

### Default Settings
- SSID: `ParrotHotspot`
- Password: `Parrot123`
- Internet Adapter: `wlo1`
- Hotspot Adapter: `wlx20235199be72`

### Customizing Settings
1. Click the "Advanced ⚙️" button in the app
2. Enter new SSID and password (minimum 8 characters)
3. Authenticate with your password to save changes
4. Restart the hotspot for changes to take effect

### Manual Configuration
Edit the config file: `/etc/hotspot-manager/config.conf`
```bash
sudo nano /etc/hotspot-manager/config.conf

### NOTE: THIS APPLICATION WORKS IF YOU HAVE TWO ADAPTERS WHERE ONE ACTS AS THE HOTSPOT AND THE OTHER ACTS AS THE OTHER WIFI RECEIVER  FOR EXAMPLE I USED INTEL NETWORK ADAPTER FOR HOTSPOTTING AND A REALTEK ADAPTER FOR RECEIVING A WIFI NETWORK I WANTED TO HOTSPOT
