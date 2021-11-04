import json
import os
import random
import re
import time
import requests
from retrying import retry
import redis
import configparser
import sys
# 修改最大递归深度
sys.setrecursionlimit(10000)


class Instagram:
    def __init__(self):
        self.useragent = ""
        self.init_headers = {
            'authority': 'www.instagram.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': self.useragent,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cookie': 'rur="EAG\\05449520332153\\0541663318056:01f7978936c1263e414dde120e1ca89749516db0542c565b8c64233d4193a2551ea2c55f";sessionid=49520332153%3AdH8EQbXkukGpf3%3A23;csrftoken=boyS3BaGVulVPbULIJysXqPWMH0ASeBW;ig_nrcb=1;ds_user_id=49520332153;ig_did=DE42BFA8-8AE0-4A6B-95A2-A086E91FA86E;mid=YUMEmgALAAFX2YpyUGGjE5KTnaaM',
        }
        self.proxies = {
            "http": "http://127.0.0.1:1080",
            "https": "http://127.0.0.1:1080"
        }
        self.next_page = "https://www.instagram.com/graphql/query/"
        self.temp_data_path = r"D:\data\Ins"
        self.redis_conn = redis.StrictRedis(db=10, decode_responses=True)
        self.cookie_list = []
        self.next_headers = {
            'authority': 'www.instagram.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'x-asbd-id': '198387',
            'user-agent': self.useragent,
            'x-csrftoken': '',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': '',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cookie': 'mid=YUKq2AALAAGuezku2WENzHzaXYGR; ig_did=638ECA58-E851-4FE0-9626-B2539850099B; ig_nrcb=1; csrftoken=Xd6YowXF7OR0AGtvHejMTIxOySxYQcBq; ds_user_id=49159886430; sessionid=49159886430%3A6tY7PP66yzUMOT%3A24; rur="NAO\\05449159886430\\0541663327108:01f7b09a5eacd5268ccb0deb3ceea70a81a9ff1c5c6d46ba9c61d37649942e6aaba5057a"',
        }

    @retry()
    def downloader(self, url):
        response = requests.get(url=url, proxies=self.proxies)
        time.sleep(random.randint(2, 6))
        return response

    @retry()
    def get_response(self, url, headers):
        response = requests.get(url=url, headers=headers, proxies=self.proxies)
        time.sleep(random.randint(15, 25))
        return response

    @retry()
    def get_params_response(self, url, headers, params):
        response = requests.get(url=url, headers=headers, params=params, proxies=self.proxies)
        time.sleep(random.randint(15, 25))
        return response

    def download_single_pic(self, data, user_name):
        """单张图片下载"""
        try:
            display_resources = data['display_resources']
            pic_info = display_resources[-1]
            pic_src = pic_info['src']
        except KeyError:
            pic_src = data['display_url']
        pic_id = data['id']
        shortcode = data['shortcode']
        # 发布时间
        taken_at_timestamp = data['taken_at_timestamp']
        # 简介
        try:
            edge_media_to_caption = data['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError:
            edge_media_to_caption = ''
        # 点赞数
        edge_media_preview_like = data['edge_media_preview_like']['count']
        # 评论数
        edge_media_to_comment = data['edge_media_to_comment']['count']
        pic_path = self.temp_data_path + '\\' + user_name + '\\' + pic_id
        if not os.path.exists(pic_path):
            os.makedirs(pic_path)
        src_response = self.downloader(pic_src)
        open(pic_path + '\\' + f'{shortcode}.jpg', 'wb').write(src_response.content)
        info_dict = {
            "简介": edge_media_to_caption,
            "点赞数": edge_media_preview_like,
            "评论数": edge_media_to_comment,
            "发布时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(taken_at_timestamp))
        }
        print(info_dict)
        open(pic_path + '\\' + f'{shortcode}.json', 'w', encoding='utf8').write(json.dumps(info_dict, ensure_ascii=False))

    def download_multi_media(self, data, user_name):
        """多张图片下载"""
        edges = data['edge_sidecar_to_children']['edges']
        pic_id = data['id']
        shortcode = data['shortcode']
        # 发布时间
        taken_at_timestamp = data['taken_at_timestamp']
        try:
            edge_media_to_caption = data['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError:
            edge_media_to_caption = ''
        pic_path = self.temp_data_path + '\\' + user_name + '\\' + pic_id
        if not os.path.exists(pic_path):
            os.makedirs(pic_path)
        for index, edge in enumerate(edges):
            node = edge['node']
            try:
                display_resources = node['display_resources']
                pic_info = display_resources[-1]
                pic_src = pic_info['src']
            except KeyError:
                pic_src = node['display_url']
            src_response = self.downloader(pic_src)
            open(pic_path + '\\' + f'{shortcode + "_" + str(index)}.jpg', 'wb').write(src_response.content)
        # 点赞数
        edge_media_preview_like = data['edge_media_preview_like']['count']
        # 评论数
        edge_media_to_comment = data['edge_media_to_comment']['count']
        info_dict = {
            "简介": edge_media_to_caption,
            "点赞数": edge_media_preview_like,
            "评论数": edge_media_to_comment,
            "发布时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(taken_at_timestamp))
        }
        print(info_dict)
        open(pic_path + '\\' + f'{shortcode}.json', 'w', encoding='utf8').write(json.dumps(info_dict, ensure_ascii=False))

    def download_single_video(self, data, user_name):
        """视频格式文件下载"""
        video_url = data['video_url']
        video_id = data['id']
        shortcode = data['shortcode']
        # 发布时间
        taken_at_timestamp = data['taken_at_timestamp']
        # 简介
        try:
            edge_media_to_caption = data['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError:
            print(data['edge_media_to_caption'])
            edge_media_to_caption = ''
        video_resp = self.downloader(video_url)
        pic_path = self.temp_data_path + '\\' + user_name + '\\' + video_id
        if not os.path.exists(pic_path):
            os.makedirs(pic_path)
        # 播放量
        video_view_count = data['video_view_count']
        # 点赞数
        edge_media_preview_like = data['edge_media_preview_like']['count']
        # 评论数
        edge_media_to_comment = data['edge_media_to_comment']['count']
        info_dict = {
            "简介": edge_media_to_caption,
            "点赞数": edge_media_preview_like,
            "评论数": edge_media_to_comment,
            "播放量": video_view_count,
            "发布时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(taken_at_timestamp))
        }
        print(info_dict)
        open(pic_path + '\\' + f'{shortcode}.mp4', 'wb').write(video_resp.content)
        open(pic_path + '\\' + f'{shortcode}.json', 'w', encoding='utf8').write(json.dumps(info_dict, ensure_ascii=False))

    def extract_message(self, edges, user_name):
        for edge in edges:
            node = edge['node']
            media_info_type = node['__typename']
            if media_info_type == 'GraphSidecar':
                # todo 组图的数据提取方式
                self.download_multi_media(node, user_name)
            elif media_info_type == 'GraphImage':
                # todo  单图的数据提取
                self.download_single_pic(node, user_name)
            else:
                # todo 视频的提取方式
                self.download_single_video(node, user_name)

    def extract_user_info(self, user, info):
        # 粉丝数
        fans_count = user['edge_followed_by']['count']
        # 关注数
        edge_follow = user['edge_follow']['count']
        # 帖子数
        edge_count = user['edge_owner_to_timeline_media']['count']
        # 用户名
        user_name = user['username']
        # 用户头像
        user_pic = user['profile_pic_url_hd']
        user_info = {
            "账号名称": info['posts_user'],
            "主页链接": info['posts_url'],
            "风格": info['posts_style'],
            "性别": info['posts_sex'],
            "备注": info['posts_remarks'],
            "帖子数": edge_count,
            "关注数": edge_follow,
            "粉丝数": fans_count
        }
        print(user_info)
        # 用户头像下载
        user_path = self.temp_data_path + '\\' + user_name
        if not os.path.exists(user_path):
            os.makedirs(user_path)
        src_response = self.downloader(user_pic)
        open(user_path + '\\' + f'{user_name}.jpg', 'wb').write(src_response.content)
        # 用户基本信息 json
        open(user_path + '\\' + f'{user_name}.json', 'w', encoding='utf8').write(
            json.dumps(user_info, ensure_ascii=False))

    def get_next_page(self, user_id, end_cursor, user_name):
        """
        获取下一页数据 使用了递归
        :param user_id:
        :param end_cursor:
        :param user_name:
        :return:
        """
        params = {
            "query_hash": "8c2a529969ee035a5063f2fc8602a0fd",
            "variables": '{"id":"%s","first":12,"after":"%s"}' % (user_id, end_cursor)
        }
        old_cookie = random.choice(self.cookie_list)
        cookie = old_cookie.replace('\\\\', "\\")
        csrf_token = re.findall('csrftoken=(.*?);', cookie)
        self.next_headers['x-csrftoken'] = csrf_token[0]
        self.next_headers['cookie'] = cookie
        response = self.get_params_response(url=self.next_page, headers=self.next_headers, params=params)
        resp_cookie = ';'.join(response.raw.headers.getlist('Set-Cookie'))
        rur = re.findall('(rur=.*?);', resp_cookie, re.S)[0].replace('\\', "\\\\")
        old_cookie = random.choice(self.cookie_list)
        cookie = old_cookie.replace('\\\\', "\\")
        new_cookie = re.sub('(rur=.*?);', rur + ';', cookie)
        cookie_index = self.cookie_list.index(old_cookie)
        self.cookie_list[cookie_index] = new_cookie
        json_resp = response.json()
        user = json_resp['data']['user']
        end_cursor = user['edge_owner_to_timeline_media']['page_info']['end_cursor']  # 下一页的翻页数据
        edges = user['edge_owner_to_timeline_media']['edges']  # 这是页面数据 也就是每一个发布的id
        self.extract_message(edges, user_name)
        if end_cursor:
            self.get_next_page(user_id, end_cursor, user_name)

    def get_first_page(self, info):
        """
        第一页发布的帖子数据展示
        :param info:  基础已经提供的数据
        :return:
        """
        posts_url = info['posts_url']
        old_cookie = random.choice(self.cookie_list)
        cookie = old_cookie.replace('\\\\', "\\")
        self.init_headers['cookie'] = cookie
        response = self.get_response(posts_url, self.init_headers)
        resp_cookie = ';'.join(response.raw.headers.getlist('Set-Cookie'))
        rur = re.findall('(rur=.*?);', resp_cookie, re.S)[0].replace('\\', "\\\\")
        new_cookie = re.sub('(rur=.*?);', rur+';', cookie)
        cookie_index = self.cookie_list.index(old_cookie)
        self.cookie_list[cookie_index] = new_cookie
        self.next_headers['referer'] = posts_url   # 修改referer
        result = re.findall("window._sharedData = (.*?);</script>", response.content.decode(), re.S)
        result_json = json.loads(result[0])
        try:
            user = result_json['entry_data']['ProfilePage'][0]['graphql']['user']
        except KeyError:
            result = re.findall("window.__additionalDataLoaded\((.*?)\);</script>", response.content.decode(), re.S)
            result_json = json.loads(','.join(result[0].split(",")[1:]))
            user = result_json['graphql']['user']
        #  提取用户数据
        self.extract_user_info(user, info)
        # 用户名
        user_name = user['username']
        # 用户id
        user_id = user['id']
        end_cursor = user['edge_owner_to_timeline_media']['page_info']['end_cursor']  # 下一页的翻页数据
        edges = user['edge_owner_to_timeline_media']['edges']  # 这是页面数据 也就是每一个发布的id
        if edges:
            # 数据提取模块
            self.extract_message(edges, user_name)
        else:
            print(user_name + '  该用户需要关注才能采集数据  ')
            return
        # 翻页逻辑
        self.get_next_page(user_id, end_cursor, user_name)

    def start_spider(self):
        
        self.get_first_page({"posts_user": "twistflip", "posts_url": "https://www.instagram.com/twistflip/", "posts_style": "男，休闲", "posts_sex": "男", "posts_remarks": ""})
        # while True:
        #     result = self.redis_conn.spop("ins_posts")
        #     if result:
        #         result_info = json.loads(result)
        #         self.get_first_page(result_info)
        #     else:
        #         break

    def get_cookie_ua(self):
        #  获取当前配置文件的路径
        cur_path = os.path.dirname(os.path.realpath(__file__))
        cfg_path = os.path.join(cur_path, "ins.ini")
        # 读取当前的配置文件
        conf = configparser.RawConfigParser()
        conf.read(cfg_path, encoding="utf-8")
        try:
            parameter = sys.argv[1]
        except IndexError:
            parameter = "1"
        cookie_index = "cookie_" + parameter
        # 读取cookie
        try:
            cookie = conf['Cookies'][cookie_index]
        except KeyError:
            cookie = conf['Cookies']["cookie_1"]
        self.cookie_list.append(cookie)
        ua_index = "ua_" + parameter
        try:
            ua = conf['UserAgent'][ua_index]
        except KeyError:
            ua = conf['UserAgent']['ua_1']
        self.useragent = ua

    def run(self):
        self.get_cookie_ua()
        self.start_spider()


if __name__ == '__main__':
    Instagram().run()
