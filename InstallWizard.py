from platform import system as system_name
import os
import sys
import traceback
import subprocess

class InstallWizard:
    def __init__(self):
        self.env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        self.requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")

    def setup_environment(self):
        """处理虚拟环境和依赖安装"""
        if sys.prefix == sys.base_prefix:
            venv_path = self.get_valid_venv_path()
            self.create_virtualenv(venv_path)
            venv_python = self.get_venv_python(venv_path)
            self.install_dependencies(venv_python)
            self.relaunch_with_venv(venv_python)
        else:
            print(f"Using venv: {sys.prefix}")
            self.check_and_install_dependencies()

    def get_valid_venv_path(self):
        """获取有效的虚拟环境路径"""
        while True:
            venv_path = input("Enter NEW venv path:\ne.g. ./ddns\n").strip()
            try:
                os.makedirs(venv_path, exist_ok=True)
                return venv_path
            except OSError as e:
                print(f"Path not accessible: {e}")

    def create_virtualenv(self, venv_path):
        """创建虚拟环境"""
        import venv
        venv.create(venv_path, with_pip=True)

    def get_venv_python(self, venv_path):
        """获取虚拟环境的Python路径"""
        return os.path.join(venv_path, 'Scripts' if system_name() == 'Windows' else 'bin', 'python')

    def install_dependencies(self, python_path):
        """安装依赖项"""
        try:
            subprocess.run([python_path, '-m', 'pip', 'install', '-r', self.requirements_path], 
                          check=True, capture_output=True, text=True)
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            self.handle_installation_error(e)

    def handle_installation_error(self, error):
        """处理安装错误"""
        print(f"Error installing dependencies:\n{error.stderr}")
        traceback.print_exc()
        sys.exit(1)

    def relaunch_with_venv(self, venv_python):
        """用虚拟环境重新启动程序"""
        new_process = subprocess.Popen([venv_python] + sys.argv)
        new_process.wait()
        sys.exit(0)

    def check_and_install_dependencies(self):
        """检查并安装依赖"""
        try:
            import cloudflare, tencentcloud.common, dotenv
        except ImportError:
            self.install_dependencies(sys.executable)
            self.relaunch_with_venv(sys.executable)

    def configure_network_interfaces(self):
        from dotenv import set_key
        """配置网络接口"""
        if input("Assign specific NIC?(y/n)\n").lower() == 'y':
            import netifaces
            interfaces = netifaces.interfaces()
            selected = input(f"Available NICs:\n{interfaces}\nPlease select one by typing FULL NAME: ")
            set_key(self.env_path, 'ETH_LIST', selected.replace("'", "").replace('"', ""))

    def initialize_ddns(self):
        """初始化DDNS配置"""
        from dotenv import load_dotenv
        load_dotenv()
        self.set_ddns()
        self.create_ip_file()

    def create_ip_file(self):
        """创建IP记录文件"""
        ipfile_path = os.path.join(os.path.dirname(__file__), "last_ipv6_address.txt")
        with open(ipfile_path, 'w') as f:
            f.write("never runned")

    def get_user_input_and_set_env(self, prompt_text, env_key):
        from dotenv import set_key
        value = None
        while not value:
            value = input(prompt_text).strip()
        os.environ[env_key] = value
        set_key(self.env_path, env_key, value)

    def dnspod_set_ddns(self):
        from dotenv import set_key

        self.get_user_input_and_set_env("Please enter your secret id：", "TENCENTCLOUD_SECRETID")
        self.get_user_input_and_set_env("Please enter your secret key：", "TENCENTCLOUD_SECRETKEY")

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
                set_key(self.env_path, "TENCENTCLOUD_RECORDID", os.environ["TENCENTCLOUD_RECORDID"])
            except :
                print(f"Error: Failed to get RecordId \n common_client_output is: {common_client_output} \n ")
                traceback.print_exc()

        TencentCloud_get_recordid()

    def cloudflare_set_ddns(self):
        from dotenv import set_key
        
        self.get_user_input_and_set_env(" Please enter your Cloudflare email：", "CLOUDFLARE_EMAIL")
        self.get_user_input_and_set_env(" Please enter your Cloudflare API key：", "CLOUDFLARE_API_KEY")

        from cloudflare import Cloudflare

        def CF_get_zone_id(client, domain):
            try:
                page = client.zones.list(name=domain)
                return page.result[0].id
            except Exception as e:
                print(f"Error: Failed to get Zone ID for domain {domain}\n{e}")
                traceback.print_exc()

        def CF_get_record_id(client, zone_id, sub_domain, domain):

            if sub_domain == "@":
                domainname = domain
            else:
                domainname = f"{sub_domain}.{domain}"

            try:
                page = client.dns.records.list(zone_id=zone_id, name=domainname, type='AAAA')
                return page.result[0].id
            except Exception as e:
                print(f"Error: Failed to get Record ID for subdomain {domainname}\n{e}")
                traceback.print_exc()

        try :
            client = Cloudflare(api_email=os.environ.get('CLOUDFLARE_EMAIL'), api_key=os.environ.get('CLOUDFLARE_API_KEY'))

            domain = os.environ.get('DOMAIN')
            sub_domain = os.environ.get('SUBDOMAIN')

            zone_id = CF_get_zone_id(client, domain)
            record_id = CF_get_record_id(client, zone_id, sub_domain, domain)

            os.environ["CLOUDFLARE_ZONE_ID"] = str(zone_id)
            set_key(self.env_path, "CLOUDFLARE_ZONE_ID", os.environ["CLOUDFLARE_ZONE_ID"])
            os.environ["CLOUDFLARE_RECORD_ID"] = str(record_id)
            set_key(self.env_path, "CLOUDFLARE_RECORD_ID", os.environ["CLOUDFLARE_RECORD_ID"])
        except Exception as e:
            print(f"Error: Failed to set DDNS with Cloudflare\n{e}")
            traceback.print_exc()

    def set_ddns(self):
        from dotenv import load_dotenv , set_key
        load_dotenv()

        ddns_provider = None
        while not ddns_provider in ['dnspod','cloudflare']:
            ddns_provider = input("\nPlease select a DDNS provider: dnspod/cloudflare: ")
        os.environ['DDNS_PROVIDER'] = ddns_provider
        set_key(self.env_path, 'DDNS_PROVIDER', ddns_provider)

        self.get_user_input_and_set_env("\nPlease enter your domain name\ne.g. example.com; ddns.example.com", "DOMAIN")
        self.get_user_input_and_set_env("\nPlease enter your sub domain name\ne.g. foo for foo.example.com", "SUBDOMAIN")

        match ddns_provider:
            case 'dnspod':
                self.dnspod_set_ddns()
            case 'cloudflare':
                self.cloudflare_set_ddns()

    def Linux_Install(self):
        import subprocess

        main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
        try:
            print(f"Modifying{main_path}executable permissions...")
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

        if input(f"Setting crontab, current user's crontab will be override with the followings:\n{new_cron_content}\nDo you want to set the crontab? (y/n): ") == 'y':
            pass
        else:
            print(f'Done! Update command is "{sys.executable} {main_path}", please set crontab by yourself.')
            exit(0)

        try:
            subprocess.run(['crontab', '-'], input=new_cron_content, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to set crontab\n{e}")
            traceback.print_exc()
            exit(1)
        else:
            print("Crontab set successfully!")
            exit(0)


    def Windows_Install(self):
        import subprocess

        main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
        pythonw_path = os.path.join(os.path.dirname(os.path.abspath(sys.executable)), "pythonw.exe")

        if input(f"Setting routine task, will run as current user per minute.\nDo you want to set this? (y/n): ") == 'y':
            pass
        else:
            print(f'Done! Update command is "{pythonw_path} {main_path}", please set routine task by yourself.')
            exit(0)

        command = f'schtasks /create /tn "ipv6_ddns" /tr "\'{pythonw_path}\' \'{main_path}\'" /sc MINUTE /np'
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to set crontab\n{e}")
            traceback.print_exc()
            exit(1)
        else:
            print("Routine task set successfully!")
            exit(0)
        

    def MacOS_Install(self):
        main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
        print(f'Done! Update command is "{sys.executable} {main_path}", please set routine task by yourself.')
        exit(0)

    def Unknown_platform_Install(self):

        main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
        print(f'Done! Update command is "{sys.executable} {main_path}", please set routine task by yourself.')
        exit(0)

    def main(self):
        self.setup_environment()
        self.initialize_ddns()
        self.configure_network_interfaces()
        
        # 根据平台执行安装
        platform_installers = {
            'Windows': self.Windows_Install,
            'Linux': self.Linux_Install,
            'Darwin': self.MacOS_Install
        }
        installer = platform_installers.get(system_name(), self.Unknown_platform_Install)
        installer()

if __name__ == "__main__":
    wizard = InstallWizard()
    wizard.main()