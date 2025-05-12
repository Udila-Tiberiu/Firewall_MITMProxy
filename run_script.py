import subprocess
import time
import os
import sys

# Set paths
MITM_SCRIPT = "mitm_proxy/mitm_script.py"
LOG_SERVER_SCRIPT = "server/server.py"
REACT_APP_DIR = "client"

def run_command(command, cwd=None):
    return subprocess.Popen(command, shell=True, cwd=cwd)

def set_windows_proxy(enable=True):
    if enable:
        # Set proxy to localhost:8080 (default mitmproxy port)
        subprocess.call('netsh winhttp set proxy 127.0.0.1:8080', shell=True)
        subprocess.call('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f', shell=True)
        subprocess.call('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /t REG_SZ /d 127.0.0.1:8080 /f', shell=True)
    else:
        # Disable proxy
        subprocess.call('netsh winhttp reset proxy', shell=True)
        subprocess.call('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f', shell=True)

def main():
    try:
        print("Enabling Windows proxy...")
        set_windows_proxy(True)

        print("Starting mitmproxy...")
        mitm_process = run_command(f"mitmdump -s {MITM_SCRIPT}")

        time.sleep(2)

        print("Starting Flask server...")
        flask_process = run_command(f"{sys.executable} {LOG_SERVER_SCRIPT}")

        time.sleep(2)

        print("Starting React client...")
        react_process = run_command("npm start", cwd=REACT_APP_DIR)

        print("\nAll services started.")
        print("Press Ctrl+C to stop everything.")

        # Wait for any of the processes to exit
        mitm_process.wait()
        flask_process.wait()
        react_process.wait()

    except KeyboardInterrupt:
        print("\nStopping all processes...")

    finally:
        print("Terminating processes...")
        for proc in [mitm_process, flask_process, react_process]:
            if proc and proc.poll() is None:
                proc.terminate()
        print("Disabling Windows proxy...")
        set_windows_proxy(False)

if __name__ == "__main__":
    main()
