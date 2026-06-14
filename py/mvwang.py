#coding=utf-8
from base.spider import Spider
import re
import urllib.parse

class Spider(Spider):
    def __init__(self):
        self.host = "http://www.whwhd.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        # 分类映射 - 修正为网站实际使用的路径
        self.typeMap = {
            "dianying": "电影",
            "dianshiju": "电视剧",
            "zongyi": "综艺",
            "dongman": "动漫",
            "juqing": "剧情",
            "dongzuo": "动作片",
            "xiju": "喜剧片",
            "aiqing": "爱情片",
            "kehuan": "科幻片",
            "kongbu": "恐怖片",
            "zhanzheng": "战争片"
        }

    def getName(self):
        return "万宏达影院"

    def init(self, extend=""):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {}
        classes = []
        for k, v in self.typeMap.items():
            classes.append({
                'type_name': v,
                'type_id': k
            })
        result['class'] = classes
        return result

    def homeVideoContent(self):
        # 可以返回首页推荐，如果没有就返回空
        return {'list': []}

    def categoryContent(self, tid, pg, filter, extend):
        result = {}
        
        # 修正：使用网站实际的分类页URL格式
        if pg == 1:
            url = f"{self.host}/type/{tid}.html"
        else:
            url = f"{self.host}/type/{tid}-{pg}.html"
        
        # 获取页面内容
        html = self.fetch(url, headers=self.headers)
        
        # 解析视频列表 - 从实际页面中提取
        videos = []
        # 匹配常见的列表项结构，可能需要根据实际页面微调
        pattern = r'<li[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>\s*<img[^>]*src="([^"]+)"[^>]*alt="([^"]+)"[^>]*>.*?<span[^>]*class="[^"]*remark[^"]*"[^>]*>([^<]+)</span>'
        items = re.findall(pattern, html, re.S)
        
        if not items:
            # 备选匹配模式
            pattern2 = r'<div[^>]*class="[^"]*movie-item[^"]*"[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*title="([^"]+)"[^>]*>.*?<img[^>]*src="([^"]+)"[^>]*>.*?<div[^>]*class="[^"]*remarks?[^"]*"[^>]*>([^<]+)</div>'
            items = re.findall(pattern2, html, re.S)
        
        for item in items:
            # 根据不同的匹配结果调整索引
            if len(item) >= 4:
                detail_url = item[0]
                if not detail_url.startswith("http"):
                    detail_url = self.host + detail_url
                
                # 尝试获取标题
                title = item[2] if len(item) > 2 else ""
                if not title and len(item) > 1:
                    title = item[1]
                
                # 图片
                img_url = item[1] if len(item) > 1 else ""
                if img_url and not img_url.startswith("http"):
                    img_url = self.host + img_url
                
                # 备注（如HD、更新到第几集）
                remark = item[3] if len(item) > 3 else ""
                
                videos.append({
                    "vod_id": detail_url,
                    "vod_name": title,
                    "vod_pic": img_url,
                    "vod_remarks": remark
                })
        
        # 判断是否有下一页
        next_pattern = r'<a[^>]*href="([^"]+)"[^>]*>下一页</a>'
        next_page = re.findall(next_pattern, html)
        has_next = len(next_page) > 0
        
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999 if has_next else pg
        result['limit'] = 24
        result['total'] = 999999
        
        return result

    def detailContent(self, ids):
        if isinstance(ids, list):
            url = ids[0]
        else:
            url = ids
        
        # 获取详情页HTML
        html = self.fetch(url, headers=self.headers)
        
        # 提取基本信息
        name = ""
        name_pattern = r'<h1[^>]*>(.*?)</h1>'
        name_match = re.search(name_pattern, html)
        if name_match:
            name = name_match.group(1).strip()
        
        pic = ""
        pic_pattern = r'<img[^>]*class="[^"]*lazyload[^"]*"[^>]*src="([^"]+)"'
        pic_match = re.search(pic_pattern, html)
        if pic_match:
            pic = pic_match.group(1)
            if not pic.startswith("http"):
                pic = self.host + pic
        
        # 提取信息项
        type_name = ""
        area = ""
        year = ""
        actor = ""
        director = ""
        description = ""
        
        # 匹配"主演"等信息
        info_pattern = r'<span[^>]*class="[^"]*text-muted[^"]*"[^>]*>([^<]+)：</span>([^<]+)'
        info_items = re.findall(info_pattern, html)
        
        for key, value in info_items:
            key = key.strip()
            value = value.strip()
            if "分类" in key or "类型" in key:
                type_name = value
            elif "地区" in key:
                area = value
            elif "年份" in key:
                year = value
            elif "主演" in key:
                actor = value
            elif "导演" in key:
                director = value
        
        # 提取简介
        desc_pattern = r'<span[^>]*class="[^"]*detail-content[^"]*"[^>]*>(.*?)</span>'
        desc_match = re.search(desc_pattern, html, re.S)
        if desc_match:
            description = desc_match.group(1).strip()
            description = re.sub(r'<[^>]+>', '', description)
        
        # 提取播放列表
        play_urls = []
        play_pattern = r'<div[^>]*class="[^"]*play-btn[^"]*"[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
        plays = re.findall(play_pattern, html, re.S)
        
        for play_url, play_name in plays:
            if play_url.startswith("http"):
                full_url = play_url
            else:
                full_url = self.host + play_url
            play_urls.append(f"{play_name}${full_url}")
        
        vod = {
            "vod_id": url,
            "vod_name": name,
            "vod_pic": pic,
            "type_name": type_name,
            "vod_year": year,
            "vod_area": area,
            "vod_actor": actor,
            "vod_director": director,
            "vod_content": description,
            "vod_play_from": "万宏达云",
            "vod_play_url": "#".join(play_urls)
        }
        
        result = {'list': [vod]}
        return result

    def searchContent(self, key, quick):
        encoded_key = urllib.parse.quote(key)
        url = f"{self.host}/vodsearch/-------------.html?wd={encoded_key}"
        
        html = self.fetch(url, headers=self.headers)
        
        # 搜索结果解析，复用categoryContent中的解析逻辑
        videos = []
        pattern = r'<li[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>\s*<img[^>]*src="([^"]+)"[^>]*alt="([^"]+)"[^>]*>.*?<span[^>]*class="[^"]*remark[^"]*"[^>]*>([^<]+)</span>'
        items = re.findall(pattern, html, re.S)
        
        for item in items:
            detail_url = item[0]
            if not detail_url.startswith("http"):
                detail_url = self.host + detail_url
            
            videos.append({
                "vod_id": detail_url,
                "vod_name": item[2],
                "vod_pic": item[1] if item[1].startswith("http") else self.host + item[1],
                "vod_remarks": item[3]
            })
        
        return {'list': videos}

    def playerContent(self, flag, id, vipFlags):
        result = {}
        
        # 获取播放页面HTML
        html = self.fetch(id, headers=self.headers)
        video_url = ""
        
        # 尝试提取iframe
        iframe_pattern = r'<iframe.*?src="([^"]+)".*?>'
        iframes = re.findall(iframe_pattern, html)
        
        if iframes:
            iframe_url = iframes[0]
            if not iframe_url.startswith("http"):
                iframe_url = self.host + iframe_url
            
            iframe_html = self.fetch(iframe_url, headers=self.headers)
            
            # 从iframe中提取视频URL
            video_pattern = r'<video.*?src="([^"]+)".*?>'
            videos = re.findall(video_pattern, iframe_html)
            if videos:
                video_url = videos[0]
            
            if not video_url:
                # 尝试js变量
                js_pattern = r'url["\']?\s*[:=]\s*["\']([^"\']+)["\']'
                js_urls = re.findall(js_pattern, iframe_html)
                if js_urls:
                    video_url = js_urls[0]
        
        # 直接提取video
        if not video_url:
            video_pattern = r'<video.*?src="([^"]+)".*?>'
            videos = re.findall(video_pattern, html)
            if videos:
                video_url = videos[0]
        
        result["parse"] = 0 if video_url else 1
        result["playUrl"] = ""
        result["url"] = video_url if video_url else id
        result["header"] = self.headers
        
        return result

    def fetch(self, url, headers=None, data=None):
        import requests
        
        if headers is None:
            headers = self.headers
        
        try:
            if data:
                response = requests.post(url, headers=headers, data=data, timeout=10)
            else:
                response = requests.get(url, headers=headers, timeout=10)
            
            response.encoding = 'utf-8'
            return response.text
        except:
            return ""

    def post(self, url, data, headers=None):
        return self.fetch(url, headers=headers, data=data)

    def localProxy(self, param):
        return [200, "video/MP2T", "", ""]