# Gesture Controlled Presentation System

A computer vision based system that allows users to control presentation slides using hand gestures through a webcam.

This project uses **MediaPipe hand tracking** and **OpenCV** to detect hand gestures and control slides in presentation software such as **Microsoft PowerPoint** and **Google Slides**.

---

## Features

* Control presentation slides using hand gestures
* Next slide gesture
* Previous slide gesture
* Laser pointer using index finger
* Lock / Unlock gesture control
* Real-time hand tracking
* Works with PowerPoint, Google Slides, and other presentation tools

---

## Technologies Used

* Python
* MediaPipe
* OpenCV
* PyAutoGUI
* NumPy

---

## Installation

1. Clone the repository

git clone https://github.com/anuradhayadagiri/gesture-presentation-controller.git

2. Navigate to the project folder

cd gesture-presentation-controller

3. Install required libraries

pip install -r requirements.txt

4. Run the program

python gesture_controller.py

---

## Gestures

Gesture       Action                

Open Palm     Unlock gestures            
Two Fingers   Next  Slide 
Four fingers  previous slide     
Index Finger  Laser Pointer         
Fist          Lock / Unlock Control 

---

## How It Works

The system captures video from the webcam using OpenCV.
MediaPipe detects hand landmarks and identifies finger positions.
Based on these positions, gestures are recognized and converted into keyboard commands using PyAutoGUI to control presentation slides.

---


## Author

Anuradha

---

