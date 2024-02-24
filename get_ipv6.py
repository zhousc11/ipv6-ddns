import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
}


def get_ipv6():
    req_url = 'https://6.ipw.cn'
    try:
        response = requests.get(req_url, timeout=10, headers=headers, verify=False)
        response.raise_for_status()  # raise error when status code is not 200
        return response.text
    except requests.exceptions.HTTPError as e:
        print(f'HTTPError: {e}')
    except requests.exceptions.ConnectionError as e:
        print(f'ConnectionError: {e}')
    except requests.exceptions.Timeout as e:
        print(f'Timeout: {e}')
    except requests.exceptions.RequestException as e:
        print(f'RequestException: {e}')
    return None


if __name__ == '__main__':
    result = get_ipv6()
    if result:
        print(result)
    else:
        print('Failed to get IPv6 address')
