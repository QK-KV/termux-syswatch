## Termux SysWatch

**Termux SysWatch** is a lightweight and visually enhanced system monitoring tool built specifically for Termux. It displays real-time usage of your device's **CPU**, **memory**, and **network I/O** using a beautiful terminal interface powered by the [Rich](https://github.com/Textualize/rich) Python library.

### Features
- Live updates every 0.5 seconds
- Displays:
  - CPU usage
  - Memory usage (used / total)
  - Network data (sent / received)
- Clean, colorful terminal interface
- Optimized for low-resource environments like Termux

### Installation

```bash
git clone https://github.com/T6ARB/termux-syswatch.git
```
```bash
cd termux-syswatch
```
```bash
pkg install python -y
```
```bash
pip install -r requirements.txt
```
Usage
```bash
python monitor.py
