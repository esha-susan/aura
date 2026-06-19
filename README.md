# AURA (Are U Really Attentive?)

**Real-time attention & drowsiness monitor — powered by your webcam.**

AURA watches your face through your webcam and scores how attentive you are, frame by frame. It tracks head position, eye openness, and face presence using [MediaPipe](https://google.github.io/mediapipe/) Face Mesh, then combines them into a live **Attention %** score. If your eyes stay closed too long, it sounds an alarm — built for catching drowsiness during study sessions, long work hours, or anywhere you need to stay alert.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-FaceMesh-00897B?style=flat&logo=google&logoColor=white)
![Status](https://img.shields.io/badge/status-active%20development-yellow)

---

## How it works

AURA computes attention as a weighted score from three signals, captured live from your webcam feed:

| Signal | What it measures | Weight |
|---|---|---|
| **Head presence** | Is your face properly framed and at a reasonable distance from the camera? | 40% |
| **Eye openness** | Eye Aspect Ratio (EAR) — are your eyes open or closed? | 30% |
| **Head orientation** | Are you facing the screen, or looking away? | 30% |

These combine into a single **Attention Score (0–100%)**, displayed live on screen alongside head status (`Attentive` / `Distracted`) and eye state.

If your eyes are detected as closed for **5+ continuous seconds**, AURA treats this as a drowsiness event and plays an audible alarm to wake you up.

> **Note:** A gaze-direction module (`gaze.py`) is included but currently disabled — it estimates left/right/center gaze using iris landmarks and is planned for future integration into the attention score.

---

## Demo

Run it and a window titled **AURA** will pop up showing your webcam feed with:
- Green face mesh overlay
- Head status (`Attentive` in green / `Distracted` in red)
- Live attention percentage
- A drowsiness alert + alarm sound if eyes stay closed too long

Press **`Esc`** at any time to quit.

---

## Tech stack

- **Python 3.9+**
- **OpenCV** — webcam capture & rendering
- **MediaPipe Face Mesh** — 468-point facial landmark detection (with iris refinement)
- **NumPy** — vector math for the Eye Aspect Ratio (EAR) calculation
- **playsound** — alarm audio playback

---

## Setup

### Prerequisites
- Python 3.9 or higher
- A working webcam
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/esha-susan/aura.git
cd aura

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Run

```bash
python run.py
```

Grant webcam permission if prompted by your OS. The AURA window should open within a few seconds.

---

## Project structure

```
aura/
├── run.py            # Entry point — webcam capture loop & main display
├── detector.py       # MediaPipe Face Mesh setup & landmark detection
├── attention.py      # Core logic: head position & Eye Aspect Ratio (EAR) checks
├── utils.py          # Combines signals into attention score, drowsiness alarm logic
├── gaze.py           # Iris-based gaze direction estimation (currently disabled)
├── fifths.wav        # Alarm sound played on drowsiness detection
└── requirements.txt
```

---

## Configuration

A couple of constants in `utils.py` can be tuned to your setup:

```python
EAR_THRESHOLD = 0.23       # Eye Aspect Ratio below this = eyes considered closed
EYES_CLOSED_SECONDS = 5    # Seconds of closed eyes before the alarm triggers
```

Lighting conditions and camera angle can affect EAR readings — if AURA is too sensitive or not sensitive enough, adjust `EAR_THRESHOLD` accordingly.

---

## Roadmap

- [ ] Re-enable and integrate gaze direction into the attention score
- [ ] Session logging (attention trends over time, exportable reports)
- [ ] Configurable alert sounds / visual-only mode
- [ ] Multi-face handling for shared screens

---

## Known limitations

- Single-face detection only (`max_num_faces=1`)
- Accuracy depends on lighting and camera quality
- Tested primarily on [Linux Ubuntu]


---

## Author

Built by [Esha Susan](https://github.com/esha-susan)
