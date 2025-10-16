import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import subprocess
import time
import threading
from datetime import datetime

# Check network connectivity
def check_network():
    try:
        subprocess.check_output(["ping", "-n", "1", "google.com"])
        return "Connected"
    except:
        return "Disconnected"

# Save report to a text file
def save_report():
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"System_Report_{now}.txt"

    report = (
        f"System Diagnostic Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"------------------------------------------------------\n"
        f"CPU Usage: {cpu_percent.get()}%\n"
        f"RAM Usage: {ram_percent.get()}% ({round(psutil.virtual_memory().used / (1024 ** 3), 2)} GB used)\n"
        f"Disk Usage: {disk_percent.get()}% ({round(psutil.disk_usage('/').used / (1024 ** 3), 2)} GB used)\n"
        f"Network: {net_status.get()}\n"
    )

    with open(filename, "w") as f:
        f.write(report)

    messagebox.showinfo("Report Saved", f"Report successfully saved as {filename}")

# Update stats every 3 seconds
def update_stats():
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = check_network()

        cpu_percent.set(cpu)
        ram_percent.set(ram.percent)
        disk_percent.set(disk.percent)
        net_status.set(network)

        # Update text labels
        cpu_label.config(text=f"CPU Usage: {cpu}%")
        ram_label.config(text=f"RAM Usage: {ram.percent}%")
        disk_label.config(text=f"Disk Usage: {disk.percent}%")
        net_label.config(text=f"Network: {network}")

        # Update network color
        net_label.config(fg="green" if network == "Connected" else "red")

        # Update progress bars
        cpu_bar['value'] = cpu
        ram_bar['value'] = ram.percent
        disk_bar['value'] = disk.percent

        time.sleep(3)

# --- GUI SETUP ---
root = tk.Tk()
root.title("🧠 System Diagnostic Dashboard")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use('clam')
style.configure("TProgressbar", thickness=20, troughcolor="#333333", background="#00ffff")

# Title
tk.Label(
    root, text="System Diagnostic Dashboard", 
    font=("Segoe UI", 16, "bold"), bg="#1e1e1e", fg="#00ffff"
).pack(pady=10)

# Variables
cpu_percent = tk.DoubleVar()
ram_percent = tk.DoubleVar()
disk_percent = tk.DoubleVar()
net_status = tk.StringVar()

# Frame
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

# CPU
cpu_label = tk.Label(frame, text="CPU Usage:", font=("Segoe UI", 12), bg="#1e1e1e", fg="white")
cpu_label.pack(pady=5)
cpu_bar = ttk.Progressbar(frame, length=400, variable=cpu_percent, maximum=100)
cpu_bar.pack(pady=5)

# RAM
ram_label = tk.Label(frame, text="RAM Usage:", font=("Segoe UI", 12), bg="#1e1e1e", fg="white")
ram_label.pack(pady=5)
ram_bar = ttk.Progressbar(frame, length=400, variable=ram_percent, maximum=100)
ram_bar.pack(pady=5)

# Disk
disk_label = tk.Label(frame, text="Disk Usage:", font=("Segoe UI", 12), bg="#1e1e1e", fg="white")
disk_label.pack(pady=5)
disk_bar = ttk.Progressbar(frame, length=400, variable=disk_percent, maximum=100)
disk_bar.pack(pady=5)

# Network
net_label = tk.Label(frame, text="Network: Checking...", font=("Segoe UI", 12), bg="#1e1e1e", fg="white")
net_label.pack(pady=10)

# Save Report Button
save_btn = ttk.Button(root, text="💾 Save Report", command=save_report)
save_btn.pack(pady=15)

# Start background thread
thread = threading.Thread(target=update_stats, daemon=True)
thread.start()

root.mainloop()
