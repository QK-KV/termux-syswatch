import psutil
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def create_table():
    table = Table(title="System Monitor", style="bold cyan")
    table.add_column("Component", justify="right", style="bold yellow")
    table.add_column("Usage", justify="left", style="bold green")

    # CPU
    cpu_percent = psutil.cpu_percent()
    table.add_row("CPU Usage", f"{cpu_percent}%")

    # Memory
    mem = psutil.virtual_memory()
    mem_used = get_size(mem.used)
    mem_total = get_size(mem.total)
    table.add_row("Memory Usage", f"{mem_used} / {mem_total} ({mem.percent}%)")

    # Network
    net = psutil.net_io_counters()
    table.add_row("Bytes Received", get_size(net.bytes_recv))
    table.add_row("Bytes Sent", get_size(net.bytes_sent))

    return table

with Live(console=console, refresh_per_second=2):  # Updates every 0.5 seconds
    while True:
        table = create_table()
        console.clear()
        console.print(table)
        time.sleep(0.5)
