from netmiko.ssh_autodetect import SSHDetect

remote_device = {
    "device_type": "autodetect",
    "host": "10.199.199.101",
    "username": "admin",
    "password": "admin",
}


def detect(host: str, username: str, password: str) -> str:
    device = {
        "device_type": "autodetect",
        "host": host,
        "username": username,
        "password": password,
    }
    guesser = SSHDetect(**device)
    best_match = guesser.autodetect()
    return best_match
