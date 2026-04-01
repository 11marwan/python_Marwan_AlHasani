ip = input("Enter an IP address: ")
ip = ip.strip()
cidr = input("Enter CIDR prefix : ")
# define a function to validate the IPv4 address
def validate_ipv4(ip):
    # split the address by "."
    parts = ip.split(".")
    if len(parts) != 4:
        return False

    # check if each octet is a number between 0 and 255
    for part in parts:
     if not part.isdigit() or not 0 <= int(part) <= 255:
        return False
    return True



# validate the IP address and print the result
if not validate_ipv4(ip):
    print("--- Subnet Calculator ---")
    print(f"Error: Invalid IP address or CIDR prefix provided. Details: {ip} is not a valid IPv4 address")

# validate the CIDR prefix and print the result
else:
    try:
        cidr = int(cidr) # Convert CIDR prefix to int
        if not 24 <= cidr <= 30:  # Check if CIDR prefix is between 24 and 30
            print("--- Subnet Calculator ---")
            print(f"Error: Invalid IP address or CIDR prefix provided. Details: {cidr} is not a valid netmask")
        else:
            # Calculate the network address, broadcast address, and number of usable hosts
            #https://askfilo.com/user-question-answers-smart-solutions/subnetting-formula-guide-1-to-find-the-number-of-subnets-3430393030313435
            lastPart = int(ip.split(".")[-1])
            remainigBits = (cidr % 8)
            blockSize = 2 ** (8 - remainigBits)

            netAddress = (lastPart // blockSize) * blockSize
            brodcastAddress = netAddress + blockSize - 1

            # calculate the number of usable hosts
            hostBits = 32 - cidr
            usableHosts = (2 ** hostBits) - 2
            print("--- Subnet Calculator ---")
            print(f"Network address: {ip.rsplit('.', 1)[0]}.{netAddress}")
            print(f"Broadcast address: {ip.rsplit('.', 1)[0]}.{brodcastAddress}")
            print(f"Number of usable hosts: {usableHosts}")
    except ValueError as e:
        print("--- Subnet Calculator ---")
        print(f"Error: Invalid IP address or CIDR prefix provided. Details: invalid literalfor int() with base 10: {e}")