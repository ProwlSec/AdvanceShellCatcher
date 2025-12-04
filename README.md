# 🐾 PROWLER — ProwlSec Multi-Session Shell Catcher
### Advanced Reverse Shell Handler for Pentesters & Red Teams  
**Author:** ProwlSec  
**Program:** PROWLER.py  

PROWLER is a powerful, multi-session reverse shell catcher designed for real-world offensive security workflows.  
It supports **multiple shells**, **rich-based UI**, **dynamic payload generation**, and **interactive TTY mode**, all running on a fast, thread-safe Python backend.

---

## 📥 Install

PROWLER runs on Linux, macOS, and other Unix-like platforms.  
Requires **Python 3.8+**.

### 🔹 Download & Run (no install needed)

```bash
wget https://raw.githubusercontent.com/ProwlSec/PROWLER/main/PROWLER.py \
  && python3 PROWLER.py
```

Install using pipx (recommended)
```bash
pipx install git+https://github.com/ProwlSec/PROWLER
```

Install the requirements
```bash
pip install rich
```
## 🚀 Features

### 🟣 Core Capabilities
- Multi-session reverse shell handling  
- Real-time interactive TTY shell control  
- Rich-powered UI with tables, prompts, and color formatting  
- Thread-safe TCP listener with stable session management  
- Automatic session indexing and connection tracking  
- Background/foreground shell switching  
- Built-in payload generator for Bash, Python, and Netcat shells  
- Clean and intuitive command-line interface (CLI)  

---

## 🟣 Session Features

| Description | Unix | Windows |
|------------|-------|---------|
| Multi-session support | ✔ | ✔ |
| Interactive shell (TTY/PTY) | PTY | readline |
| Background sessions | ✔ | ✔ |
| Rich-formatted shell output | ✔ | ✔ |
| Detect lost/disconnected clients | ✔ | ✔ |
| Session kill control | ✔ | ✔ |
| Stable threaded listener | ✔ | ✔ |

---

## 🟣 Payload Modules

| Payload | Description | Platform |
|--------|-------------|----------|
| `reverse_tcp/bash` | Classic Bash reverse shell | Unix |
| `reverse_tcp/python` | Python3 PTY spawn TTY shell | Unix |
| `reverse_tcp/netcat` | Netcat `-e` shell | Unix / Windows* |

\* Windows support depends on netcat variant.

---

## 🟣 Usability Features
- Color-coded prompts and panels  
- Intelligent error handling  
- Modular option system (LHOST, LPORT, PAYLOAD)  
- Instant payload command preview  
- Supports up to 10 simultaneous connections by default  
- Graceful shutdown of listener and sessions

## Starting the tool with python
<img width="1524" height="379" alt="image" src="https://github.com/user-attachments/assets/8e472fd2-e858-445b-9ff7-159e8264edc3" />

## Setting the LPORT and LHOST
```bash
set LHOST <your ip>
set LPORT <listening port>
```
<img width="1082" height="169" alt="image" src="https://github.com/user-attachments/assets/c34e84b0-3962-441a-88e0-2bc2fae071ea" />

