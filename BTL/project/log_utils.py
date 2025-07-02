# log_utils.py
import datetime
import socket
import os


def write_log(user_id, action_type, description):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = get_local_ip()
    log_line = f"{user_id}|{action_type}|{description}|{now}|{ip}\n"
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(log_line)


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip = "127.0.0.1"
    return ip
