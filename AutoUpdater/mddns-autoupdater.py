import subprocess
import json
import socket


# Haal benodigde informatie uit het configuratiebestand op
def read_configuration(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
        return config["api_key"], config["api_ip"], config["subdomains"]


# Het huidige IP-adres ophalen dat op de Bind server bekend is
def GetCurrentDNSip(url, api_key):
    try:
        result = subprocess.run(["curl", url, "-H", f"X-API-Key: {api_key}"], capture_output=True, text=True,
                                check=True)
        json_response = json.loads(result.stdout)
        if "ipv4" in json_response and not json_response["error"]:
            return json_response["ipv4"]
        else:
            print("Error in response:", json_response)
            return None
    except subprocess.CalledProcessError as e:
        print("Error executing curl command:", e)
        return None


# Functie om het DNS-record te updaten door middel van de API
def UpdateDNSRecord(api_key, api_ip, subdomain, new_ip):
    url = f"https://{api_ip}/subdomain/name/{subdomain}"
    data = {"ip": new_ip}
    try:
        subprocess.run(["curl", url, "-H", f"Content-type: application/json", "-H", f"X-API-Key: {api_key}", "-d",
                        json.dumps(data), "-X", "PUT"], check=True)
        print(f"DNS record for subdomain '{subdomain}' updated successfully with IP '{new_ip}'.")
    except subprocess.CalledProcessError as e:
        print("Error updating DNS record:", e)


def main():
    # Configuratiebestand
    config_file = "mddns-autoupdater-config.json"

    # Haal benodigde informatie uit het configuratiebestand op
    api_key, api_ip, subdomains, = read_configuration(config_file)

    # Get local IP address
    local_ip = socket.gethostbyname(socket.gethostname())

    # Check DNS records for each subdomain
    for subdomain in subdomains:
        current_ip = GetCurrentDNSip(f"https://{api_ip}/subdomain/name/{subdomain}", api_key)
        if current_ip is None:
            print(f"Failed to retrieve DNS record for subdomain '{subdomain}'.")
            continue

        # Update DNS record if necessary
        if current_ip != local_ip:
            print(f"Updating DNS record for subdomain '{subdomain}'...")
            UpdateDNSRecord(api_key, api_ip, subdomain, local_ip)
        else:
            print(f"DNS record for subdomain '{subdomain}' is already up to date.")


if __name__ == "__main__":
    main()
