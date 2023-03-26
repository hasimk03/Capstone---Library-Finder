# Capstone---Library-Finder
Spring 2023 Capstone Project

Initial Setup:
1. Connect Esp32 camera to your machine (via micro usb cable) 

Red led should turn on indicating the esp32 is powered on

2. Download Arduino IDE (if not already installed)
3. Navigate to File/Arduino IDE -> Preferences/Settings -> Additional Board Managerand insert the following link into the board manager 

https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json


Hit ok and the files should be imported to your IDE
4. Go to Tools -> Board -> Board Manager and search for esp32 (ensure version is 2.0.7+) then install
5. In the drop down menu at the top of the IDE (next to the debug button) select your Arduino Board

Arduino Board should say 'AI Thinker ESP32-CAM' once selected

6. Finally upload the sketch to your board and open a serial monitor (Tools->Serial Monitor)

The newly assigned ip address should be printed in the serial monitor

7. Open to the stream and hit 'start stream' - if no video pops up then hit the RST button on the camera and refresh your page

Note: Once you have started the stream - right click the video pop up and hit copy image address (save this).

Close the tab and navigate to the adress you just saved. When attempting to run the ML models the stream should be started and all ip camera windows should be closed (hard code the copied address into the ML model when attempting to run it)