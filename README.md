Monitor-Manager

Monitor-Manager is a Python script that allows you to easily manage display settings on Linux using xrandr. It supports listing active displays, setting custom resolutions, extending displays, and automating resolution changes across sessions.
Features

    . List Active Displays: Displays connected and disconnected monitors along with their resolution and status.
    
    . Set Custom Resolution: Set custom resolution for any connected monitor by providing X and Y axis dimensions.
    
    . Auto Adjust Resolution: Automatically adjust the resolution of active monitors.
    
    . Extend Displays: Easily set up dual monitors and adjust positioning (left, right, above, below).
    
    . Persistent Settings: Configuration is saved across reboots using LightDM.

Requirements

    . Python 3.x
    . xrandr (pre-installed on most Linux distributions)
    . Linux environment using LightDM display manager

Installation

    Clone the repository:

    git clone https://github.com/yourusername/Monitor-Manager.git
    cd Monitor-Manager

    Note: The subprocess module is built into Python and requires no installation.

Usage

    Run the script:


    sudo python3 monitor_manager.py

    The script provides a menu with the following options:
    
        1. Show Monitors List: Displays all connected and disconnected monitors.
        
        2. Set Resolution: Allows you to manually set the resolution for a selected display.
        
        3. Automatically Set Resolution: Automatically adjusts resolution for all active monitors.
        
        4. Set Extended Monitors: Configures extended displays with custom positioning.

Example

    
    $ sudo python3 monitor_manager.py
    
    1. Show Monitors List
    2. Set Resolution
    3. Automatically Set Resolution
    4. Set Extended Monitors
    
    Enter your choice: 1

    [Display Name, Status, Resolution]
    [HDMI-1, connected, 1920x1080]
    [eDP-1, disconnected]

    $ sudo python3 monitor_manager.py
    
    Enter your choice: 2
    
    Display Name: HDMI-1
    X-axis(Horizontal): 1366
    Y-axis(Vertical): 768
    You have successfully set a new resolution: 1366x768

Configuration and Persistence

    The script creates a configuration file (/etc/lightdm/my_conf.sh) to store the xrandr commands required to set resolutions across sessions.
    Updates are made to the LightDM configuration file (/etc/lightdm/lightdm.conf) to ensure the script runs on startup.
    The autostart configuration is updated if needed (/root/.config/autostart/lxrandr-autostart.desktop).

Troubleshooting

    Permission Denied Errors: Make sure you are running the script with sudo as it modifies system files.
    Display Not Found: Ensure that the display name entered matches the output from the "Show Monitors List" option.
    Resolution Setting Errors: Check whether the desired resolution is supported by your monitor.
    Autostart File Not Found: The script checks for an existing autostart file; if not found, you may need to manually create it.
