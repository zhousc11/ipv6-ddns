from platform import system as system_name
import os
import sys
import traceback

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

def Linux_Install():
    import subprocess

    main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
    try:
        print(f"正在赋予{main_path}执行权限...")
        subprocess.run(['chmod', '+x', main_path])
    except:
        print(f"Error: Failed to set execute permission for {main_path}")
        traceback.print_exc()
        exit(1)


    cron = ""
    while not cron:
        cron = input("input your cron (exmaple:* * * * *): ")

    try:
        current_cron = subprocess.check_output(['crontab', '-l'], text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to get current crontab\n{e}")
        traceback.print_exc()
        exit(1)


    new_cron_entry = f'{cron} {sys.executable} {main_path}\n'
    new_cron_content = current_cron + new_cron_entry

    if input(f"正在设置定时任务，当前用户cron将被覆盖为以下内容：\n {new_cron_content}\nDo you want to set the crontab? (y/n): ") == 'y':
        pass
    else:
        print(f'完毕！执行DDNS更新命令为"{sys.executable} {main_path}"，请自行设置定时任务。')
        exit(0)

    try:
        subprocess.run(['crontab', '-'], input=new_cron_content, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to set crontab\n{e}")
        traceback.print_exc()
        exit(1)
    else:
        print("定时任务设置成功！")
        exit(0)


def Windows_Install():
    import subprocess

    main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
    pythonw_path = os.path.join(os.path.dirname(os.path.abspath(sys.executable)), "pythonw.exe")

    if input(f"正在设置定时任务，以当前用户权限每分钟执行一次\nDo you want to set this? (y/n): ") == 'y':
        pass
    else:
        print(f'完毕！执行DDNS更新命令为"{pythonw_path} {main_path}"，请自行设置定时任务。')
        exit(0)

    command = f'schtasks /create /tn "ipv6_ddns" /tr "\'{pythonw_path}\' \'{main_path}\'" /sc MINUTE /np'
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to set crontab\n{e}")
        traceback.print_exc()
        exit(1)
    else:
        print("定时任务设置成功！")
        exit(0)
    

def MacOS_Install():
    main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
    print(f'完毕！执行DDNS更新命令为"{sys.executable} {main_path}"，请自行设置定时任务。')
    exit(0)

def Unknown_platform_Install():

    main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
    print(f'完毕！执行DDNS更新命令为"{sys.executable} {main_path}"，请自行设置定时任务。')
    exit(0)



def dnspod_set_ddns():
    from dotenv import set_key

    scretid = None
    while not scretid:
        scretid = input(" Please enter your secret id：")
    os.environ['TENCENTCLOUD_SECRETID'] = scretid
    set_key(env_path, 'TENCENTCLOUD_SECRETID', scretid)

    secretkey = None
    while not secretkey:
        secretkey = input(" Please enter your secret key：")
    os.environ['TENCENTCLOUD_SECRETKEY'] = secretkey
    set_key(env_path, 'TENCENTCLOUD_SECRETKEY', secretkey)

    from tencentcloud.common.common_client import CommonClient
    from tencentcloud.common import credential
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile

    def TencentCloud_get_recordid():
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
                common_client_output = common_client.call_json(action="DescribeRecordList", params={"Domain": os.getenv('DOMAIN'),"Subdomain": os.getenv('SUBDOMAIN'), "RecordType": "AAAA"})
            except TencentCloudSDKException as err:
                print(err)
            RecordId = common_client_output['Response']['RecordList'][0]['RecordId']
            os.environ["TENCENTCLOUD_RECORDID"] = str(RecordId)
            set_key(env_path, "TENCENTCLOUD_RECORDID", os.environ["TENCENTCLOUD_RECORDID"])
        except :
            print(f"Error: Failed to get RecordId \n common_client_output is: {common_client_output} \n ")
            traceback.print_exc()

    TencentCloud_get_recordid()

def cloudflare_set_ddns():
    from dotenv import set_key
    
    cf_email = None
    while not cf_email:
        cf_email = input(" Please enter your Cloudflare email：")
    os.environ['CLOUDFLARE_EMAIL'] = cf_email
    set_key(env_path, 'CLOUDFLARE_EMAIL', cf_email)


    cf_api_key = None
    while not cf_api_key:
        cf_api_key = input(" Please enter your Cloudflare API key：")
    os.environ['CLOUDFLARE_API_KEY'] = cf_api_key
    set_key(env_path, 'CLOUDFLARE_API_KEY', cf_api_key)

    from cloudflare import Cloudflare

    def CF_get_zone_id(client, domain):
        try:
            page = client.zones.list(name=domain)
            return page.result[0].id
        except Exception as e:
            print(f"Error: Failed to get Zone ID for domain {domain}\n{e}")
            traceback.print_exc()

    def CF_get_record_id(client, zone_id, sub_domain, domain):

        try:
            page = client.dns.records.list(zone_id=zone_id, name=f"{sub_domain}.{domain}")
            return page.result[0].id
        except Exception as e:
            print(f"Error: Failed to get Record ID for subdomain {sub_domain}.{domain}\n{e}")
            traceback.print_exc()

    try :
        client = Cloudflare(api_email=os.environ.get('CLOUDFLARE_EMAIL'), api_key=os.environ.get('CLOUDFLARE_API_KEY'))

        domain = os.environ.get('DOMAIN')
        sub_domain = os.environ.get('SUBDOMAIN')

        zone_id = CF_get_zone_id(client, domain)
        record_id = CF_get_record_id(client, zone_id, sub_domain, domain)

        os.environ["CLOUDFLARE_ZONE_ID"] = str(zone_id)
        set_key(env_path, "CLOUDFLARE_ZONE_ID", os.environ["CLOUDFLARE_ZONE_ID"])
        os.environ["CLOUDFLARE_RECORD_ID"] = str(record_id)
        set_key(env_path, "CLOUDFLARE_RECORD_ID", os.environ["CLOUDFLARE_RECORD_ID"])
    except Exception as e:
        print(f"Error: Failed to set DDNS with Cloudflare\n{e}")
        traceback.print_exc()

def set_ddns():
    from dotenv import load_dotenv , set_key
    load_dotenv()

    ddns_provider = None
    while not ddns_provider in ['dnspod','cloudflare']:
        ddns_provider = input("\nPlease select a DDNS provider: dnspod/cloudflare: ")
    os.environ['DDNS_PROVIDER'] = ddns_provider
    set_key(env_path, 'DDNS_PROVIDER', ddns_provider)

    domain = None
    while not domain:
        domain = input(" \nPlease enter your domain name (for example: the root domain hosted with your DNS provider, such as 'ddns.example.com' if it is hosted via NS records on Dnspod, then enter 'ddns.example.com')：")
    os.environ['DOMAIN'] = domain
    set_key(env_path, 'DOMAIN', domain)

    sub_domain = None
    while not sub_domain:
        sub_domain = input("\nPlease enter your sub domain name (for example: 'emm' if you want to use 'emm.ddns.example.com' as your DDNS domain name)：")
    os.environ['SUBDOMAIN'] = sub_domain
    set_key(env_path, 'SUBDOMAIN', sub_domain)

    match ddns_provider:
        case 'dnspod':
            dnspod_set_ddns()
        case 'cloudflare':
            cloudflare_set_ddns()

def main():

    import subprocess

    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")

    print("初始化环境……")
    if sys.prefix != sys.base_prefix :
        pass
    else :
        print("请在虚拟环境运行……")
        venv_path = ""

        while not os.path.isdir(venv_path):
            venv_path = input("正在尝试创建虚拟环境，请输入用户可写路径，目标应当为空文件夹(路径不存在时将尝试创建)：")
            if os.path.exists(venv_path) and os.path.isdir(venv_path):
                break
            elif os.path.exists(venv_path) and not os.path.isdir(venv_path):
                print("路径已存在，但不是文件夹")
                venv_path = ""
            else:
                try:
                    os.makedirs(venv_path)
                except OSError as e:
                    print(f"路径不可用，创建失败: {e}")
                    venv_path = ""
        
        import venv
        venv.create(venv_path, with_pip=True)

        if system_name() == 'Windows':
            venv_python = os.path.join(venv_path, 'Scripts', 'python.exe')
        else:
            venv_python = os.path.join(venv_path, 'bin', 'python')
        
        print("安装依赖……")
        try:
            subprocess.run([venv_python, '-m', 'pip', 'install', '-r', requirements_path], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"依赖安装失败，请手动在虚拟环境中安装依赖……\n{e.stderr}")
            traceback.print_exc()
            sys.exit(1)
        else:
            print("依赖安装成功！")

        newbash = subprocess.Popen([venv_python] + sys.argv)
        newbash.wait()
        sys.exit(0)
    
    try:
        import cloudflare
        import tencentcloud.common
        import dotenv
    except ImportError:
        print("安装依赖……")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', requirements_path], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"依赖安装失败，请手动在虚拟环境中安装依赖……\n{e.stderr}")
            traceback.print_exc()
            sys.exit(1)
        else:
            print("依赖安装成功！")
            newbash = subprocess.Popen([sys.executable] + sys.argv)
            newbash.wait()
            sys.exit(0)


    from dotenv import load_dotenv
    load_dotenv()

    set_ddns()

    ipfile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_ipv6_address.txt")
    with open(ipfile_path, 'w') as f:
        f.write("never runned")

    match system_name():
        case 'Windows':
            Windows_Install()
        case 'Linux':
            Linux_Install()
        case 'Darwin':
            MacOS_Install()
        case _:
            Unknown_platform_Install()

main()