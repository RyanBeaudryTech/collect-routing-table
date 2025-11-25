from netmiko import ConnectHandler
import paramiko
import yaml

# (Optional) For older routers that only support legacy ciphers:
paramiko.Transport._preferred_kex = (
    'diffie-hellman-group14-sha1',
    'diffie-hellman-group-exchange-sha1'
)
paramiko.Transport._preferred_keys = ('ssh-rsa',)


# Load routers from YAML file
with open("routers.yaml", "r") as f:
    data = yaml.safe_load(f)

routers = data["routers"]

# Connect to each router
for router in routers:
    print(f"Connecting to {router['hostname']} ({router['host']}:{router['port']})...")

    # Copy router dict to avoid modifying original
    netmiko_params = router.copy()
    hostname = netmiko_params.pop("hostname")  # remove before passing to ConnectHandler

    try:
        connection = ConnectHandler(**netmiko_params)
        output = connection.send_command("show ip route")

        filename = f"{router['hostname']}_{router['host']}_route.txt"
        with open(filename, "w") as file:
            file.write(output)

        print(f"Saved route table to {filename}")
        connection.disconnect()

    except Exception as e:
        print(f"Failed to connect to {router['host']}:{router['port']} - {e}")

