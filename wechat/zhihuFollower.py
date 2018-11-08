import requests


class SimpleCrawler:

    def crawl(self, params=None):
        # 必须指定UA，否则知乎服务器会判定请求不合法

        url = "https://www.zhihu.com/api/v4/columns/pythoneer/followers"
        n = 0
        while n < 110:
            # 查询参数
            params = {"limit": 10,
                      "offset": n,
                      "include": "data[*].follower_count, gender, is_followed, is_following"}

            headers = {
                "Host": "www.zhihu.com",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            }
            response = requests.get(url, headers=headers, params=params)
            n += 10
            print("请求URL：", response.url)
            # 你可以先将返回的响应数据打印出来，拷贝到 http://www.kjson.com/jsoneditor/ 分析其结构。
            print("返回数据：", response.text)

            # 解析返回的数据
            for follower in response.json().get("data"):
                print("返回跟随：", follower)


if __name__ == '__main__':
    SimpleCrawler().crawl()