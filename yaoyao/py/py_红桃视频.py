# coding=utf-8
import sys
import json
import base64
import re
import hashlib
import time
import urllib.parse
sys.path.append('..')
try:
    from base.spider import Spider
except Exception:
    class Spider(object):
        pass

class Spider(Spider):
    host = "https://www.ht058hht.vip:9527"
    SIGN_KEY = "opum3_Loily$SV^6H"
    BUNDLE_ID = "com.ht9.web20.video"
    BRAND_ID = "mitao"
    VERSION = "1.0.0"
    CHANNEL_ID = 5

    def getName(self):
        return "py_红桃视频"

    def init(self, extend=""):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/132.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
        }
        self.device_id = "H5-spider" + hashlib.md5(str(time.time()).encode()).hexdigest()[:6]
        self.user_id = ""
        self.session_id = ""
        self.type_names = {}
        self.subtype_names = {}
        self._inited = False

    def _get_aes_key(self, timestamp):
        return timestamp[-6:] + self.SIGN_KEY[:4] + self.BUNDLE_ID[:6]

    def _get_aes_iv(self):
        return self.BUNDLE_ID[-6:] + self.SIGN_KEY[-4:] + self.device_id[:6]

    def _make_sign(self, params, endpoint):
        sorted_keys = sorted(params.keys())
        concat = ""
        for k in sorted_keys:
            concat += str(params[k])
        concat += self.SIGN_KEY + endpoint
        return hashlib.md5(concat.encode('utf-8')).hexdigest().upper()

    def _encrypt(self, data_str, key, iv):
        from Crypto.Cipher import AES
        data_bytes = data_str.encode('utf-8')
        pad_len = (16 - len(data_bytes) % 16) % 16
        padded = data_bytes + b'\x00' * pad_len
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
        return base64.b64encode(cipher.encrypt(padded)).decode('utf-8')

    def _decrypt(self, enc_str, key, iv):
        from Crypto.Cipher import AES
        enc_bytes = base64.b64decode(enc_str)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
        decrypted = cipher.decrypt(enc_bytes).rstrip(b'\x00').decode('utf-8')
        return json.loads(decrypted)

    def _api_request(self, endpoint, params=None):
        if params is None:
            params = {}
        timestamp = str(int(time.time() * 1000))
        key = self._get_aes_key(timestamp)
        iv = self._get_aes_iv()

        base_params = {
            "timezone": "Asia/Karachi",
            "version": self.VERSION,
            "channelId": self.CHANNEL_ID,
            "channelId2": urllib.parse.urlparse(self.host).netloc,
            "brandId": self.BRAND_ID,
            "t": timestamp,
        }
        base_params.update(params)
        base_params["sign"] = self._make_sign(base_params, endpoint)

        encrypted = self._encrypt(json.dumps(base_params, separators=(',', ':'), ensure_ascii=False), key, iv)

        headers = {
            'User-Agent': self.header['User-Agent'],
            'Content-Type': 'text/plain',
            't': timestamp,
            'deviceId': self.device_id,
            'bundleId': self.BUNDLE_ID,
            'encrypt': 'true',
            'deviceType': 'H5-Android',
            'lang': 'cn',
            'userId': self.user_id,
            'sessionId': self.session_id,
        }

        try:
            import requests
            requests.packages.urllib3.disable_warnings()
            url = self.host + endpoint
            resp = requests.post(url, data=encrypted.encode('utf-8'), headers=headers, verify=False, timeout=15)
            text = resp.text
            result = json.loads(text)
            if result.get("code") == 10000 and isinstance(result.get("data"), str):
                result["data"] = self._decrypt(result["data"], key, iv)
            return result
        except Exception as e:
            print("[py_红桃视频] API请求失败:", e)
            return {}

    def _ensure_login(self):
        if not self._inited and not self.user_id:
            result = self._api_request("/ht/users/deviceLogin")
            if result.get("code") == 10000 and result.get("data"):
                self.user_id = str(result["data"].get("userId", ""))
                self.session_id = result["data"].get("sessionId", "")
            self._inited = True

    def _get_pic(self, url):
        if not url:
            return ""
        if url.startswith("//"):
            url = "https:" + url
        try:
            import requests
            requests.packages.urllib3.disable_warnings()
            resp = requests.get(url, headers=self.header, verify=False, timeout=10)
            data = resp.content
            decrypted = self._decrypt_image(data)
            b64 = base64.b64encode(decrypted).decode()
            return "data:image/jpeg;base64," + b64
        except Exception as e:
            print("[py_红桃视频] 图片获取失败:", e)
            return ""

    def _batch_get_pics(self, url_list):
        """多线程并发下载解密图片"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        result_map = {}
        valid_urls = {}
        for idx, url in enumerate(url_list):
            if url:
                if url.startswith("//"):
                    url = "https:" + url
                valid_urls[idx] = url
        if not valid_urls:
            return result_map

        def download(idx, url):
            try:
                import requests
                requests.packages.urllib3.disable_warnings()
                resp = requests.get(url, headers=self.header, verify=False, timeout=10)
                data = resp.content
                decrypted = self._decrypt_image(data)
                b64 = base64.b64encode(decrypted).decode()
                return idx, "data:image/jpeg;base64," + b64
            except:
                return idx, ""

        with ThreadPoolExecutor(max_workers=10) as pool:
            futures = {pool.submit(download, idx, url): idx for idx, url in valid_urls.items()}
            for future in as_completed(futures):
                idx, pic = future.result()
                result_map[idx] = pic
        return result_map

    def _decrypt_image(self, data):
        """解密图片：每个字节异或0x88"""
        if len(data) < 2:
            return data
        if data[0] == 0xff and data[1] == 0xd8:
            return data
        return bytes([b ^ 0x88 for b in data])

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        self._ensure_login()
        result = self._api_request("/ht/users/appConfig")
        classes = []
        filters = {}
        self.type_names = {}
        self.subtype_names = {}

        if result.get("code") == 10000 and result.get("data"):
            type_list = result["data"].get("appConfig", {}).get("videoTypeList", [])
            for t in type_list:
                if t.get("typePid") == 0:
                    type_id = str(t["typeId"])
                    type_name = t["typeName"]
                    self.type_names[type_id] = type_name
                    classes.append({"type_id": type_id, "type_name": type_name})
                    children = [x for x in type_list if x.get("typePid") == t["typeId"]]
                    if children:
                        filter_items = [{"n": "全部", "v": type_id}]
                        for c in children:
                            c_id = str(c["typeId"])
                            c_name = c["typeName"]
                            self.subtype_names[c_id] = c_name
                            filter_items.append({"n": c_name, "v": c_id})
                        filters[type_id] = [{"key": "subtype", "name": "分类", "value": filter_items}]

        classes.append({"type_id": "chiGua", "type_name": "吃瓜"})
        self.type_names["chiGua"] = "吃瓜"

        return {"class": classes, "filters": filters}

    def homeVideoContent(self):
        self._ensure_login()
        result = self._api_request("/ht/content/homeH5", {"showId": 13, "pageNo": 0, "alreadyShowAdvIds": ""})
        videos = []
        if result.get("code") == 10000 and result.get("data"):
            cl = result["data"].get("contentClassifyList", [])
            for c in cl:
                for i in c.get("videoList", c.get("contentList", [])):
                    name = i.get("title", "")
                    pic = i.get("img", "")
                    id = str(i.get("contentId", ""))
                    remark = str(i.get("duration", ""))
                    videos.append({"vod_id": id, "vod_name": name, "vod_pic": pic, "vod_remarks": remark, "_pic_raw": pic})
            pic_map = self._batch_get_pics([v.get("_pic_raw", "") for v in videos])
            for idx, v in enumerate(videos):
                v["vod_pic"] = pic_map.get(idx, "")
                del v["_pic_raw"]
        result = {'list': videos}
        return result

    def categoryContent(self, cid, pg, filter, ext):
        self._ensure_login()
        videos = []
        
        if cid == "chiGua":
            result = self._api_request("/ht/content/getOriTopicList", {"pageNo": int(pg) - 1, "pageSize": 20})
            if result.get("code") == 10000 and result.get("data"):
                for i in result["data"].get("oriTopicList", []):
                    name = i.get("topicName", "")
                    pic = i.get("topicPic", "")
                    id = "topic_" + str(i.get("topicId", ""))
                    videos.append({"vod_id": id, "vod_name": name, "vod_pic": pic, "vod_remarks": "", "_pic_raw": pic})
            pic_map = self._batch_get_pics([v.get("_pic_raw", "") for v in videos])
            for idx, v in enumerate(videos):
                v["vod_pic"] = pic_map.get(idx, "")
                del v["_pic_raw"]
            result = {'list': videos}
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 20
            result['total'] = 999999
            return result

        type_id = cid
        if ext and isinstance(ext, dict):
            subtype = ext.get("subtype", "")
            if subtype and subtype != cid:
                type_id = subtype

        result = self._api_request("/ht/content/queryTypeVideosH5", {
            "typeId": int(type_id) if type_id.isdigit() else type_id,
            "pageNo": int(pg) - 1,
        })
        if result.get("code") == 10000 and result.get("data"):
            for i in result["data"].get("typeVideoList", []):
                name = i.get("title", "")
                pic = i.get("img", "")
                id = str(i.get("contentId", ""))
                remark = str(i.get("duration", ""))
                videos.append({"vod_id": id, "vod_name": name, "vod_pic": pic, "vod_remarks": remark, "_pic_raw": pic})
            pic_map = self._batch_get_pics([v.get("_pic_raw", "") for v in videos])
            for idx, v in enumerate(videos):
                v["vod_pic"] = pic_map.get(idx, "")
                del v["_pic_raw"]
        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 20
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        self._ensure_login()
        did = ids[0]
        videos = []

        if did.startswith("topic_"):
            topic_id = did.replace("topic_", "")
            result = self._api_request("/ht/content/queryOriTopicVideos", {
                "topicId": int(topic_id),
                "pageNo": 0,
                "pageSize": 50,
            })
            play_url = ""
            if result.get("code") == 10000 and result.get("data"):
                video_ids = result["data"].get("topicVideoIdList", [])
                for v_id in video_ids:
                    play_url += "视频$" + str(v_id) + "#"
                play_url = play_url[:-1]
            videos.append({
                "vod_id": did,
                "vod_name": "吃瓜合集",
                "vod_pic": "",
                "vod_content": "",
                "vod_play_from": "红桃视频",
                "vod_play_url": play_url
            })
            result = {'list': videos}
            return result

        result = self._api_request("/ht/content/detail", {
            "contentId": int(did) if did.isdigit() else did,
            "tryPlayFlag": "0",
        })
        if result.get("code") != 10000 or not result.get("data"):
            return {'list': []}

        data = result["data"]
        vd = data.get("videoDetail", {})
        play_url = data.get("playUrl", "")
        pic = vd.get("img", "")
        if pic:
            if pic.startswith("//"):
                pic = "https:" + pic
            pic = self._get_pic(pic)
        name = vd.get("title", "")
        tags = vd.get("tags", "")
        down_url = data.get("downUrl", "")

        play_parts = ""
        if play_url:
            play_parts = "正片$" + play_url
        if down_url:
            if play_parts:
                play_parts += "#"
            play_parts += "下载$" + down_url

        videos.append({
            "vod_id": str(vd.get("contentId", did)),
            "vod_name": name,
            "vod_pic": pic,
            "vod_content": tags or name,
            "vod_play_from": "红桃视频",
            "vod_play_url": play_parts
        })
        result = {'list': videos}
        return result

    def playerContent(self, flag, id, vipFlags):
        if id.isdigit() and not id.startswith("http"):
            result = self._api_request("/ht/content/detail", {
                "contentId": int(id),
                "tryPlayFlag": "0",
            })
            if result.get("code") == 10000 and result.get("data"):
                play_url = result["data"].get("playUrl", "")
                if play_url:
                    id = play_url
        return {
            'jx': 0,
            'parse': 0,
            'url': id,
            'header': {"User-Agent": "Mozilla/5.0"}
        }

    def searchContent(self, key, quick, pg="1"):
        self._ensure_login()
        videos = []
        result = self._api_request("/ht/content/search", {
            "keywords": key,
            "pageNo": int(pg) - 1,
            "pageSize": 20,
        })
        if result.get("code") == 10000 and result.get("data"):
            for i in result["data"].get("searchList", []):
                name = i.get("title", "")
                pic = i.get("img", "")
                id = str(i.get("contentId", ""))
                remark = str(i.get("duration", ""))
                videos.append({"vod_id": id, "vod_name": name, "vod_pic": pic, "vod_remarks": remark, "_pic_raw": pic})
            pic_map = self._batch_get_pics([v.get("_pic_raw", "") for v in videos])
            for idx, v in enumerate(videos):
                v["vod_pic"] = pic_map.get(idx, "")
                del v["_pic_raw"]
        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 20
        result['total'] = 999999
        return result

    def localProxy(self, param):
        url = base64.urlsafe_b64decode(param.get('url', '')).decode()
        ptype = param.get('type', '')
        if ptype == 'img':
            import requests
            requests.packages.urllib3.disable_warnings()
            resp = requests.get(url, headers=self.header, verify=False, timeout=15)
            data = resp.content
            decrypted = self._decrypt_image(data)
            return [200, "image/jpeg", decrypted]
        return [200, "text/plain", b'']
