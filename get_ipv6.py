import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
}


def get_ipv6():
    req_url = 'https://6.ipw.cn'
    try:
        response = requests.get(req_url, timeout=10, headers=headers, verify=False)
    except requests.exceptions.RequestException as e:
        return None

    if response.status_code == 200:
        return response.text, response.headers['content-type']
    else:
        return None


if __name__ == '__main__':
    # print(get_ipv6())
    content_type = get_ipv6()[1]
    body = get_ipv6()[0]
    print(content_type)
    print(body)
