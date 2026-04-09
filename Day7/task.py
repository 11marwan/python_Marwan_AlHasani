import subprocess
import json
import yaml
import smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

# Define subnet to scan
base_ip = "192.168.1."
ip_range = range(1, 255)

# Email settings
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASS = "your_app_password"
DEST_EMAIL = "receiver_email@gmail.com"

# Store scan output
scan_data = []

print("Launching ping sweep...")

for i in ip_range:
    current_ip = f"{base_ip}{i}"

    try:
        ping_process = subprocess.run(
            ["ping", "-c", "1", "-W", "1", current_ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        device_state = "Reachable" if ping_process.returncode == 0 else "Unreachable"

        scan_data.append({
            "address": current_ip,
            "state": device_state,
            "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as err:
        scan_data.append({
            "address": current_ip,
            "state": "Failure",
            "details": str(err)
        })

print("Ping sweep finished.")

# Create output directory
output_dir = Path("scan_outputs")
output_dir.mkdir(exist_ok=True)

# File names
json_output = output_dir / "scan_results.json"
yaml_output = output_dir / "scan_results.yaml"

# Write JSON
with open(json_output, "w", encoding="utf-8") as jf:
    json.dump(scan_data, jf, indent=2)

# Write YAML
with open(yaml_output, "w", encoding="utf-8") as yf:
    yaml.dump(scan_data, yf, default_flow_style=False)

print("Files generated successfully.")

# Prepare email
email_msg = EmailMessage()
email_msg["Subject"] = "Automated Network Scan Results"
email_msg["From"] = SENDER_EMAIL
email_msg["To"] = DEST_EMAIL
email_msg.set_content("Please find attached the latest scan results in JSON and YAML formats.")

# Attach JSON
with open(json_output, "rb") as jf:
    email_msg.add_attachment(
        jf.read(),
        maintype="application",
        subtype="json",
        filename="scan_results.json"
    )

# Attach YAML
with open(yaml_output, "rb") as yf:
    email_msg.add_attachment(
        yf.read(),
        maintype="application",
        subtype="x-yaml",
        filename="scan_results.yaml"
    )

# Send email
try:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp_conn:
        smtp_conn.starttls()
        smtp_conn.login(SENDER_EMAIL, SENDER_PASS)
        smtp_conn.send_message(email_msg)

    print("Report email delivered successfully.")

except Exception as mail_error:
    print(f"Email sending failed: {mail_error}")