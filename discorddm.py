import requests

DISCORD_TOKEN = "YOUR_DISCORD_TOKEN"
FRIEND_USER_ID = "YOUR FRIENDS USER ID"
DM_API_URL = f"https://discord.com/api/v9/users/@me/channels"

headers = {
    "Authorization": DISCORD_TOKEN,
    "Content-Type": "application/json"
}

def get_external_ip():
    response = requests.get("https://api.ipify.org?format=json")
    return response.json().get("ip")

def send_discord_message(channel_id, message):
    payload = {"content": message}
    response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("id")
    return None

def pin_discord_message(channel_id, message_id):
    response = requests.put(f"https://discord.com/api/v9/channels/{channel_id}/pins/{message_id}", headers=headers)
    return response.status_code == 204

def get_dm_channel_id(friend_user_id):
    payload = {"recipient_id": friend_user_id}
    response = requests.post(DM_API_URL, headers=headers, json=payload)
    return response.json().get("id")

def main():
    current_ip = get_external_ip()
    
    # Load the last known IP address from a file
    try:
        with open("last_known_ip.txt", "r") as file:
            last_known_ip = file.read().strip()
    except FileNotFoundError:
        last_known_ip = None

    # If the IP has changed, notify via Discord and update the stored IP
    if current_ip != last_known_ip:
        channel_id = get_dm_channel_id(FRIEND_USER_ID)
        message = f"Your IP address has changed to {current_ip}"
        message_id = send_discord_message(channel_id, message)
        if message_id:
            pin_discord_message(channel_id, message_id)
            print("IP change notification sent and pinned.")
        else:
            print("Failed to send message.")

        # Save the new IP to a file
        with open("last_known_ip.txt", "w") as file:
            file.write(current_ip)
    else:
        print("No IP change detected.")

if __name__ == "__main__":
    main()
