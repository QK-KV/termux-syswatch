import psutil
import time
import subprocess
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn, ProgressColumn
from rich.text import Text
from datetime import datetime

console = Console()

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_cpu_percent():
    try:
        output = subprocess.check_output(["top", "-n", "1", "-b"], universal_newlines=True)
        for line in output.splitlines():
            if "CPU" in line or "cpu" in line:
                parts = line.split(",")
                for part in parts:
                    if "id" in part:
                        idle_str = part.strip().split("%")[0]
                        idle = float(idle_str)
                        usage = 100 - idle
                        return usage
        return 0.0
    except Exception:
        return 0.0

def get_network_usage():
    try:
        with open("/proc/net/dev", "r") as f:
            data = f.readlines()
        bytes_recv = 0
        bytes_sent = 0
        for line in data[2:]:
            parts = line.split()
            if len(parts) < 17:
                continue
            bytes_recv += int(parts[1])
            bytes_sent += int(parts[9])
        return bytes_recv, bytes_sent
    except Exception:
        return None, None

def colorize_percent(value):
    if value < 50:
        return "green"
    elif value < 75:
        return "yellow"
    else:
        return "red"

def create_progress_bar(percentage):
    bar_length = 30
    filled_length = int(bar_length * percentage // 100)
    empty_length = bar_length - filled_length
    bar = ("█" * filled_length) + ("─" * empty_length)
    color = colorize_percent(percentage)
    return f"[{color}]{bar}[/{color}]"

def create_table():
    table = Table(title="System Monitor", style="bold cyan", expand=True, border_style="bright_blue")

    table.add_column("Component", justify="right", style="bold yellow")
    table.add_column("Usage", justify="left", style="bold green")

    # CPU
    cpu_percent = get_cpu_percent()
    cpu_bar = create_progress_bar(cpu_percent)
    cpu_text = f"{cpu_bar} {cpu_percent:.1f}%"
    table.add_row("CPU Usage", cpu_text)

    # Memory
    mem = psutil.virtual_memory()
    mem_used = get_size(mem.used)
    mem_total = get_size(mem.total)
    mem_percent = mem.percent
    mem_bar = create_progress_bar(mem_percent)
    mem_text = f"{mem_used} / {mem_total} ({mem_percent}%) {mem_bar}"
    table.add_row("Memory Usage", mem_text)

    # Network
    bytes_recv, bytes_sent = get_network_usage()
    if bytes_recv is not None and bytes_sent is not None:
        table.add_row("Bytes Received", get_size(bytes_recv))
        table.add_row("Bytes Sent", get_size(bytes_sent))
    else:
        table.add_row("Bytes Received", "Permission denied")
        table.add_row("Bytes Sent", "Permission denied")

    # Current Time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    table.add_row("Timestamp", now)

    return table

with Live(console=console, refresh_per_second=2):
    while True:
        table = create_table()
        console.clear()
        console.print(table)
        time.sleep(0.5)
