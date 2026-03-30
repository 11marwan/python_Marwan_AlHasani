# ask user for input of an IPv4 address 
ipv4 = input("Enter an IPv4 address: ")

# define a function to validate the IPv4 address
def validate_ipv4(ipv4):
    # split the address into its four octets
    parts = ipv4.split(".")
    if len(parts) != 4:
        return False
    
    # check if each octet is a number between 0 and 255
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True


# validate the IPv4 address and print the result
if validate_ipv4(ipv4):
    print(f"{ipv4} is a valid IPv4 address.")
else:
    print(f"{ipv4} is not a valid IPv4 address.")


# ask user for input of a list of IPv4 addresses separated by commas
listIp = input("Enter a list of IPv4 addresses separated by commas: ").split(",")

# validate each IPv4 address in the list and print the result
for ip in listIp:
    ip = ip.strip()
    if validate_ipv4(ip):
        print(f"{ip} is a valid IPv4 address.")
    else:
        print(f"{ip} is not a valid IPv4 address.")





