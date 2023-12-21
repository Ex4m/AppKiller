import psutil
import re
import pickle
import os
import sys


def get_executable_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.realpath(__file__))


def find_config_file(script_dir, def_name):
    config_file = os.path.join(script_dir, f"{def_name}.pkl")
    name = def_name
    if not os.path.isfile(config_file):
        name = 'AKconfig.pkl'
        config_file = os.path.join(script_dir, name)
    return config_file, name


def import_config():
    try:
        script_dir = get_executable_path()
        def_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        exe_file = os.path.join(script_dir, f"{def_name}.exe") if hasattr(
            sys, 'frozen') else __file__

        if not os.path.isfile(exe_file):
            print('AppKiller.exe not found.')
            return

        config_file, name = find_config_file(script_dir, def_name)
        print(
            f"Loaded data from file {name} and on path: {script_dir}")

        with open(config_file, 'rb') as file:
            config_data = pickle.load(file)

        for section_data in config_data:
            section_number = section_data.get('section_number')
            exe_to_kill = section_data.get('exe_to_kill', '')
            app_path = section_data.get('app_path', '')

        return config_data

    except Exception as error:
        print(f"There was some kind of import error - {error}")
        return None


# Přesunutí definice def_name před volání funkce import_config
def_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
config_data = import_config()


def app_killer_from_config(config_data):
    if config_data is None:
        return

    terminated_count = 0

    for section_data in config_data:
        numbering = section_data['section_number']
        exe_to_kill = section_data['exe_to_kill']
        path_contains = section_data['app_path']

        print(section_data)

        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                # Kontrola, zda je klíčové slovo obsaženo v názvu procesu, v cestě k exe souboru nebo v argumentech
                if exe_to_kill in proc.info['name'].lower():
                    if path_contains in proc.info['exe'].lower() or any(path_contains in arg.lower() for arg in proc.info['cmdline']):
                        print(
                            f"Terminating process {proc.info['name']} (PID: {proc.info['pid']})")
                    psutil.Process(proc.info['pid']).terminate()
                    terminated_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Skip any errors when retrieving process information
                pass

    print(f"Terminated {terminated_count} processes.")


app_killer_from_config(config_data)
