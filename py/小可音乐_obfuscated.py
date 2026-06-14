# coding = utf-8
#!/usr/bin/python
import json
import sys
import base64
import types
from base.spider import Spider

sys.path.append('..')

# 动态代码生成与混淆层
_ = lambda x: x
__ = lambda x, y: x if y else x[::-1]
___ = lambda: None

# 字符串编码表
_s = {
    'a': 'aHR0cDovL211c2ljLnhpYW9rZXlpbnl1ZS5jbg==',
    'b': 'YXBpL211c2ljL2xpc3Q=',
    'c': 'Y29kZQ==',
    'd': 'ZGF0YQ==',
    'e': 'bGlzdA==',
    'f': 'dGl0bGU=',
    'g': 'c2luZ2Vy',
    'h': 'dXJs',
    'i': 'aWQ=',
    'j': 'bW9yZQ==',
    'k': 'Y2F0ZWlk',
    'l': 'cGFnZV9ubw==',
    'm': 'cGFnZV9zaXpl',
    'n': 'TW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDEwOyBLKSBBcHBsZVdlYktpdC81MzcuMzY=',
    'o': 'UmVmZXJlcg==',
    'p': 'VXNlci1BZ2VudA==',
    'q': 'QXBwbGljYXRpb24vanNvbg==',
    'r': 'cGFyc2U=',
    's': 'dm9kXw==',
    't': 'aWQ=',
    'u': 'bmFtZQ==',
    'v': 'cGlj',
    'w': 'cmVtYXJrcw==',
    'x': 'cGxheV9mcm9t',
    'y': 'cGxheV91cmw=',
    'z': 'Y29udGVudA==',
}

def _d(k):
    """获取原始Base64字符串"""
    return _s.get(k, k)

# 动态属性访问封装
class _A:
    def __init__(self, obj):
        self._o = obj
    
    def __call__(self, *args, **kwargs):
        return self._o(*args, **kwargs)
    
    def __getattr__(self, name):
        attr = getattr(self._o, name, None)
        if callable(attr):
            return _A(attr)
        return attr
    
    def __getitem__(self, key):
        return self._o.get(key) if hasattr(self._o, 'get') else self._o[key]

# 控制流混淆装饰器
def _f(func):
    def wrapper(*args, **kwargs):
        # 无意义控制流
        _t = 0
        for _ in range(3):
            _t += 1
            if _t > 10:
                break
        
        # 动态跳转
        _c = {0: lambda: None, 1: lambda: None}
        _c.get(_t % 2, lambda: None)()
        
        return func(*args, **kwargs)
    return wrapper

# 核心类 - 高度混淆
class Spider(Spider):
    def __init__(self):
        self.__n = "小可音乐"
        self.__h = base64.b64decode(_d('a')).decode('utf-8')
        self.__r = {
            _d('p'): base64.b64decode('TW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDEwOyBLKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTE0LjAuMC4wIE1vYmlsZSBTYWZhcmkvNTM3LjM2IE1pY3JvTWVzc2VuZ2VyLzguMC4zOC4yNDAxKDB4MjgwMDI2NUQpIFByb2Nlc3MvdG9vbHMgV2VDaGF0L2FybTY0IFdlaXhpbiBOZXRUeXBlL1dJRkkgTGFuZ3VhZ2UvemhfQ04gQUJJL2FybTY0').decode('utf-8'),
            _d('o'): base64.b64decode('aHR0cDovL211c2ljLnhpYW9rZXlpbnl1ZS5jbi9tb2JpbGUv').decode('utf-8'),
            'Accept': base64.b64decode('YXBwbGljYXRpb24vanNvbiwgdGV4dC9wbGFpbiwgKi8q').decode('utf-8'),
        }
        
        # 动态生成分类配置
        _cl = [
            ('1', '5bCP5Y+v5o6o6I2Q5Liy54On', 'NjjpppY='),
            ('2', '5bCP5Y+vVklQ5Liy54On', 'MTIx6aaW'),
            ('3', '5bCP5Y+v57uP5YW46L+e54mI', 'MTY46aaW'),
            ('4', '57uP5YW45Y2V5puy', 'OTnpppY='),
            ('5', '5Lit5paH5Y2V5puy', 'NjI46aaW'),
            ('6', '6Iux5paH5Y2V5puy', 'NTQz6aaW'),
            ('7', '57qv5YeA5Lit5paH5Liy54On', 'MzDpppY='),
            ('8', '5Yqo5oSfOETnjq/nu5U=', 'NjnpppY='),
        ]
        
        self.__cl = []
        self.__cn = {}
        
        for _i, (_id, _name, _cnt) in enumerate(_cl):
            _n = base64.b64decode(_name).decode('utf-8')
            _c = base64.b64decode(_cnt).decode('utf-8')
            self.__cl.append({
                'type_id': _id,
                'type_name': _n,
                'vod_pic': '',
                'vod_remarks': _c
            })
            self.__cn[_id] = _n
    
    @_f
    def getName(self):
        return self.__n
    
    @_f
    def init(self, extend=''):
        pass
    
    @_f
    def homeContent(self, filter):
        _re = {}
        _ca = []
        
        for _c in self.__cl:
            _ca.append({
                'type_id': _c['type_id'],
                'type_name': _c['type_name']
            })
        
        _re['class'] = _ca
        _re['filters'] = {}
        
        # 动态调用
        _fn = getattr(self, '_' + base64.b64decode('X2dldF9jYXRlZ29yeV92aWRlb3M=').decode('utf-8').strip('_'))
        _re['list'] = _fn('1', 1, 10)
        
        return _re
    
    @_f
    def homeVideoContent(self):
        _fn = getattr(self, '_' + base64.b64decode('X2dldF9jYXRlZ29yeV92aWRlb3M=').decode('utf-8').strip('_'))
        return {'list': _fn('1', 1, 10)}
    
    @_f
    def _get_category_videos(self, _t, _p, _l=60):
        _v = []
        try:
            _u = f"{self.__h}/{base64.b64decode(_d('b')).decode('utf-8')}"
            
            _pa = {
                base64.b64decode(_d('k')).decode('utf-8'): _t,
                base64.b64decode(_d('l')).decode('utf-8'): _p,
                base64.b64decode(_d('m')).decode('utf-8'): _l
            }
            
            _re = self.fetch(_u, params=_pa, headers=self.__r)
            
            if not _re or _re.status_code != 200:
                return _v
            
            _d1 = json.loads(_re.text)
            
            if _d1.get(base64.b64decode(_d('c')).decode('utf-8')) != 1:
                return _v
            
            _d2 = _d1.get(base64.b64decode(_d('d')).decode('utf-8'), {})
            _it = _d2.get(base64.b64decode(_d('e')).decode('utf-8'), [])
            
            _it = _it[:_l] if _l > 0 else _it
            
            for _i in _it:
                _ti = _i.get(base64.b64decode(_d('f')).decode('utf-8'), '未知')
                _si = _i.get(base64.b64decode(_d('g')).decode('utf-8'), '')
                
                _vd = {
                    base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('t')).decode('utf-8'): f"{_t}_{_i.get(base64.b64decode(_d('i')).decode('utf-8'), '')}",
                    base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('u')).decode('utf-8'): _ti,
                    base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('v')).decode('utf-8'): '',
                    base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('w')).decode('utf-8'): f"🎵{_si}" if _si else ''
                }
                _v.append(_vd)
            
            return _v
            
        except Exception as _e:
            print(f"获取视频列表失败: {_e}")
            return _v
    
    @_f
    def categoryContent(self, _t, _p, _f, _e):
        _v = []
        try:
            _u = f"{self.__h}/{base64.b64decode(_d('b')).decode('utf-8')}"
            
            _pa = {
                base64.b64decode(_d('k')).decode('utf-8'): _t,
                base64.b64decode(_d('l')).decode('utf-8'): _p,
                base64.b64decode(_d('m')).decode('utf-8'): 60
            }
            
            _re = self.fetch(_u, params=_pa, headers=self.__r)
            
            if not _re or _re.status_code != 200:
                return {'list': [], 'page': int(_p), 'pagecount': 0, 'limit': 60, 'total': 0}
            
            _d1 = json.loads(_re.text)
            
            if _d1.get(base64.b64decode(_d('c')).decode('utf-8')) != 1:
                return {'list': [], 'page': int(_p), 'pagecount': 0, 'limit': 60, 'total': 0}
            
            _d2 = _d1.get(base64.b64decode(_d('d')).decode('utf-8'), {})
            _it = _d2.get(base64.b64decode(_d('e')).decode('utf-8'), [])
            _mo = _d2.get(base64.b64decode(_d('j')).decode('utf-8'), 0)
            
            for _i in _it:
                _ti = _i.get(base64.b64decode(_d('f')).decode('utf-8'), '未知')
                _si = _i.get(base64.b64decode(_d('g')).decode('utf-8'), '')
                
                _vd = {
                    base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('t')).decode('utf-8'): f"{_t}_{_i.get(base64.b64decode(_d('i')).decode('utf-8'), '')}",
                    base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('u')).decode('utf-8'): _ti,
                    base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('v')).decode('utf-8'): '',
                    base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('w')).decode('utf-8'): f"🎵{_si}" if _si else ''
                }
                _v.append(_vd)
            
            _pc = int(_p) + 1 if _mo == 1 else int(_p)
            
            return {
                'list': _v,
                'page': int(_p),
                'pagecount': _pc,
                'limit': 60,
                'total': len(_v) * int(_p)
            }
            
        except Exception as _e:
            print(f"获取分类内容失败: {_e}")
            return {'list': [], 'page': int(_p), 'pagecount': 0, 'limit': 60, 'total': 0}
    
    @_f
    def detailContent(self, _ids):
        try:
            _vid = str(_ids[0])
            _pt = _vid.split('_')
            
            if len(_pt) >= 2:
                _t = _pt[0]
                _sid = _pt[1]
            else:
                return {'list': []}
            
            _u = f"{self.__h}/{base64.b64decode(_d('b')).decode('utf-8')}"
            
            _pa = {
                base64.b64decode(_d('k')).decode('utf-8'): _t,
                base64.b64decode(_d('l')).decode('utf-8'): 1,
                base64.b64decode(_d('m')).decode('utf-8'): 100
            }
            
            _re = self.fetch(_u, params=_pa, headers=self.__r)
            
            if not _re or _re.status_code != 200:
                return {'list': []}
            
            _d1 = json.loads(_re.text)
            
            if _d1.get(base64.b64decode(_d('c')).decode('utf-8')) != 1:
                return {'list': []}
            
            _d2 = _d1.get(base64.b64decode(_d('d')).decode('utf-8'), {})
            _it = _d2.get(base64.b64decode(_d('e')).decode('utf-8'), [])
            
            _vi = None
            for _i in _it:
                if str(_i.get(base64.b64decode(_d('i')).decode('utf-8'), '')) == _sid:
                    _vi = _i
                    break
            
            if not _vi:
                return {'list': []}
            
            _mu = _vi.get(base64.b64decode(_d('h')).decode('utf-8'), '')
            if _mu:
                if _mu.startswith('/'):
                    _mu = 'aHR0cDovL3N0YXRpYy54aWFva2V5aW55dWUuY24=' + _mu
                    _mu = base64.b64decode(_mu[:40]).decode('utf-8') + _mu[40:]
                _mu = _mu.replace('/listen/music/', '/music/')
            
            _ti = _vi.get(base64.b64decode(_d('f')).decode('utf-8'), '未知')
            _si = _vi.get(base64.b64decode(_d('g')).decode('utf-8'), '')
            
            _vd = {
                base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('t')).decode('utf-8'): _vid,
                base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('u')).decode('utf-8'): _ti,
                base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('v')).decode('utf-8'): '',
                base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('w')).decode('utf-8'): f"🎵{_si}" if _si else '',
                base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('z')).decode('utf-8'): f"分类: {self.__cn.get(_t, '')}\n歌手: {_si}",
                'vod_director': '',
                'vod_actor': _si,
                base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('x')).decode('utf-8'): '小可音乐',
                base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('y')).decode('utf-8'): f"{_ti}${_mu}"
            }
            
            return {'list': [_vd]}
            
        except Exception as _e:
            print(f"获取详情失败: {_e}")
            return {'list': []}
    
    @_f
    def searchContent(self, _k, _q, _p=1):
        _v = []
        try:
            for _cid in self.__cn.keys():
                _u = f"{self.__h}/{base64.b64decode(_d('b')).decode('utf-8')}"
                
                _pa = {
                    base64.b64decode(_d('k')).decode('utf-8'): _cid,
                    base64.b64decode(_d('l')).decode('utf-8'): _p,
                    base64.b64decode(_d('m')).decode('utf-8'): 50
                }
                
                _re = self.fetch(_u, params=_pa, headers=self.__r)
                
                if not _re or _re.status_code != 200:
                    continue
                
                _d1 = json.loads(_re.text)
                
                if _d1.get(base64.b64decode(_d('c')).decode('utf-8')) != 1:
                    continue
                
                _d2 = _d1.get(base64.b64decode(_d('d')).decode('utf-8'), {})
                _it = _d2.get(base64.b64decode(_d('e')).decode('utf-8'), [])
                
                for _i in _it:
                    _ti = _i.get(base64.b64decode(_d('f')).decode('utf-8'), '').lower()
                    _si = _i.get(base64.b64decode(_d('g')).decode('utf-8'), '').lower()
                    
                    if _k.lower() in _ti or _k.lower() in _si:
                        _st = _i.get(base64.b64decode(_d('f')).decode('utf-8'), '未知')
                        _ss = _i.get(base64.b64decode(_d('g')).decode('utf-8'), '')
                        
                        _vd = {
                            base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('t')).decode('utf-8'): f"{_cid}_{_i.get(base64.b64decode(_d('i')).decode('utf-8'), '')}",
                            base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('u')).decode('utf-8'): _st,
                            base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('v')).decode('utf-8'): '',
                            base64.b64decode(_d('s')).decode('utf-8') + base64.b64decode(_d('w')).decode('utf-8'): f"🎵{_ss}" if _ss else ''
                        }
                        _v.append(_vd)
            
            _tt = len(_v)
            _pc = (_tt + 49) // 50 if _tt > 0 else 1
            
            return {
                'list': _v[:50],
                'page': int(_p),
                'pagecount': _pc,
                'limit': 50,
                'total': _tt
            }
            
        except Exception as _e:
            print(f"搜索失败: {_e}")
            return {'list': [], 'page': int(_p), 'pagecount': 0, 'limit': 50, 'total': 0}
    
    @_f
    def playerContent(self, _f, _i, _v):
        try:
            _pu = _i
            
            if not _pu:
                return {'parse': 0, 'playUrl': '', 'url': ''}
            
            return {
                'parse': 0,
                'playUrl': '',
                'url': _pu,
                'header': json.dumps({
                    'User-Agent': self.__r['User-Agent'],
                    'Referer': base64.b64decode(self.__r['Referer']).decode('utf-8')
                })
            }
            
        except Exception as _e:
            print(f"播放解析失败: {_e}")
            return {'parse': 0, 'playUrl': '', 'url': ''}
    
    @_f
    def isVideoFormat(self, _u):
        _af = ['.mp3', '.m4a', '.wav', '.flac', '.aac']
        return any(_u.lower().endswith(_f) for _f in _af) or any(_f in _u.lower() for _f in ['.mp3', '.m4a'])
    
    @_f
    def manualVideoCheck(self):
        pass
    
    @_f
    def localProxy(self, _p):
        return None
    
    def fetch(self, _u, params=None, headers=None):
        import requests
        try:
            if headers is None:
                headers = self.__r
            _re = requests.get(_u, params=params, headers=headers, timeout=10)
            return _re
        except Exception as _e:
            print(f"请求异常: {_e}")
            class _fr:
                status_code = 0
                text = ""
            return _fr()

if __name__ == '__main__':
    pass
