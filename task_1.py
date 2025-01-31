import math as m
import numpy as n
import matplotlib.pyplot as plt
import time as t

# Loading simulator function
def loading_simulator(duration=2, message="Loading"):
    print(message, end="", flush=True)  
    for _ in range(3):  
        t.sleep(0.5)  
        print(".", end="", flush=True)
    t.sleep(duration - 1.5)  
    print("\n")  
    
# Program description
print("\n" + "=" * 100)
print("🚀 Payload Release Point Calculator 🚀".center(70))
print("=" * 100)
print(
    "Welcome! This program helps you calculate the perfect release point for your payload\n"
    "so it lands within a 10-meter radius of the target. Think of it as your personal\n"
    "payload GPS! The start point is set at x = 0, and distances are calculated using the\n"
    "haversine formula (fancy math for Earth distances!). All distances are in kilometers."
)
print("\nHere are the constants I've used for the calculations:")
print("- Mass of the payload: 1.5 kg")
print("- Drag coefficient: 0.47 (i googled it!)")
print("- Air density: 1.225 kg/m³ (standard sea-level air)")
print("- Radius of the payload: 0.1 m (compact)")
print("- Acceleration due to gravity(g): 9.81 m/s² (what goes up must come down!)")
print("- Wind speed: 3 m/s")
print("- Time step: 0.01 s (tiny steps for precise calculations)")
print("- Max simulation time: 100 s (we won't wait forever!)")
print("=" * 100)
input("[Press Enter to Start!]")
print("")

# Reading start.txt
loading_simulator(duration=2, message="Reading input files")
try:
    with open('start.txt', 'r') as start:
        lines = start.readlines()
except FileNotFoundError:
    print("🚨 Error: 'start.txt' file not found. Please make sure it exists!")
    exit()

# Start point data
lat_d = n.array([int(line.split()[0].split('_')[1]) for line in lines])
lat_m = n.array([int(line.split()[1]) for line in lines])
lat_s = n.array([int(line.split()[2]) for line in lines])
lat_dir = n.array([line.split()[3] for line in lines])
latitude = (lat_d + lat_m / 60 + lat_s / 3600) * n.where(lat_dir == 'N', 1, -1)

lon_d = n.array([int(line.split()[4].split('_')[1]) for line in lines])
lon_m = n.array([int(line.split()[5]) for line in lines])
lon_s = n.array([int(line.split()[6]) for line in lines])
lon_dir = n.array([line.split()[7] for line in lines])
longitude = (lon_d + lon_m / 60 + lon_s / 3600) * n.where(lon_dir == 'E', 1, -1)

lst_p = n.column_stack((latitude, longitude)).flatten().tolist()

ivel_x = n.array([float(line.split()[8].split('_')[1]) for line in lines])
ivel_y = n.array([float(line.split()[9].split('_')[1]) for line in lines])

intitail_vel = n.column_stack((ivel_x, ivel_y)).flatten().tolist()

# Reading end.txt
loading_simulator(duration=2, message="Processing drop location data")
try:
    with open('end.txt', 'r') as end:
        lines = end.readlines()
except FileNotFoundError:
    print("🚨 Error: 'end.txt' file not found. Please make sure it exists!")
    exit()

# Drop location data
lat_end_d = n.array([int(line.split()[0].split('_')[1]) for line in lines])
lat_end_m = n.array([int(line.split()[1]) for line in lines])
lat_end_s = n.array([int(line.split()[2]) for line in lines])
lat_end_dir = n.array([line.split()[3] for line in lines])
latitude_end = (lat_end_d + lat_end_m / 60 + lat_end_s / 3600) * n.where(lat_end_dir == 'N', 1, -1)

lon_end_d = n.array([int(line.split()[4].split('_')[1]) for line in lines])
lon_end_m = n.array([int(line.split()[5]) for line in lines])
lon_end_s = n.array([int(line.split()[6]) for line in lines])
lon_end_dir = n.array([line.split()[7] for line in lines])
longitude_end = (lon_end_d + lon_end_m / 60 + lon_end_s / 3600) * n.where(lon_end_dir == 'E', 1, -1)

lst_target = n.column_stack((latitude_end, longitude_end)).flatten().tolist()

loading_simulator(duration=2, message="Calculating distance to target")

# Haversine formula for those earthy distances
def haversine(phi1, lam1, phi2, lam2):
    phi1, lam1, phi2, lam2 = map(m.radians, [phi1, lam1, phi2, lam2])
    delphi = phi2 - phi1
    dellam = lam2 - lam1
    hav = (m.sin(delphi / 2)) ** 2 + m.cos(phi1) * m.cos(phi2) * (m.sin(dellam / 2)) ** 2
    return hav

R = 6371  #km
phi1, lam1 = lst_p[0], lst_p[1]
phi2, lam2 = lst_target[0], lst_target[1]
hav = haversine(phi1, lam1, phi2, lam2)
dist = 2 * R * m.asin(m.sqrt(hav))

# Output start and drop locations
print("-" * 70)
print("📍 Start Point:".ljust(20), f"{lat_d[0]}°{lat_m[0]}'{lat_s[0]}\" {lat_dir[0]}, {lon_d[0]}°{lon_m[0]}'{lon_s[0]}\" {lon_dir[0]}")
print("🎯 Drop Location:".ljust(20), f"{lat_end_d[0]}°{lat_end_m[0]}'{lat_end_s[0]}\" {lat_end_dir[0]}, {lon_end_d[0]}°{lon_end_m[0]}'{lon_end_s[0]}\" {lon_end_dir[0]}")
print("-" * 70)
print(f"📏 Distance to target: {dist:.3f} km")
print(f"💨 Initial velocities (x, y): {intitail_vel[0]} m/s, {intitail_vel[1]} m/s")
print("-" * 70 + "\n")
input("[Press Enter to calculate the release poitn!]" + "\n")

loading_simulator(duration=2, message="Calculating release point and payload trajectory")
print("-" * 70)

# Trajectory calculation functions
def trajectory(vel_x, vel_y, mass, C_d, rho, A, vel_wind):
    dt = 0.01
    g = 9.81
    x, y = [0], [20]
    time = 0
    max_time = 100
    while y[-1] > 0 and time < max_time:
        v_rel = n.sqrt((vel_x + vel_wind) ** 2 + vel_y ** 2)
        F_d = 0.5 * C_d * rho * A * v_rel ** 2
        ax = -F_d * (vel_x + vel_wind) / (mass * v_rel)
        ay = -g - (F_d * vel_y) / (mass * v_rel)
        vel_x += ax * dt
        vel_y += ay * dt
        x.append(x[-1] + vel_x * dt)
        y.append(y[-1] + vel_y * dt)
        time += dt
    return x, y, time

def ideal_trajectory(vel_x, vel_y):
    dt = 0.01
    g = 9.81
    x, y = [0], [20]
    time = 0
    max_time = 100
    while y[-1] > 0 and time < max_time:
        vel_y -= g * dt
        x.append(x[-1] + vel_x * dt)
        y.append(y[-1] + vel_y * dt)
        time += dt
    return x, y, time

# Constants
mass = 1.5
C_d = 0.47
rho = 1.225
radius = 0.1
A = m.pi * radius ** 2
vel_x = intitail_vel[0]
vel_y = intitail_vel[1]
vel_wind = 3

# Calculated trajectories
x1, y1, time1 = ideal_trajectory(vel_x, vel_y)
x2, y2, time2 = trajectory(vel_x, vel_y, mass, C_d, rho, A, vel_wind)

# Calculated release point
drop_rad = float(f"{x2[-1]:.3f}")
release_point = float(f"{dist:.3f}") - drop_rad / 1000 - 0.01
print(f"🎯 Release the payload when x = {release_point:.3f} km")
print("-" * 70)

# Wanna plot?
print("\nDo you want to see the expected trajectory plot of the payload?")
choice = input("[Y/N]: ").strip().upper()

if choice == "Y":
    plt.figure(figsize=(10, 6))
    plt.plot(x1, y1, 'g-', label="Without Air Drag")
    plt.plot(x2, y2, 'r--', label="With Air Drag")
    plt.title("Expected Payload Trajectory with Drag taken in account")
    plt.xlabel("Horizontal Distance (m)")
    plt.ylabel("Vertical Distance (m)")
    plt.grid(True)
    plt.legend()
    plt.show()
elif choice == "N":
    print("\nThanks for using the program! Safe travels! 🚀")
else:
    print("\nInvalid input. Exiting program. 🚨")

# Thanks
print("\n" + "=" * 100)
print("Thank you for using my Payload Release Point Calculator! 🚀".center(70))
print("=" * 100)