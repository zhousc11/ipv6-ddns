from dotenv import load_dotenv
import os
import traceback
import random
import netifaces

ipv6_address_list = []
ip_address = ""

def get_local_ipv6_address():

    global ipv6_address_list
    for interface in netifaces.interfaces():
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET6 in addresses:
                for addr_info in addresses[netifaces.AF_INET6]:
                    ipv6_address = addr_info.get('addr')
                    if ipv6_address and '%' in ipv6_address:  # 去掉接口标识符
                        ipv6_address = ipv6_address.split('%')[0]
                    if ipv6_address and not ipv6_address.startswith('fe80'):  # 排除链路本地地址
                        ipv6_address_list.append(ipv6_address)

def Dnspod_update_dns_record() :
    global ip_address

    from tencentcloud.common.common_client import CommonClient
    from tencentcloud.common import credential
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile

    try :
        try:
            cred = credential.Credential(
                secret_id=os.environ.get("TENCENTCLOUD_SECRETID"),
                secret_key=os.environ.get("TENCENTCLOUD_SECRETKEY"))

            httpProfile = HttpProfile()
            # 域名首段必须和下文中CommonClient初始化的产品名严格匹配
            httpProfile.endpoint = "dnspod.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            # 实例化要请求的common client对象，clientProfile是可选的。
            common_client = CommonClient(service="dnspod", version='2021-03-23', credential=cred, profile=clientProfile,region="")
            # 接口参数作为json字典传入，得到的输出也是json字典，请求失败将抛出异常，headers为可选参数
            common_client_output = common_client.call_json(action="ModifyDynamicDNS", params={"Domain": os.getenv('DOMAIN'),"SubDomain": os.getenv('SUBDOMAIN'), "RecordId": int(os.getenv('TENCENTCLOUD_RECORDID')), "RecordLine": "默认", "Value": ip_address})
        except TencentCloudSDKException as err:
            print(err)
        recordid=common_client_output["Response"]["RecordId"]
    except :
        print(f"Error: Failed to update record \n common_client_output is: {common_client_output} \n ")
        traceback.print_exc()

def Cloudflare_update_dns_record() :

    from cloudflare import Cloudflare

    global ip_address
    client = Cloudflare(
    api_email=os.environ.get("CLOUDFLARE_EMAIL"), 
    api_key=os.environ.get("CLOUDFLARE_API_KEY"), 
    )
    try :
        record_response = client.dns.records.edit(
            dns_record_id=os.environ.get("CLOUDFLARE_RECORD_ID"),
            zone_id=os.environ.get("CLOUDFLARE_ZONE_ID"),
            content=ip_address,
        )
        record_response.content
    except :
        print("Error: Failed to update record \n")
        traceback.print_exc()




def main():
    
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    load_dotenv(env_path)

    ipfile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_ipv6_address.txt")
    get_local_ipv6_address()
    with open(ipfile_path, 'r') as f :
        last_ipv6_address = f.read().strip()

    if last_ipv6_address in ipv6_address_list :
        print("IPv6 address not changed.")
        exit(0)
    
    else :
        global ip_address
        ip_address = random.choice(ipv6_address_list)

        match os.getenv('DDNS_PROVIDER') :
            case 'dnspod' :
                Dnspod_update_dns_record()
            case 'cloudflare' :
                Cloudflare_update_dns_record()
            case None :
                print("DDNS_PROVIDER not set in environment variables.")
                exit(1)
            case _:
                print("Invalid DDNS_PROVIDER in environment variables.")
                exit(1)

        with open(ipfile_path, 'w') as f :
            f.write(ip_address)

        exit(0)

main()
    