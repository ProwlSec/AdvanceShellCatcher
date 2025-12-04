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


## ❓ FAQ

### 🔹 Can PROWLER be used in OSCP and other OffSec exams?
**Yes.**  
PROWLER does not perform exploitation, automation, brute forcing, enumeration, or any prohibited actions.  
It functions purely as a **reverse shell listener**, similar to `nc -lvnp` or Metasploit’s `multi/handler`, and is therefore compliant with OffSec exam rules.

---

### 🔹 Does PROWLER exploit targets automatically?
No.  
PROWLER only **accepts incoming reverse shell connections**.  
It never sends exploit code, payloads, or initiates an attack on any host.

---

### 🔹 Is PROWLER allowed on other certifications like PNPT, eJPT, eCPPT, CRTO, etc.?
Yes.  
Since PROWLER only handles shells and does not automate exploitation, it is allowed in all major hands-on exams.

---

### 🔹 Does PROWLER work on Windows shells?
Partially.  
It works if the payload provides a Windows-compatible reverse shell (e.g., certain versions of Netcat).  
Python PTY shells are Unix-only.

---

### 🔹 How many sessions can PROWLER handle?
Up to **10 simultaneous sessions** by default.  
You can modify this limit in the source if needed.

---

### 🔹 Does PROWLER support TTY/PTY upgrades?
Yes.  
The Python payload module automatically spawns a PTY-enabled Bash shell for full TTY control.

---

### 🔹 Does PROWLER require administrative privileges?
No.  
It only needs permission to bind to the chosen port (above 1024 unless run as root).

---

### 🔹 What platforms are supported?
- Linux  
- macOS  
- Unix-like systems  
Reverse shell sources can be anything (Linux, macOS, Windows) as long as they provide a valid TCP shell.

---

### 🔹 Can PROWLER be used for team collaboration or multi-host operations?
Yes.  
PROWLER supports multiple incoming shells simultaneously, making it useful for red teaming or multi-host labs.

---

### 🔹 Is PROWLER safe for production or internal network labs?
Yes.  
It acts as a passive listener and does not perform any intrusive operations on its own.

---


## 🔚 Closing Note

Thank you for checking out **PROWLER** — a project built with a focus on stability, clarity, and real-world usefulness for pentesters, students, and red‑teamers.  
Whether you're practicing in a home lab, working through certifications like **OSCP**, or performing authorized assessments, I hope PROWLER becomes a reliable part of your toolkit.

If you have **feature suggestions, bug reports, optimization ideas, or general feedback**, they are always welcome.  
Feel free to open an **Issue** or submit a **Pull Request** — contributions from the community help the project grow and improve.

Stay sharp, stay ethical, and keep prowling safely. 🐾  
**— ProwlSec**
