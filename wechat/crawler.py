# -*- coding: utf-8 -*-

import requests
import zlib
import chardet
import urllib


def crawl():
    # url中的参数需要根据自己的情况做调整
    url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzUxMTM2NTI0OA==&scene=126&devicetype=iOS12.0&version=16070228&lang=en&nettype=WIFI&a8scene=0&fontScale=100&pass_ticket=L4DL95MXgHjvCNuX%2FNlrWu5qc1R0mpX9UfHkXirDRRRVxhOm5Q1IeFdn35wDisfS&wx_header=1"
    headers = """
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: br, gzip, deflate
X-WECHAT-KEY: c6731e19fc9aa088a26ef5ddd65f38a4d33cd2e73c9b563316b7e92b3ad7a122af5d18f5013355db5c4b33d724b0352b699c2e26ccc6b64236d9756c8aa7e5d4a8bb79c8e819169a020fe9404cbd54f8
X-WECHAT-UIN: MjcyNTI1MTkxMw%3D%3D
Accept-Language: en-US,en;q=0.9,zh-CN;
Connection: keep-alive
Cookie: devicetype=iOS12.0; lang=en; pass_ticket=L4DL95MXgHjvCNuX/NlrWu5qc1R0mpX9UfHkXirDRRRVxhOm5Q1IeFdn35wDisfS; version=16070228; wap_sid2=CMmWwJMKEnBKbmtmNVl6ZWVpQ2pZdVFXZjM5VXBQQVJTeDN0ZTZiMnJkc0p0VUhHdkFhTjlqTjk3ZlpMb1NGV2pSSFVmeW02bjNSMGtXWWRvbGpERGFBbFFJUXpBakJ1RGRJNkpVQ2h1WW96MlhORDNJZlNBd0FBMMKOiN4FOA1AlU4=; wxuin=2725251913; wxtokenkey=777; rewardsn=; pgv_pvid=6628091792; pgv_pvi=3294419968; sd_cookie_crttime=1523715187068; sd_userid=60371523715187068
Host: mp.weixin.qq.com
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.2 NetType/WIFI Language/en
    """
    headers = headers_to_dict(headers)
    print(headers)
    response = requests.get(url, headers=headers, verify=False)
    print(response.text)

    with open("weixin_history_all.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    if '<title>验证</title>' in response.text:
        raise Exception("获取微信公众号文章失败，可能是因为你的请求参数有误，请重新获取")
    data = extract_data(response.text)
    for item in data:
        print(item)


def extract_data(html_content):
    """
    从html页面中提取历史文章数据
    :param html_content 页面源代码
    :return: 历史文章列表
    """
    import re
    import html
    import json

    rex = "msgList = '({.*?})'"
    pattern = re.compile(pattern=rex, flags=re.S)
    match = pattern.search(html_content)
    if match:
        data = match.group(1)
        data = html.unescape(data)
        data = json.loads(data)
        articles = data.get("list")
        for item in articles:
            print(item)
        return articles


def headers_to_dict(headers):
    """
    将字符串
    '''
    Host: mp.weixin.qq.com
    Connection: keep-alive
    Cache-Control: max-age=
    '''
    转换成字典类型
    :param headers: str
    :return: dict
    """
    headers = headers.split("\n")
    d_headers = dict()
    for h in headers:
        h = h.strip()
        if h:
            k, v = h.split(":", 1)
            d_headers[k] = v.strip()
    return d_headers


if __name__ == '__main__':
    crawl()