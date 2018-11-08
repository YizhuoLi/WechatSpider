import requests

def headers_to_dict(headers):
    """
    将字符串
    '''
    Host: mp.weixin.qq.com
    Connection: keep-alive
    Cache-Control: max-age=
    '''
    转换成字典对象
    {
        "Host": "mp.weixin.qq.com",
        "Connection": "keep-alive",
        "Cache-Control":"max-age="
    }
    :param headers: str
    :return: dict
    """
    headers = headers.split("\n")
    d_headers = dict()
    for h in headers:
        if h:
            k, v = h.split(":", 1)
            d_headers[k] = v.strip()
    return d_headers

# v0.1
def crawl():
    url = "https://mp.weixin.qq.com/mp/appmsgreport?action=page_time&__" \
          "biz=MzA5MDUwNzcxOA==&uin=777&key=777&pass_ticket=Qja16oMjzLyPI7G" \
          "A2fYyjw%25252Bz6ddRZf1FGgL0x2x9LGcaOIuX2fX%25252FeXSwJcQPmbLV&wxtok" \
          "en=777&devicetype=iOS12.0&clientversion=16070228&appmsg_token=978_zWA" \
          "ZzfyLLyp9jMTahw5kyBZ7DNlL78EimXvlwDajQQj5GOEvWSn9_JeGGoNCSxJdWwnovZRDHv" \
          "hnV5Tb&x5=0&f=json"

    headers = "Host: mp.weixin.qq.com" \
              "Connection: keep-alive" \
              "Upgrade-Insecure-Requests: 1" \
              "UserAgent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.2 NetType/WIFI Language/en"
    headers = headers_to_dict(headers)
    response = requests.get(url, headers=headers, verify=False)
    print(response.text)

    with open("weixin_history.html", "w", encoding="utf-8") as f:
        f.write(response.text)

crawl()