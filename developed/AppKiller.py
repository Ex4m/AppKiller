import psutil
import re
import pickle
import os


import os
import pickle


def find_config_file(script_dir, def_name):
    config_file = os.path.join(script_dir, f"{def_name}.pkl")
    if not os.path.isfile(config_file):
        config_file = os.path.join(script_dir, 'AKconfig.pkl')
    return config_file


def import_config():
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        exe_file = os.path.join(script_dir, 'AppKiller.exe')

        if not os.path.isfile(exe_file):
            print('AppKiller.exe not found.')
            return

        def_name = os.path.splitext(os.path.basename(exe_file))[0]
        config_file = find_config_file(script_dir, def_name)

        with open(config_file, 'rb') as file:
            config_data = pickle.load(file)

        for section_data in config_data:
            section_number = section_data.get('section_number')
            exe_to_kill = section_data.get('exe_to_kill', '')
            app_path = section_data.get('app_path', '')

            # Provádějte akce podle načtených dat, např.:
            print(
                f"Section '{section_number}'\n Exe to kill: '{exe_to_kill}'\n App path: '{app_path}'\n\n")

        print(f'Configuration imported successfully from: {config_file}')

    except Exception as error:
        print(f"There was some kind of import error - {error}")


# Použití funkce pro import
config_data = import_config()


def app_killer_from_config(config_data):
    terminated_count = 0

    for section_data in config_data:
        exe_to_kill = section_data.get('exe_to_kill', '')
        path_contains = section_data.get('app_path', '')

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


app_killer_from_config(config_data)
