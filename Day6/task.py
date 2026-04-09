from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException, NetMikoAuthenticationException
from datetime import datetime
from pathlib import Path

# Inventory of devices
network_inventory = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",
        "username": "admin",
        "password": "admin123",
        "secret": "admin123",
        "port": 22,
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.1.2",
        "username": "admin",
        "password": "admin123",
        "secret": "admin123",
        "port": 22,
    },
    {
        "device_type": "cisco_ios",
        "host": "10.0.0.1",
        "username": "admin",
        "password": "admin123",
        "secret": "admin123",
        "port": 22,
    },
    {
        "device_type": "juniper_junos",
        "host": "192.168.1.3",
        "username": "admin",
        "password": "admin123",
        "port": 22,
    }
]

# Backup folder
save_path = Path("device_backups")
save_path.mkdir(exist_ok=True)

# Date and time stamp
today_stamp = datetime.now().strftime("%Y-%m-%d")
time_stamp = datetime.now().strftime("%H-%M-%S")


def get_config_command(platform):
    if platform == "cisco_ios":
        return "show running-config"
    elif platform == "juniper_junos":
        return "show configuration"
    return "show running-config"


for node in network_inventory:
    device_ip = node["host"]
    platform = node["device_type"]
    session = None

    print(f"\nConnecting to {device_ip} using {platform} driver...")

    try:
        session = ConnectHandler(**node)
        print(f"Connection established with {device_ip}")

        # Enter enable mode for Cisco if secret exists
        if platform == "cisco_ios" and "secret" in node:
            session.enable()

        prompt_name = session.find_prompt().strip("#>$")
        print(f"Detected prompt name: {prompt_name}")

        show_cmd = get_config_command(platform)
        print(f"Executing command: {show_cmd}")

        running_output = session.send_command(
            show_cmd,
            delay_factor=2,
            read_timeout=60
        )

        backup_file = save_path / f"{prompt_name}_{today_stamp}_{time_stamp}.cfg"

        with open(backup_file, "w", encoding="utf-8") as backup:
            backup.write(running_output)

        print(f"Backup completed for {prompt_name}")
        print(f"Saved at: {backup_file}")

    except NetMikoTimeoutException:
        print(f"Timeout error: unable to reach {device_ip}")

    except NetMikoAuthenticationException:
        print(f"Authentication failed for {device_ip}")

    except Exception as error:
        print(f"General failure on {device_ip}: {error}")

    finally:
        if session is not None:
            session.disconnect()
        print(f"Session closed for {device_ip}")