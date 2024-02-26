# To-do: read dnspod api doc and implement the function
import json
import os

from dotenv import load_dotenv
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.dnspod.v20210323 import dnspod_client, models

from get_ipv6 import get_ipv6

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
        'Value': get_ipv6()
    }
    req.from_json_string(json.dumps(params))

    resp = client.CreateRecord(req)

    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)
