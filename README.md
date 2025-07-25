✋🧠 Gesture-Based Math Solver using OpenCV and MediaPipe

This project is a **real-time hand gesture-based calculator** that lets users input and evaluate mathematical expressions using only hand gestures. Designed for accessibility and computer vision learning, it translates hand signs into digits, operators, and commands.

---

 🚀 Features

* 📷 Real-time gesture detection using webcam
* 🔢 Multi-digit input support (e.g., 2 → 4 → 7 becomes "247")
* ➕ Gesture-controlled operations (`+`, `-`, `*`, `/`)
* ✅ Built-in expression evaluation (`=`)
* 🧹 Gesture-based `Clear`, `Delete`, and `Exit` commands
* 🖐️ Runs on a standard webcam (no extra hardware needed)

---

🧠 Tech Stack

| Tool          | Purpose                              |
| ------------- | ------------------------------------ |
| **Python**    | Core programming language            |
| **OpenCV**    | Webcam access & display rendering    |
| **MediaPipe** | Hand landmark detection (21 points)  |
| **NumPy**     | Math processing, vector calculations |

---

 ✋ Supported Gestures

| Gesture                            | Function       |
| ---------------------------------- | -------------- |
| 1–5 fingers (one hand)             | Digits 1–5     |
| 5 + 1–4 fingers (both hands)       | Digits 6–9     |
| 0 fingers (one hand)               | Digit 0        |
| 1 finger (each hand)               | `+` (add)      |
| 1 + 2 fingers (left + right)       | `-` (subtract) |
| 1 + 3 fingers                      | `*` (multiply) |
| 1 + 4 fingers                      | `/` (divide)   |
| Both hands 0 fingers               | `=` (evaluate) |
| Both hands 5 fingers               | `Clear` input  |
| Both hands 2 fingers               | `Delete` input |
| Right index < Left index (spatial) | Exit program   |

---

📦 Installation

 🔧 Clone and Set Up

```bash
git clone https://github.com/yourusername/mathSolver.git
cd mathSolver
python -m venv venv
.\venv\Scripts\activate  # for Windows
pip install -r requirements.txt
```

---

 ▶️ Running the Project

Make sure your webcam is working. Then simply run:

```bash
python mathsvoice.py
```

---

💡 Notes

* Ensure good lighting for accurate gesture detection.
* Keep your hands in the camera frame steadily for best results.
* If `cv2` or `mediapipe` errors occur, recheck the `requirements.txt` installation.

---

 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---


