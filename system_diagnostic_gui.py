import tkinter as tk
from tkinter import ttk
import psutil
import subprocess
import platform
import time
import threading

# Function to check network connectivity
def check_network():
    try:
        subprocess.check_output(["ping", "-n", "1", "google.com"])
        return "Connected"
    except:
        return "Disconnected"

# Function to update system stats
def update_stats():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net_status = check_network()

        cpu_label.config(text=f"CPU Usage: {cpu_percent}%")
        ram_label.config(text=f"RAM Usage: {ram.percent}% ({round(ram.used / (1024 ** 3), 2)} GB / {round(ram.total / (1024 ** 3), 2)} GB)")
        disk_label.config(text=f"Disk Usage: {disk.percent}% ({round(disk.used / (1024 ** 3), 2)} GB / {round(disk.total / (1024 ** 3), 2)} GB)")
        net_label.config(text=f"Network: {net_status}")

        # Color indicator for network status
        if net_status == "Connected":
            net_label.config(fg="green")
        else:
            net_label.config(fg="red")

        time.sleep(3)  # refresh every 3 seconds

# Create the main window
root = tk.Tk()
root.title("System Diagnostic Dashboard")
root.geometry("500x300")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

# Title
title_label = tk.Label(root, text="🧠 System Diagnostic Dashboard", font=("Segoe UI", 16, "bold"), bg="#1e1e1e", fg="#00ffff")
title_label.pack(pady=10)

# Info Frame
info_frame = ttk.Frame(root)
info_frame.pack(pady=10)

cpu_label = tk.Label(info_frame, text="CPU Usage: ", font=("Segoe UI", 12), bg="#1e1e1e", fg="white")
cpu_label.pack(pady=5)

ram_label = tk.Label(info_frame, text="RAM Usage: ", font=("Segoe UI", 12), bg="#1e1e1e", fg="white")
ram_label.pack(pady=5)

disk_label = tk.Label(info_frame, text="Disk Usage: ", font=("Segoe UI", 12), bg="#1e1e1e", fg="white")
disk_label.pack(pady=5)

net_label = tk.Label(info_frame, text="Network: ", font=("Segoe UI", 12), bg="#1e1e1e", fg="white")
net_label.pack(pady=5)

# Start the background thread for updating stats
thread = threading.Thread(target=update_stats, daemon=True)
thread.start()

# Run the app
root.mainloop()
