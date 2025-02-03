# IPv6 DDNS仓库

简中|[EN](./README_EN.md)

## 介绍
现在IPv6越来越普及了，用IPv6去访问远程桌面，NAS，Homeassistant这样的服务真的很方便，但是运营上给的IPv6地址不是固定的，经常会变动。

所以如果我们能够写一个小程序，在主机上运行，获取IPv6地址，然后使用域名服务商们的API去更新域名的AAAA记录，那么我们就可以通过域名去访问我们的服务了。

这样就可以极大的方便我们的使用。

> 现在只支持dnspod、cloudflare的API，后续会支持更多的域名服务商的API（如果我有时间）
## To-do list
- [x] 获取IPv6地址并存入变量
- [x] 获取域名服务商的API
- [ ] 一个能用的GUI （++一个用户引导
- [ ] 看看别家域名注册商的API文档，更通用  （++添加了cloudflare

## 先决条件
- 运行需要python环境
- 使用前应当已创建域名的AAAA记录

## 使用方法
1. 下载源码
```shell
git clone https://github.com/zhousc11/ipv6-ddns.git
```
2. 进入目录
```shell
cd ipv6-ddns
```
3. 运行引导
```shell
python3 InstallWizard.py
```
> Windows、Linux支持自动添加定时任务，其他系统请自行添加。

> Domain是指托管在DNS服务商的域名，例如 通过NS记录，将ddns.example.com托管到Dnspod，ddns.example.com 即为Domain ；通过解析DNS服务器，将example.com托管到Cloudflare，example.com 即为Domain。

> Subdomain是指在DNS服务商添加的主机记录，例如 将ddns.example.com托管到Dnspod，使用 ipv6.ddns.example.com 作为 指向本机IPv6地址 的域，ipv6 即为Subdomain ； 将example.com托管到Cloudflare，使用 ipv6.ddns.example.com 作为 指向本机IPv6地址 的域，ipv6.ddns 即为Subdomain 。

> 直接使用Domain作为指向本机IPv6地址的域 ，请在Subdomain填入 @ 。

欢迎issues和PRs，谢谢你的支持。

## API令牌配置
- 腾讯云Dnspod
> 腾讯云是指cloud.tencent.com而非tencentcloud.com。
1. 转到[腾讯云CAM](https://console.cloud.tencent.com/cam)，新建子用户
2. 快速创建-> 访问方式-编程访问,用户权限-策略-QcloudDNSPodFullAccess -> 保存SecretId、SecretKey。
> SecretId、SecretKey丢失时，请到[腾讯云CAM](https://console.cloud.tencent.com/cam) -> 用户详情 -> API 密钥 进行新建密钥。
> 每个子用户限制最多 2 对密钥。
> [DnspodToken](https://console.dnspod.cn/account/token/token)实际已不可用。

- Cloudflare
  转到[Cloudflare API令牌](https://dash.cloudflare.com/profile/api-tokens) -> API 密钥 -> Global API Key ，查看并保存。
> API 令牌不可用于需要使用的API [Update DNS Record](https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/edit/)和[List DNS Records](https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/list/)（Security：
API Email + API Key），所以仍需使用Global API Key

## Credits
本项目使用了提供的API接口来获取IPv6地址，万分感谢万分感谢，如果有冒犯请[联系我](mailto:zhousc11@icloud.com)删除。

另外使用了腾讯云的Python SDK，感谢腾讯云提供的服务。
另外使用了cloudflare的Python SDK，感谢cloudflare提供的服务。
