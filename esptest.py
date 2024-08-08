import requests

ESP8266_IP = "172.18.120.105"
ESP_PORT = 8080

def send(command):
    try:
        response = requests.get(f"http://{ESP8266_IP}/{command}")
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

while True:
    val = input("Command: ")
    send(val)