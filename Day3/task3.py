import json
import csv

# -----------------------------
# Step 1: Initialize variables
# -----------------------------
entries = []
total_lines = 0
valid_lines = 0
malformed_lines = 0

accept_count = 0
drop_count = 0

port_counter = {}
ip_counter = {}

# -----------------------------
# Step 2: Read file
# -----------------------------
with open("C:/Users/CodeLine/Desktop/marwanPyth/Day3/firewall.log", "r") as file:
    for line in file:
        total_lines += 1
        line = line.strip()

        # Skip empty or corrupted lines
        if "SRC=" not in line or "DST=" not in line:
            malformed_lines += 1
            continue

        parts = line.split()

        try:
            # Extract basic info
            timestamp = parts[0] + " " + parts[1]
            action = parts[2]
            protocol = parts[3]

            # Count actions
            if action == "ACCEPT":
                accept_count += 1
            elif action == "DROP":
                drop_count += 1

            # Initialize variables
            src_ip = src_port = dst_ip = dst_port = packet_size = ""

            # Extract fields
            for item in parts:
                if item.startswith("SRC="):
                    src_ip = item.split("=")[1]
                elif item.startswith("SPT="):
                    src_port = item.split("=")[1]
                elif item.startswith("DST="):
                    dst_ip = item.split("=")[1]
                elif item.startswith("DPT="):
                    dst_port = item.split("=")[1]
                elif item.startswith("LEN="):
                    packet_size = item.split("=")[1]

            # Store entry
            entry = {
                "timestamp": timestamp,
                "action": action,
                "protocol": protocol,
                "source_ip": src_ip,
                "source_port": src_port,
                "destination_ip": dst_ip,
                "destination_port": dst_port,
                "packet_size": packet_size
            }

            entries.append(entry)
            valid_lines += 1

            # Count ports
            if dst_port in port_counter:
                port_counter[dst_port] += 1
            else:
                port_counter[dst_port] = 1

            # Count IPs
            if src_ip in ip_counter:
                ip_counter[src_ip] += 1
            else:
                ip_counter[src_ip] = 1

        except:
            malformed_lines += 1

# -----------------------------
# Step 3: Analysis
# -----------------------------

# Top 3 ports
top_ports = sorted(port_counter.items(), key=lambda x: x[1], reverse=True)[:3]

# Suspicious IPs
suspicious_ips = {}
for ip, count in ip_counter.items():
    if count >= 3:
        suspicious_ips[ip] = count

# -----------------------------
# Step 4: Save CSV
# -----------------------------
with open("output.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Timestamp", "Action", "Protocol",
        "Source IP", "Source Port",
        "Destination IP", "Destination Port",
        "Packet Size"
    ])

    for e in entries:
        writer.writerow([
            e["timestamp"], e["action"], e["protocol"],
            e["source_ip"], e["source_port"],
            e["destination_ip"], e["destination_port"],
            e["packet_size"]
        ])

# -----------------------------
# Step 5: Save JSON
# -----------------------------
with open("output.json", "w") as jsonfile:
    json.dump(entries, jsonfile, indent=4)

# -----------------------------
# Step 6: Save Threat Report
# -----------------------------
with open("threats.txt", "w") as f:
    f.write("THREAT REPORT\n")
    f.write("============================\n")

    for ip, count in suspicious_ips.items():
        f.write(f"IP: {ip} | Occurrences: {count}\n")

# -----------------------------
# Step 7: Print Report
# -----------------------------
print("="*50)
print("FIREWALL LOG ANALYSIS REPORT")
print("="*50)

print(f"Total entries processed : {total_lines}")
print(f"Valid entries parsed    : {valid_lines}")
print(f"Malformed entries       : {malformed_lines}")

print("\n--- Action Summary ---")
print(f"ACCEPT : {accept_count}")
print(f"DROP   : {drop_count}")

print("\n--- Top 3 Destination Ports ---")
for i, (port, count) in enumerate(top_ports, 1):
    print(f"{i}. Port {port} - {count} hits")

print("\n--- Suspicious IPs ---")
for ip, count in suspicious_ips.items():
    print(f"{ip} - {count} times")

print("\nOutput saved: output.csv, output.json, threats.txt")
print("="*50)





