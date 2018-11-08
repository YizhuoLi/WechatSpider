# -*- coding: utf-8 -*-

import json
import logging
import time
from datetime import datetime

import requests

import wechat.utils
from wechat.models import Post

requests.urllib3.disable_warnings()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class WeiXinCrawler:
    def crawl(self, n=0):
        """
        爬取更多文章
        :return:
        """


        url = "https://mp.weixin.qq.com/mp/profile_ext?" \
              "action=getmsg&" \
              "__biz=MzUxMTM2NTI0OA==&" \
              "f=json&" \
              "offset="+str(n)+"&" \
              "count=10&is_ok=1&scene=126&uin=777&key=777&" \
              "pass_ticket=3ZDhqdzS%2BiKkazaSxjXmZIQwjNzlkGBtLRQn91OnGb1Ro4umo694euGsno3z0JCl&" \
              "wxtoken=&" \
              "appmsg_token=978_LuSLYc%252BxacTshXEaYnGGcdtQ3acNaMKwI3NSUw~~&x5=0&" \
              "f=json"  # appmsg_token 也是临时的

        headers = """
Host: mp.weixin.qq.com
Accept-Encoding: br, gzip, deflate
Cookie: devicetype=iOS12.0; lang=en; pass_ticket=3ZDhqdzS+iKkazaSxjXmZIQwjNzlkGBtLRQn91OnGb1Ro4umo694euGsno3z0JCl; version=16070228; wap_sid2=CMmWwJMKElxBc2ZrcWRUQUhMMHc1amV4YXF5RUE2cEFscDBIWGhucm0tdmcxUTh6RGZUV0lwYnl5SEk3MnhBS3M5Q0llSE5FQjY3NGFQYlZJa05idmc4V3FOVllFdElEQUFBfjCB5I7eBTgNQJVO; wxuin=2725251913; pgv_pvid=6628091792; pgv_pvi=3294419968; sd_cookie_crttime=1523715187068; sd_userid=60371523715187068
Connection: keep-alive
Accept: */*
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.2 NetType/WIFI Language/en
Referer: https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzUxMTM2NTI0OA==&scene=126&devicetype=iOS12.0&version=16070228&lang=en&nettype=WIFI&a8scene=0&fontScale=100&pass_ticket=3ZDhqdzS%2BiKkazaSxjXmZIQwjNzlkGBtLRQn91OnGb1Ro4umo694euGsno3z0JCl&wx_header=1
Accept-Language: zh-cn
X-Requested-With: XMLHttpRequest
"""
        headers = wechat.utils.str_to_dict(headers)
        response = requests.get(url, headers=headers, verify=False)
        result = response.json()
        if result.get("ret") == 0:
            msg_list = result.get("general_msg_list")
            logger.info("抓取数据：offset=%s, data=%s" % (n, msg_list))
            self.save(msg_list)
            # 递归调用
            has_next = result.get("can_msg_continue")
            print(has_next)
            if has_next == 1:
                n += 10
                print(n)
                time.sleep(2)
                self.crawl(n)
        else:
            # 错误消息
            # {"ret":-3,"errmsg":"no session","cookie_count":1}
            logger.error("无法正确获取内容，请重新从Fiddler获取请求参数和请求头")
            exit()


    @staticmethod
    def save(msg_list):

        msg_list = msg_list.replace("\/", "/")
        data = json.loads(msg_list)
        msg_list = data.get("list")
        for msg in msg_list:
            p_date = msg.get("comm_msg_info").get("datetime")
            msg_info = msg.get("app_msg_ext_info")  # 非图文消息没有此字段
            if msg_info:
                WeiXinCrawler._insert(msg_info, p_date)
                multi_msg_info = msg_info.get("multi_app_msg_item_list")
                for msg_item in multi_msg_info:
                    WeiXinCrawler._insert(msg_item, p_date)
            else:
                logger.warning(u"此消息不是图文推送，data=%s" % json.dumps(msg.get("comm_msg_info")))

    @staticmethod
    def _insert(item, p_date):
        keys = ('title', 'author', 'content_url', 'digest', 'cover', 'source_url')
        sub_data = wechat.utils.sub_dict(item, keys)
        post = Post(**sub_data)
        p_date = datetime.fromtimestamp(p_date)
        post["p_date"] = p_date
        logger.info('save data %s ' % post.title)
        try:
            post.save()
        except Exception as e:
            logger.error("保存失败 data=%s" % post.to_json(), exc_info=True)

    def update(self, post):

        post_url_params = {'__biz': 'MzUxMTM2NTI0OA==',
                           'mid': '2247486952',
                           'idx': '1',
                           'sn': '7e37a9967d3bbd2f7cc32b17e85868d3',
                           'chksm': 'f9759407ce021d117e4e53fe247075e63cda5595d496a425664b64b5a37571cf2e1ba4b1966c',
                           'scene': '27'}


        url_params = {
            'f': 'json', 'mock': '', 'uin': '777', 'key': '777',
            'pass_ticket': 'fakFRtpDP9lnqkxa9Mf3VhRNtrSsKTOWxdfSl1aYTX4S%2BEGqxB3DKns7sdFfi268',
            'wxtoken': '777', 'devicetype': 'iOS12.0', 'clientversion': '16070228',
            'appmsg_token': '978_VLXLxsD7VALwmk8t1sQ_JAmJUp1APxourWaH7AmRKeNt3EVHspKERH4MaxDGMZbLMRlx15IqWjo1Nh6',
            'x5': '0', '__biz': 'MzUxMTM2NTI0OA==', 'mid': '2247486952', 'idx': '1',
            'sn': '7e37a9967d3bbd2f7cc32b17e85868d3',
            'chksm': 'f9759407ce021d117e4e53fe247075e63cda5595d496a425664b64b5a37571cf2e1ba4b1966c', 'scene': '27'}

        from urllib.parse import urlsplit
        import html
        url_params.update(wechat.utils.str_to_dict(urlsplit(html.unescape(post.content_url)).query, "&", "="))
        body = "r=0.03640379980668673&appmsg_type=9&title=90%25E5%2590%258E%25E7%259A%2584%25E6%2588%25BF%25E4%25BA%258B%25EF%25BC%258C%25E4%25B8%258D%25E5%25A0%25AA%25E5%2585%25A5%25E7%259B%25AE&ct=1524040278&abtest_cookie=BAABAAoACwASABMABAAjlx4AT5keAFmZHgBgmR4AAAA%3D&devicetype=iOS12.0&version=16070228&is_need_ticket=0&is_need_ad=0&comment_id=242397342077059072&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=1506Kog1sC8URwU176nFiDFL&pass_ticket=3ZDhqdzS%25252BiKkazaSxjXmZIQwjNzlkGBtLRQn91OnGb1Ro4umo694euGsno3z0JCl&is_temp_url=0&item_show_type=undefined&tmp_version=1"
        data = wechat.utils.str_to_dict(body, "&", "=")

        headers = """

Host: mp.weixin.qq.com
Connection: keep-alive
Content-Length: 774
Origin: https://mp.weixin.qq.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.2 NetType/WIFI Language/en
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Accept: */*
Referer: https://mp.weixin.qq.com/s?__biz=MzUxMTM2NTI0OA==&mid=2247486012&idx=1&sn=d413a5fd219d0ae108c8b19587431cd0&chksm=f97593d3ce021ac5de8deece853c581bcd0be7b1196ed0418add09be34a98cd8ed3780872ece&scene=4&subscene=126&ascene=0&devicetype=iOS12.0&version=16070228&nettype=WIFI&abtest_cookie=BAABAAoACwASABMABAAjlx4AT5keAFmZHgBgmR4AAAA%3D&lang=en&fontScale=100&pass_ticket=3ZDhqdzS%2BiKkazaSxjXmZIQwjNzlkGBtLRQn91OnGb1Ro4umo694euGsno3z0JCl&wx_header=1
Accept-Encoding: br, gzip, deflate
Accept-Language: zh-CN,en-US;q=0.8
Cookie: wxtokenkey=777; devicetype=iOS12.0; lang=en; pass_ticket=3ZDhqdzS+iKkazaSxjXmZIQwjNzlkGBtLRQn91OnGb1Ro4umo694euGsno3z0JCl; rewardsn=; version=16070228; wap_sid2=CMmWwJMKElxOWUpXUUxyNTd3V2Y3ZERXcm02MHJOWC1tRW9GV0psY3oxX2VTR1pnNE83MU81Qmx5S3NmQkc5RWpmVmZqSEFYbVZWNDlKSXlkblJpRkZFN1AxRlN0ZElEQUFBfjCDjI/eBTgNQAE=; wxuin=2725251913; pgv_pvid=6628091792; pgv_pvi=3294419968; sd_cookie_crttime=1523715187068; sd_userid=60371523715187068
        """

        headers = wechat.utils.str_to_dict(headers)

        url = "https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=777&key=777&pass_ticket=3ZDhqdzS%25252BiKkazaSxjXmZIQwjNzlkGBtLRQn91OnGb1Ro4umo694euGsno3z0JCl&wxtoken=777&devicetype=iOS12.0&clientversion=16070228&appmsg_token=978_pzPMyITn835C0afgpKXYG7KekHMFn69jcY5pHAVyVbazlVIRdo8vEykZjvpyd9tXXnbWDRLJerMq7yMS&x5=0&f=json"
        r = requests.post(url, data=data, verify=False, params=url_params, headers=headers)

        result = r.json()
        if result.get("appmsgstat"):
            post['read_num'] = result.get("appmsgstat").get("read_num")
            post['like_num'] = result.get("appmsgstat").get("like_num")
            post['reward_num'] = result.get("reward_total_count")
            post['comment_num'] = result.get("comment_count")
            post['u_date'] = datetime.now()
            logger.info("「%s」read_num: %s like_num: %s reward_num: %s comment_num: %s" %
                        (post.title, post['read_num'], post['like_num'], post['reward_num'], post['comment_num']))
            post.save()
        else:
            logger.warning(u"没有获取的真实数据，请检查请求参数是否正确，data=%s" % r.text)


if __name__ == '__main__':
    # 直接运行这份代码很定或报错，或者根本抓不到数据
    # 因为header里面的cookie信息已经过去，还有URL中的appmsg_token也已经过期
    # 你需要配合Fiddler或者charles通过手机重新加载微信公众号的更多历史消息
    # 从中获取最新的headers和appmsg_token替换上面
    crawler = WeiXinCrawler()
    # crawler.crawl()
    for post in Post.objects(read_num=0):
        crawler.update(post)
        time.sleep(1)