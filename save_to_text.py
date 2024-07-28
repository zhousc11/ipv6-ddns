import mysql.connector
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# 数据库配置
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}


# 获取当前IPv6地址
def get_ipv6_address():
    response = requests.get('http://6.ipw.cn', timeout=10, verify=False)
    return response.text.strip()


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
    ipv6_address = get_ipv6_address()
    store_ipv6_address(pc_name, ipv6_address)
    print(f"IPv6 address {ipv6_address} has been stored in the database.")
