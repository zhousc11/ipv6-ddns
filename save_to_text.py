import time
from datetime import datetime
from get_ipv6 import get_ipv6


def append_to_file(text):
    with open('ipv6.txt', 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f'{datetime.now()} - {text}\n')


if __name__ == '__main__':
    while True:
        ipv6 = get_ipv6()
        if ipv6:
            append_to_file(ipv6)
        else:
            append_to_file('Failed to get IPv6 address')
        time.sleep(5)
