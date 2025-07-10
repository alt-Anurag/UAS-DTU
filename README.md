# 🎯 Payload Release Point Calculator – UAS-DTU

A physics-based simulator that helps UAVs determine the optimal release point for payload delivery. The program ensures that the payload lands within a 10-meter radius of the target location by simulating realistic trajectories with and without air drag, using accurate geolocation and physics models.

---

## 📌 Task Objective

Design a program for a UAV to:

- Estimate its current position
- Decide the exact release point of the payload
- Simulate trajectory with air drag
- Ensure the payload reaches the desired drop location accurately

---

## 🛠 How to Use

1. **Edit Input Files:**

   - Modify `start.txt` with:
     - Launch coordinates (lat/lon in DMS format)
     - Initial x and y velocities (e.g., `velX_20 velY_10`)
   - Modify `end.txt` with:
     - Target coordinates (lat/lon in DMS format)

   ⚠️ **Do not change the format or spacing** in these files.

2. **Run the Program:**

   - Run the Python script:  
     ```bash
     python your_script_name.py
     ```
   - OR run the compiled `.exe` file if available

3. **Follow On-Screen Instructions:**

   - The program simulates trajectory
   - Calculates the distance and release point
   - Optionally plots the trajectory (with/without air drag)

---

## 📐 Physics & Calculations

- Haversine formula to calculate Earth distance
- Models air drag using:
  - Drag coefficient: 0.47
  - Air density: 1.225 kg/m³
  - Radius: 0.1 m
- Gravity (g): 9.81 m/s²
- Wind speed: 3 m/s
- Uses Euler integration with a time step of 0.01s

---

## 📊 Output

- Start and target coordinates
- Distance to the target
- Recommended horizontal release point (in km)
- Optional Matplotlib plot of trajectory:
  - With air drag
  - Without air drag

---

## 🔧 Dependencies

- Python 3.x
- NumPy
- Matplotlib

Install via:

```bash
pip install numpy matplotlib
```

---

## 👨‍💻 Author

- [Anurag Kumar Jha](https://github.com/alt-Anurag)

---

