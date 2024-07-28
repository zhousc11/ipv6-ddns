# To-do: read dnspod api doc and implement the function
import json
import logging
import os
import netifaces

from dotenv import load_dotenv
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.dnspod.v20210323 import dnspod_client, models


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
    #     else:
    #         raise Exception("No IPv6 address found.")
    # logging.log(logging.ERROR, "Error retrieving IPv6 addresses.")
    return None


load_dotenv()

SecretID = os.environ.get('TENCENTCLOUD_SECRETID')
SecretKey = os.environ.get('TENCENTCLOUD_SECRETKEY')

Domain = os.environ.get('DOMAIN')
SubDomain = os.environ.get('SUBDOMAIN')

# print(SecretID, SecretKey)
try:
    cred = credential.Credential(SecretID, SecretKey)

    httpProfile = HttpProfile()
    httpProfile.endpoint = 'dnspod.tencentcloudapi.com'

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile

    client = dnspod_client.DnspodClient(cred, "", clientProfile)

    req = models.CreateRecordRequest()
    params = {
        'Domain': Domain,
        'SubDomain': SubDomain,
        'RecordType': 'AAAA',
        'RecordLine': '默认',
        'Value': get_local_ipv6_address()
    }
    req.from_json_string(json.dumps(params))

    resp = client.CreateRecord(req)

    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)
