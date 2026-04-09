from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from datetime import datetime
from getpass import getpass

# ========= FUNCTIONS =========

def check_telnet(config_text):
    config_text = config_text.lower()
    for line in config_text.splitlines():
        line = line.strip()
        if line.startswith("transport input") and "telnet" in line:
            return True
    return False


def check_http(config_text):
    config_text = config_text.lower()

    # If explicitly disabled, return False
    if "no ip http server" in config_text:
        return False

    # If enabled, return True
    if "ip http server" in config_text:
        return True

    return False


def check_snmp(config_text):
    config_text = config_text.lower()
    findings = []

    if "snmp-server community public" in config_text:
        findings.append("public")

    if "snmp-server community private" in config_text:
        findings.append("private")

    return findings


def audit_config(config_text):
    telnet_enabled = check_telnet(config_text)
    http_enabled = check_http(config_text)
    snmp_defaults = check_snmp(config_text)

    return {
        "telnet_enabled": telnet_enabled,
        "http_enabled": http_enabled,
        "snmp_defaults": snmp_defaults
    }


# ========= DEVICE LIST =========
# Replace these IPs/usernames with your real lab or real devices

username = input("Enter SSH username: ")
password = getpass("Enter SSH password: ")
enable_secret = getpass("Enter enable secret (press Enter if not needed): ")

devices = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",
        "username": username,
        "password": password,
        "secret": enable_secret,
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.1.2",
        "username": username,
        "password": password,
        "secret": enable_secret,
    }
]

# ========= REPORT FILE =========

today = datetime.now().strftime("%Y-%m-%d")
report_filename = f"Audit_Report_{today}.txt"

total_telnet = 0
total_http = 0
total_snmp = 0

with open(report_filename, "w") as report:
    report.write("--- Network Device Audit Report ---\n\n")

    for device in devices:
        host = device["host"]

        try:
            print(f"Connecting to {host} ...")

            connection = ConnectHandler(**device)

            # Enter enable mode if secret was provided
            if device.get("secret"):
                connection.enable()

            # Pull live running config
            running_config = connection.send_command("show running-config")

            # Audit the config
            results = audit_config(running_config)

            report.write(f"Device: {host}\n")

            if results["telnet_enabled"]:
                report.write("- Telnet Status: Telnet is enabled\n")
                total_telnet += 1
            else:
                report.write("- Telnet Status: Telnet is disabled\n")

            if results["http_enabled"]:
                report.write("- HTTP Server Status: HTTP server is enabled\n")
                total_http += 1
            else:
                report.write("- HTTP Server Status: HTTP server is disabled\n")

            if results["snmp_defaults"]:
                found_strings = ", ".join(results["snmp_defaults"])
                report.write(f"- SNMP Status: Default SNMP community strings found ({found_strings})\n")
                total_snmp += 1
            else:
                report.write("- SNMP Status: No default SNMP community strings found\n")

            report.write("\n")

            connection.disconnect()

        except NetmikoAuthenticationException:
            report.write(f"Device: {host}\n")
            report.write("- ERROR: Authentication failed\n\n")

        except NetmikoTimeoutException:
            report.write(f"Device: {host}\n")
            report.write("- ERROR: Connection timed out\n\n")

        except Exception as e:
            report.write(f"Device: {host}\n")
            report.write(f"- ERROR: {str(e)}\n\n")

    report.write("--- Summary ---\n")
    report.write(f"Devices with Telnet enabled: {total_telnet}\n")
    report.write(f"Devices with HTTP server enabled: {total_http}\n")
    report.write(f"Devices with default SNMP strings: {total_snmp}\n")

print(f"Audit report saved to {report_filename}")