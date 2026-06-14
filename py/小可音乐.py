# coding = utf-8
#!/usr/bin/python
import json
import sys
from base.spider import Spider
import requests
import os
import time
from urllib.parse import unquote

sys.path.append('..')

class Spider(Spider):
    def __init__(self):
        self.name = "小可音乐"
        self.host = 'http://music.xiaokeyinyue.cn'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.38.2401(0x2800265D) Process/tools WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
            'Referer': 'http://music.xiaokeyinyue.cn/mobile/',
            'Accept': 'application/json, text/plain, */*',
        }
        
        self.classes = [
            {'type_id': '1', 'type_name': '小可推荐串烧', 'vod_pic': '', 'vod_remarks': '68首'},
            {'type_id': '2', 'type_name': '小可VIP串烧', 'vod_pic': '', 'vod_remarks': '121首'},
            {'type_id': '3', 'type_name': '小可经典连版', 'vod_pic': '', 'vod_remarks': '168首'},
            {'type_id': '4', 'type_name': '经典单曲', 'vod_pic': '', 'vod_remarks': '99首'},
            {'type_id': '5', 'type_name': '中文单曲', 'vod_pic': '', 'vod_remarks': '628首'},
            {'type_id': '6', 'type_name': '英文单曲', 'vod_pic': '', 'vod_remarks': '543首'},
            {'type_id': '7', 'type_name': '纯净中文串烧', 'vod_pic': '', 'vod_remarks': '30首'},
            {'type_id': '8', 'type_name': '动感8D环绕', 'vod_pic': '', 'vod_remarks': '69首'},
        ]
        
        self.category_names = {
            '1': '小可推荐串烧',
            '2': '小可VIP串烧',
            '3': '小可经典连版',
            '4': '经典单曲',
            '5': '中文单曲',
            '6': '英文单曲',
            '7': '纯净中文串烧',
            '8': '动感8D环绕'
        }
    
    def getName(self):
        return self.name
    
    def init(self, extend=''):
        pass
    
    def homeContent(self, filter):
        result = {}
        classes = []
        for cls in self.classes:
            classes.append({
                'type_id': cls['type_id'],
                'type_name': cls['type_name']
            })
        
        result['class'] = classes
        result['filters'] = {}
        
        list_videos = self._get_category_videos('1', 1, 10)
        result['list'] = list_videos
        return result
    
    def homeVideoContent(self):
        return {'list': self._get_category_videos('1', 1, 10)}
    
    def _get_category_videos(self, tid, pg, limit=60):
        videos = []
        try:
            api_url = f'{self.host}/api/music/list'
            
            params = {
                'cateid': tid,
                'page_no': pg,
                'page_size': limit
            }
            
            response = self.fetch(api_url, params=params, headers=self.header)
            
            if not response or response.status_code != 200:
                return videos
            
            data = json.loads(response.text)
            
            if data.get('code') != 1:
                return videos
            
            list_data = data.get('data', {})
            items = list_data.get('list', [])
            
            items = items[:limit] if limit > 0 else items
            
            for item in items:
                title = item.get('title', '未知')
                singer = item.get('singer', '')
                
                video_data = {
                    'vod_id': f"{tid}_{item.get('id', '')}",
                    'vod_name': title,
                    'vod_pic': '',
                    'vod_remarks': f"🎵{singer}" if singer else ''
                }
                videos.append(video_data)
            
            return videos
            
        except Exception as e:
            print(f"获取视频列表失败: {e}")
            return videos
    
    def categoryContent(self, tid, pg, filter, extend):
        videos = []
        try:
            api_url = f'{self.host}/api/music/list'
            
            params = {
                'cateid': tid,
                'page_no': pg,
                'page_size': 60
            }
            
            response = self.fetch(api_url, params=params, headers=self.header)
            
            if not response or response.status_code != 200:
                return {
                    'list': [],
                    'page': int(pg),
                    'pagecount': 0,
                    'limit': 60,
                    'total': 0
                }
            
            data = json.loads(response.text)
            
            if data.get('code') != 1:
                return {
                    'list': [],
                    'page': int(pg),
                    'pagecount': 0,
                    'limit': 60,
                    'total': 0
                }
            
            list_data = data.get('data', {})
            items = list_data.get('list', [])
            more = list_data.get('more', 0)
            
            for item in items:
                title = item.get('title', '未知')
                singer = item.get('singer', '')
                
                video_data = {
                    'vod_id': f"{tid}_{item.get('id', '')}",
                    'vod_name': title,
                    'vod_pic': '',
                    'vod_remarks': f"🎵{singer}" if singer else ''
                }
                videos.append(video_data)
            
            # 根据more字段判断是否有更多页
            pagecount = int(pg) + 1 if more == 1 else int(pg)
            
            return {
                'list': videos,
                'page': int(pg),
                'pagecount': pagecount,
                'limit': 60,
                'total': len(videos) * int(pg)
            }
            
        except Exception as e:
            print(f"获取分类内容失败: {e}")
            return {
                'list': [],
                'page': int(pg),
                'pagecount': 0,
                'limit': 60,
                'total': 0
            }
    
    def detailContent(self, ids):
        try:
            vod_id = str(ids[0])
            parts = vod_id.split('_')
            if len(parts) >= 2:
                tid = parts[0]
                song_id = parts[1]
            else:
                return {'list': []}
            
            api_url = f'{self.host}/api/music/list'
            
            params = {
                'cateid': tid,
                'page_no': 1,
                'page_size': 100
            }
            
            response = self.fetch(api_url, params=params, headers=self.header)
            
            if not response or response.status_code != 200:
                return {'list': []}
            
            data = json.loads(response.text)
            
            if data.get('code') != 1:
                return {'list': []}
            
            list_data = data.get('data', {})
            items = list_data.get('list', [])
            
            video_info = None
            for item in items:
                if str(item.get('id', '')) == song_id:
                    video_info = item
                    break
            
            if not video_info:
                return {'list': []}
            
            music_url = video_info.get('url', '')
            if music_url:
                if music_url.startswith('/'):
                    music_url = 'http://static.xiaokeyinyue.cn' + music_url
                music_url = music_url.replace('/listen/music/', '/music/')
            
            title = video_info.get('title', '未知')
            singer = video_info.get('singer', '')
            
            video_detail = {
                'vod_id': vod_id,
                'vod_name': title,
                'vod_pic': '',
                'vod_remarks': f"🎵{singer}" if singer else '',
                'vod_content': f"分类: {self.category_names.get(tid, '')}\n歌手: {singer}",
                'vod_director': '',
                'vod_actor': singer,
                'vod_play_from': '小可音乐',
                'vod_play_url': f"{title}${music_url}"
            }
            
            return {'list': [video_detail]}
            
        except Exception as e:
            print(f"获取详情失败: {e}")
            return {'list': []}
    
    def searchContent(self, key, quick, pg=1):
        videos = []
        try:
            for cate_id in self.category_names.keys():
                api_url = f'{self.host}/api/music/list'
                
                params = {
                    'cateid': cate_id,
                    'page_no': pg,
                    'page_size': 50
                }
                
                response = self.fetch(api_url, params=params, headers=self.header)
                
                if not response or response.status_code != 200:
                    continue
                
                data = json.loads(response.text)
                
                if data.get('code') != 1:
                    continue
                
                list_data = data.get('data', {})
                items = list_data.get('list', [])
                
                for item in items:
                    title = item.get('title', '').lower()
                    singer = item.get('singer', '').lower()
                    
                    if key.lower() in title or key.lower() in singer:
                        song_title = item.get('title', '未知')
                        song_singer = item.get('singer', '')
                        
                        video_data = {
                            'vod_id': f"{cate_id}_{item.get('id', '')}",
                            'vod_name': song_title,
                            'vod_pic': '',
                            'vod_remarks': f"🎵{song_singer}" if song_singer else ''
                        }
                        videos.append(video_data)
            
            total = len(videos)
            pagecount = (total + 49) // 50 if total > 0 else 1
            
            return {
                'list': videos[:50],
                'page': int(pg),
                'pagecount': pagecount,
                'limit': 50,
                'total': total
            }
            
        except Exception as e:
            print(f"搜索失败: {e}")
            return {
                'list': [],
                'page': int(pg),
                'pagecount': 0,
                'limit': 50,
                'total': 0
            }
    
    def playerContent(self, flag, id, vipFlags):
        try:
            play_url = id
            
            if not play_url:
                return {
                    'parse': 0,
                    'playUrl': '',
                    'url': ''
                }
            
            return {
                'parse': 0,
                'playUrl': '',
                'url': play_url,
                'header': json.dumps({
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.38.2401(0x2800265D) Process/tools WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
                    'Referer': 'http://music.xiaokeyinyue.cn/mobile/'
                })
            }
            
        except Exception as e:
            print(f"播放解析失败: {e}")
            return {
                'parse': 0,
                'playUrl': '',
                'url': ''
            }
    
    def isVideoFormat(self, url):
        audio_formats = ['.mp3', '.m4a', '.wav', '.flac', '.aac']
        return any(url.lower().endswith(fmt) for fmt in audio_formats) or any(fmt in url.lower() for fmt in ['.mp3', '.m4a'])
    
    def manualVideoCheck(self):
        pass
    
    def localProxy(self, params):
        return None

if __name__ == '__main__':
    pass
