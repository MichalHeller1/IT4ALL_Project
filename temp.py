import requests


def get_vendor_by_mac_address(mac_address):
    url = f"https://api.macvendors.com/{mac_address}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return "Unable to fetch vendor information."


mac_address = "00:21:70:4d:4f:ae"
vendor = get_vendor_by_mac_address(mac_address)
print(vendor)