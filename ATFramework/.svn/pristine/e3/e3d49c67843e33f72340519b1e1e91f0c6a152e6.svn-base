
import wmi
import time
import os
import winreg
import psutil
import pandas as pd


def get_gpu_info():
    """
    Get GPU info
    return a list of dictionary with GPU info
    """
    wmi_client = wmi.WMI(namespace='root\\CIMV2')
    gpu_info_list = [{'gpu_name': gpu.Name, 'driver_version': gpu.DriverVersion, 'gpu_process': gpu.VideoProcessor} for gpu in wmi_client.Win32_VideoController()]
    print(gpu_info_list)
    return gpu_info_list


def add_gpu_z_key_to_registry():
    """
    Add registry key for GPU-Z to prevent the pop-up window for the first time
    return True if success
    """
    registry_path = r"Software\techPowerUp\GPU-Z"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE)
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_path)
    winreg.SetValueEx(key, "Install_Dir", 0, winreg.REG_SZ, "No")
    winreg.CloseKey(key)
    return True


def remove_gpu_z_log_file(file_path):
    """
    Remove GPU-Z log file
    input: file_path
    return True if success
    """
    if os.path.exists(file_path):
        os.remove(file_path)
    return True


def set_gpu_z_log_file_dir(file_path):
    """
    Create the directory for GPU-Z log file
    input: file_path
    return True if success
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return True


def start_gpu_z_with_log(gpu_z_path, log_file_path):
    """
    Start GPU-Z with log file by command line
    input: gpu_z_path, log_file_path
    return True if success
    """
    try:
        add_gpu_z_key_to_registry()
        remove_gpu_z_log_file(log_file_path)
        set_gpu_z_log_file_dir(log_file_path)
        cmd_list = f"\"{gpu_z_path}\" -log \"{log_file_path}\" -minimized"
        print(f'Start GPU-Z, {cmd_list=}')
        os.popen(cmd_list)
    except Exception as e:
        print(f"Exception occurs - {e}")
        return False
    return True


def stop_gpu_z(process_name):
    """
    Stop GPU-Z process by process name
    input: process_name
    return True if success
    """
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            proc.kill()
    return True


def calculate_gpu_load_average(file_path, min_value=5, max_value=100):
    """
    Calculate GPU usage average from GPU-Z log file
    Use the GPU usage values between min_value and max_value
    input: file_path, min_value, max_value
    return GPU load average
    """
    gpu_load_average = -1
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
        df.columns = df.columns.str.strip()
        gpu_load_values = df['GPU Load [%]'].dropna()
        filtered_gpu_load_values = gpu_load_values[(gpu_load_values >= min_value) & (gpu_load_values <= max_value)]
        gpu_load_average = round(filtered_gpu_load_values.mean(), 2)
    except Exception as e:
        print(f"Exception occurs - {e}")
    return gpu_load_average


if __name__ == '__main__':
    # Call the function to get and print GPU info
    get_gpu_info()
