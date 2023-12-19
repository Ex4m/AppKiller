import psutil
import re
import pickle




def app_killer(exe_to_kill, path_contains):
    terminated_count = 0

    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if exe_to_kill in proc.info['name'] and path_contains in proc.info['exe']:
                print(
                    f"Terminating process {proc.info['name']} (PID: {proc.info['pid']})")
                psutil.Process(proc.info['pid']).terminate()
                terminated_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Skip any errors when retrieving process information
            pass

    print(f"Terminated {terminated_count} processes.")


# Terminate the NiceTaskbar.exe process if its path contains "test"
app_killer("NiceTaskbar.exe", "9am")


