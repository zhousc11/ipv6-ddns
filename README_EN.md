# IPv6 DDNS Repository

## Introduction
IPv6 is used more and more widely. In China mainland, it's very convenient to access remote desktop, NAS, homeassistant,etc. But the public IPv6 address assigned by ISP is usually dynamic.

Thus if we can write a mini program to run on the host with python. It can obtain the IPv6 address, then use the API provided by the domain name service provider to update the AAAA record. So we can access our services by domain.

Which is very convenient.

## To-do List
- [ ] Obtain the IPv6 address and save to a variable
- [ ] Get the domain name service provider's API
- [ ] Design a friendly user interface