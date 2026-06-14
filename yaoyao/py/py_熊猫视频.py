# coding=utf-8
# !/usr/bin/python
import sys
import json
import base64

sys.path.append('..')
try:
    from base.spider import Spider
except Exception:
    class Spider(object):
        pass


class Spider(Spider):
    host = "https://spiderscloudcn2.51111666.com"
    forward_url = host + "/forward"

    class_list = [
        {"type_name": "推荐",   "type_id": "0"},
        {"type_name": "91",     "type_id": "6"},
        {"type_name": "精东",   "type_id": "7"},
        {"type_name": "麻豆",   "type_id": "8"},
        {"type_name": "映画",   "type_id": "9"},
        {"type_name": "猫爪",   "type_id": "10"},
        {"type_name": "蜜桃",   "type_id": "11"},
        {"type_name": "天美",   "type_id": "12"},
        {"type_name": "星空",   "type_id": "13"},
    ]

    # ---------------- 工具 ----------------
    @staticmethod
    def e64(text):
        try:
            return base64.b64encode(text.encode('utf-8')).decode('utf-8')
        except Exception:
            return ""

    @staticmethod
    def d64(encoded):
        try:
            return base64.b64decode(encoded.encode('utf-8')).decode('utf-8')
        except Exception:
            return ""

    @staticmethod
    def _pic_to_m3u8(pic_url):
        return (pic_url or "").replace("/1.jpg", "/playlist.m3u8")

    # ---------------- 基础信息 ----------------
    def getName(self):
        return "py_熊猫视频"

    def init(self, extend=""):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/132.0.0.0 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
        }

    def isVideoFormat(self, url):
        return bool(url) and ('.m3u8' in url)

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    # ---------------- HTTP ----------------
    def _post_json(self, type_id, page=1, content="", extra=None):
        body = {
            "command": "WEB_GET_INFO",
            "pageNumber": int(page),
            "RecordsPage": 20,
            "typeId": int(type_id),
            "typeMid": 1,
            "languageType": "CN",
            "content": content,
        }
        if extra and isinstance(extra, dict):
            body.update(extra)
        try:
            resp = self.post(self.forward_url, headers=self.header,
                             data=json.dumps(body, ensure_ascii=False))
            text = resp.content.decode('utf-8')
            return json.loads(text)
        except Exception as e:
            print("[py_熊猫视频] 请求失败:", e)
            return {}

    def _parse_items(self, items):
        vlist = []
        for it in items:
            vid = str(it.get("id", ""))
            name = it.get("vod_name", "")
            pic = it.get("vod_pic", "")
            vlist.append({
                "vod_id": self.e64(vid + "||" + name + "||" + pic),
                "vod_name": name,
                "vod_pic": pic,
                "vod_play_url": self._pic_to_m3u8(pic),
                "vod_year": "",
                "vod_area": "",
                "vod_remarks": "",
                "vod_director": "",
                "vod_actor": "",
                "vod_content": "",
            })
        return vlist

    # ---------------- 壳子接口 ----------------
    def homeContent(self, filter):
        classes = [{"type_name": c["type_name"], "type_id": c["type_id"]}
                   for c in self.class_list]
        return {"class": classes, "filters": {}}

    def homeVideoContent(self):
        data = self._post_json(type_id=0, page=1)
        items = data.get("data", {}).get("resultList", []) if isinstance(data, dict) else []
        return {"list": self._parse_items(items)}

    def categoryContent(self, tid, pg, filter, extend):
        data = self._post_json(type_id=int(tid), page=int(pg), content="")
        items = data.get("data", {}).get("resultList", []) if isinstance(data, dict) else []
        return {
            "list": self._parse_items(items),
            "page": int(pg),
            "pagecount": 9999,
            "limit": 20,
            "total": 999999,
        }

    def searchContent(self, key, quick, pg="1"):
        if not key:
            key = ""
        data = self._post_json(type_id=0, page=int(pg), content=key,
                                extra={"type": "1"})
        items = data.get("data", {}).get("resultList", []) if isinstance(data, dict) else []
        return {
            "list": self._parse_items(items),
            "page": int(pg),
            "pagecount": 9999,
            "limit": 20,
            "total": 999999,
        }

    def detailContent(self, ids):
        if not ids:
            return {"list": []}
        info = self.d64(ids[0])
        if not info or "||" not in info:
            return {"list": []}
        parts = info.split("||", 2)
        if len(parts) < 3:
            return {"list": []}
        vid, name, pic = parts[0], parts[1], parts[2]
        return {"list": [{
            "vod_id": vid,
            "vod_name": name,
            "vod_pic": pic,
            "vod_year": "",
            "vod_area": "",
            "vod_remarks": "",
            "vod_director": "",
            "vod_actor": "",
            "vod_content": name,
            "vod_play_from": "熊猫视频",
            "vod_play_url": "正片${0}".format(self._pic_to_m3u8(pic)),
        }]}

    def playerContent(self, flag, id, vipFlags):
        return {
            "parse": 0,
            "url": id,
            "header": json.dumps(self.header, ensure_ascii=False),
        }

    def localProxy(self, param):
        pass
