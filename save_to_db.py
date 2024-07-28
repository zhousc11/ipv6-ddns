import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os
import netifaces
import logging

load_dotenv()

# 数据库配置
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}


# 获取当前IPv6地址
def get_local_ipv6_address():
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET6 in addresses:
            for addr_info in addresses[netifaces.AF_INET6]:
                ipv6_address = addr_info.get('addr')
                if ipv6_address and '%' in ipv6_address:  # 去掉接口标识符
                    ipv6_address = ipv6_address.split('%')[0]
                if ipv6_address and not ipv6_address.startswith('fe80'):  # 排除链路本地地址
                    return ipv6_address
                else:
                    raise Exception("No global IPv6 address found.")
        else:
            raise Exception("No IPv6 address found.")
    logging.log(logging.ERROR, "Error retrieving IPv6 addresses.")
    return None


# 将IPv6地址存入数据库
def store_ipv6_address(pc_name, ipv6_address):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    insert_query = (
        "INSERT INTO ipv6_addresses (pc_name, ipv6_address, timestamp) "
        "VALUES (%s, %s, %s)"
    )
    cursor.execute(insert_query, (pc_name, ipv6_address, datetime.now()))

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    pc_name = 'Your_PC_Name'  # 你可以根据需要更改这个名称
    ipv6_address = get_local_ipv6_address()
    store_ipv6_address(pc_name, ipv6_address)
    print(f"IPv6 address {ipv6_address} has been stored in the database.")
