import subprocess
import requests
import json
import time


def start_virtual_android():
    """Start the virtual Android system using QEMU."""
    try:
        # Launch QEMU instance (adjust paths and options as needed)
        qemu_command = [
            "qemu-system-x86_64",
            "-avd", "Your_AVD_Name",
            "-net", "user,hostfwd=tcp::5555-:5555"
        ]
        subprocess.Popen(qemu_command)
        print("Virtual Android system is starting...")
        time.sleep(30)  # Wait for the system to boot
    except Exception as e:
        print(f"Failed to start virtual Android: {e}")


def install_apk(apk_path):
    """Install a sample APK into the virtual system using ADB."""
    try:
        print("Installing APK...")
        subprocess.run(["adb", "connect", "localhost:5555"], check=True)
        subprocess.run(["adb", "install", apk_path], check=True)
        print("APK installed successfully.")
    except Exception as e:
        print(f"Failed to install APK: {e}")


def get_system_info():
    """Retrieve system information from the virtual device."""
    try:
        subprocess.run(["adb", "connect", "localhost:5555"], check=True)
        print("Fetching system information...")
        system_info = subprocess.check_output(["adb", "shell", "getprop"]).decode()
        print(system_info)
        return system_info
    except Exception as e:
        print(f"Failed to retrieve system information: {e}")
        return None


def log_to_django_api(api_url, system_info):
    """Send system information to the Django API."""
    try:
        headers = {"Content-Type": "application/json"}
        payload = {"system_info": system_info}
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        if response.status_code == 201:
            print("System information logged to Django API successfully.")
        else:
            print(f"Failed to log to API. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to connect to Django API: {e}")


if __name__ == "__main__":
    # Adjust APK path and API URL as needed
    apk_path = "sample_app.apk"  # Path to your APK file
    django_api_url = "http://127.0.0.1:8000/api/log-system-info/"  # Adjust based on your API endpoint

    # Step 1: S