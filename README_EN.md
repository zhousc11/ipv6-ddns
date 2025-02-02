# IPv6 DDNS Repository

EN|[简中](./README.md)

## Introduction
IPv6 is used more and more widely. In China mainland, it's very convenient to access remote desktop, NAS, homeassistant,etc. But the public IPv6 address assigned by ISP is usually dynamic.

Thus if we can write a mini program to run on the host with python. It can obtain the IPv6 address, then use the API provided by the domain name service provider to update the AAAA record. So we can access our services by domain.

Which is very convenient.

> Now only support dnspod's API, will support more domain name service provider's API in the future (if I have time)
## To-Do List
- [x] Fetch the IPv6 address and store it in a variable
- [x] Obtain the API from the domain service provider
- [ ] Develop a functional GUI (+ add a user guide)
- [ ] Review API documentation from other domain registrars for broader compatibility (+ added Cloudflare support)

## Prerequisites
- Requires a Python environment to run
- Before using, ensure you've already created an AAAA record for your domain

## Usage

1. Clone the source code:
    ```shell
    git clone https://github.com/zhousc11/ipv6-ddns.git
    ```
2. Navigate to the directory:
    ```shell
    cd ipv6-ddns
    ```
3. Run the installation wizard:
    ```shell
    python3 InstallWizard.py
    ```
> **Note:** Windows and Linux support automatic addition of scheduled tasks. For other systems, please add them manually.

> **Domain** refers to the domain hosted by your DNS service provider. For example, if you delegate `ddns.example.com` to Dnspod using NS records, then `ddns.example.com` is your Domain. If you're pointing your DNS servers to Cloudflare to host `example.com`, then `example.com` is your Domain.

> **Subdomain** is the host record added at your DNS service provider. For instance, if you host `ddns.example.com` on Dnspod and use `ipv6.ddns.example.com` to point to your local IPv6 address, then `ipv6` is your Subdomain. If you're hosting `example.com` on Cloudflare and use `ipv6.ddns.example.com` to point to your local IPv6 address, then `ipv6.ddns` is your Subdomain.

> **Important:** Directly using the Domain to point to your local IPv6 address isn't supported yet. So, please avoid leaving the Subdomain field empty or entering `@`, as this will cause errors.

Feel free to open issues and pull requests. Thanks for your support!

## API Token Configuration

- **Tencent Cloud Dnspod**
    > **Note:** Tencent Cloud refers to `cloud.tencent.com`, not `tencentcloud.com`.

    1. Navigate to [Tencent Cloud CAM](https://console.cloud.tencent.com/cam) and create a new sub-user.
    2. Quick Create -> Access Method: Programmatic Access, User Permissions: Policy - `QcloudDNSPodFullAccess` -> Save the `SecretId` and `SecretKey`.
    > If you lose your `SecretId` or `SecretKey`, go to [Tencent Cloud CAM](https://console.cloud.tencent.com/cam) -> User Details -> API Keys to create new ones.
    > Each sub-user is limited to a maximum of 2 pairs of keys.
    > The [DnspodToken](https://console.dnspod.cn/account/token/token) is no longer available.

- **Cloudflare**
    - Navigate to [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens) -> API Keys -> Global API Key, then view and save it.
    > API Tokens can't be used with the required APIs: [Update DNS Record](https://developers.cloudflare.com/api/construct-a-request/dns-records/update-dns-record) and [List DNS Records](https://developers.cloudflare.com/api/construct-a-request/dns-records/list-dns-records) (Security: API Email + API Key). Therefore, the Global API Key is still needed.

## Credits
This project utilizes provided API interfaces to obtain the IPv6 address—we're immensely grateful. If there's any issue, please [contact me](mailto:zhousc11@icloud.com) for removal.

We also used Tencent Cloud's Python SDK—thanks to Tencent Cloud for their excellent services.
Additionally, we leveraged Cloudflare's Python SDK—appreciate Cloudflare for providing such powerful tools.
