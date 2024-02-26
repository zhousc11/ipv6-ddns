# IPv6 DDNS Repository

EN|[简中](./README.md)

## Introduction
IPv6 is used more and more widely. In China mainland, it's very convenient to access remote desktop, NAS, homeassistant,etc. But the public IPv6 address assigned by ISP is usually dynamic.

Thus if we can write a mini program to run on the host with python. It can obtain the IPv6 address, then use the API provided by the domain name service provider to update the AAAA record. So we can access our services by domain.

Which is very convenient.

> Now only support dnspod's API, will support more domain name service provider's API in the future (if I have time)
## To-do List
- [x] Obtain the IPv6 address and save to a variable
- [x] Get the domain name service provider's API
- [ ] Design a friendly user interface
- [ ] Read the API document of other domain name registrars, make it more general

## Usage
1. Download the source code
```shell
git clone https://github.com/zhousc11/ipv6-ddns.git
```
2. Install the dependencies
```shell
pip install -r requirements.txt
```
3. Modify the configuration file
```shell
cp .env.template .env
vim .env
```
4. Run
```shell
python req_dnspod.py
```

Welcome issues and PRs. Thanks for your support.

## Credits
This project uses the API provided by [IPW](https://ipw.cn) to obtain the IPv6 address, thank you very much. If there is any offense, please [contact me](mailto:zhousc11@icloud.com) to delete.

Also use the Python SDK of Tencent Cloud, thanks for the service provided by Tencent Cloud.

Thanks from a Chinese student who is learning python & git.