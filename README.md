# SecureCam - Human Detection and Recording System

## Overview
**SecureCam** is a Python-based application designed to monitor a live camera feed for human presence using OpenCV's face detection. It provides advanced features such as recording videos when a face is detected, real-time FPS display, and user interaction through a GUI built with PyQt5. The app is suitable for use in personal or small-scale security monitoring systems.

## Features
- **Real-time Face Detection**: Detects human faces within a predefined box.
- **Auto Recording**: Starts recording when a face is detected within the box and stops after a specified duration or if no face is detected for a given time.
- **Video Overlay**: Displays FPS and timestamp on the video feed.
- **GUI Controls**:
  - View recordings.
  - Stop recording.
  - View logs.
  - Stop alert.
- **Logs System**: Tracks and displays system activities.
- **Text-to-Speech Integration**: Announces recording start and stop events.

## Requirements
The following libraries and tools are required to run SecureCam:

- Python 3.8 or later
- OpenCV (`cv2`)
- PyQt5
- pyttsx3

2. Use the GUI to monitor the camera feed and control the recording system.

### GUI Components
- **Camera Feed**: Displays the live video feed with detection overlays.
- **Info Panel**: Displays current date, time, and last detection information.
- **Logs Panel**: Displays a log of system events.
- **Control Buttons**:
  - **View Recordings**: Placeholder for viewing recorded videos.
  - **Delete Recordings**: Placeholder for deleting recordings.
  - **View Logs**: Displays the system log.
  - **Stop Recording**: Stops the current recording manually.
  - **Stop Alert**: Placeholder for stopping alerts.

### Recording Behavior
- Recording starts when a face is detected inside the predefined green box.
- Stops if no face is detected for 20 seconds or when the maximum recording duration (10 minutes) is reached.


## Key Functions
### `is_face_in_box(x, y, w, h, box_x, box_y, box_size)`
Checks if a detected face lies within the predefined green box.

### `start_recording(frame, date_time)`
Starts recording a video with a unique filename based on the current timestamp.

### `stop_recording()`
Stops the video recording and releases the video writer object.

### `display_overlay(frame, fps)`
Adds an overlay to the video feed showing the current timestamp and FPS.

## Customization
- **Detection Box**: The detection box can be adjusted by modifying `box_x`, `box_y`, and `box_size`.
- **Recording Duration**: Modify `max_recording_duration` to change the maximum recording time.
- **Alert Messages**: Customize the text-to-speech messages in `start_recording()` and `stop_recording()`.


## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements
- OpenCV for computer vision tools.
- PyQt5 for GUI development.
- pyttsx3 for text-to-speech functionality.

