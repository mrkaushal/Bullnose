import json
import requests
import socket
import uuid
import re


def api_call():
    
    try:
    # Get the client's public IP address
      clientPublicIp = " " + requests.get('https://api.ipify.org').text
      if " " in clientPublicIp:
          clientPublicIp = clientPublicIp.replace(" ","")
    except Exception as e:
        print("Exception while retrieving public IP address, using default value", e)
        clientPublicIp = "106.193.147.98"  # default value if unable to retrieve
    try:
        # Get the client's local IP address
        hostname = socket.gethostname()
        clientLocalIp = socket.gethostbyname(hostname)
    except Exception as e:
        print("Exception while retrieving local IP address, using default value", e)
        clientLocalIp = "127.0.0.1"  # default value if unable to retrieve
    try:
        # Get the client's MAC address
        clientMacAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    except Exception as e:
        print("Exception while retrieving MAC address, using default value", e)
        clientMacAddress = "00:00:00:00:00:00"  # default value if unable to retrieve

    url = "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword"
    payload = {
        "clientcode": "K50494801",
        "password": "1379",
        "totp": "994159"
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-UserType": "USER",
        "X-SourceID": "WEB",
        "X-ClientLocalIP": clientLocalIp,
        "X-ClientPublicIP": clientPublicIp,
        "X-MACAddress": clientMacAddress,
        "X-PrivateKey": "NRlI1dza"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()

    refreshToken = data['data']['refreshToken']
    feedToken = data['data']['feedToken']
    jwtToken = data['data']['jwtToken']

    