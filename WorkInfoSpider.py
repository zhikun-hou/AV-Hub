from .CommonTools import *;
import re;


def _getInfoAnchor(bf,key):
    anchor = bf.find("td",string=key+"：");
    return anchor.find_next_sibling("td");
        
def _getNormalizedInfo(td):#DMM当丢失导演或发行商等信息时会显示 ----
    if td.string=="----":
        return None;
    else:
        return td.string;#实际结构是td.a.string

def _getMetaContent(anchor):
    if not anchor:
        return None;
    else:
        return anchor.get("content");

######元信息

def _getDmmCode(bf):#不知道为啥DMM会整出118abp001这种作为URL 可能是多表横向切割？
    #还有url中的番号和页面中的番号不一样的情况...干你妈的日本人
    url = bf.find("meta",property="og:url").get("content");
    code = url.split("cid=")[1][:-1];
    return code;

def _getCode(bf):#蓝光版和典藏版还有不同的番号比如abp120dod  还有dvaj358so这种莫名加个后缀的  53pbdvaj333这种53pb奇怪前缀的出口版  h_479gne114这种不知所云的前缀
    return _getDmmCode(bf);

def _getTitle(bf):
    anchor = bf.find("meta",property="og:title");
    return _getMetaContent(anchor);

def _getDescription(bf):
    anchor = bf.find("meta",property="og:description");
    return _getMetaContent(anchor);    

def _getLength(bf):
    anchor = _getInfoAnchor(bf,"収録時間");
    val = _getNormalizedInfo(anchor);
    if not val:
        return val;
    else:
       return int(val[:-1]);

def _getPublishedTime(bf):
    anchor = _getInfoAnchor(bf,"発売日");
    time = anchor.string.split("/");
    return {"year":int(time[0]),"month":int(time[1]),"day":int(time[2])};

######制作信息

def _getDirector(bf):
    #和出演者等 ----的情况
    anchor = _getInfoAnchor(bf,"監督");
    return _getNormalizedInfo(anchor);

def _getProducer(bf):
    anchor = _getInfoAnchor(bf,"メーカー")
    return _getNormalizedInfo(anchor);

def _getPublisher(bf):
    anchor = _getInfoAnchor(bf,"レーベル");
    return _getNormalizedInfo(anchor);

######作品内容信息

def _getSeries(bf):
    anchor = _getInfoAnchor(bf,"シリーズ");
    return _getNormalizedInfo(anchor);

def _getScore(bf):
    anchor = _getInfoAnchor(bf,"平均評価");
    score = anchor.img.get("alt")[:-1];
    if score=="0":
        return {"num":0,"score":0};#还没有人评分
    else:
        num = int(bf.find("p",class_="d-review__evaluates").strong.string);#总共多少条评分
        avg = float(bf.find("p",class_="d-review__average").strong.string[:-1]);#平均分
        return {"num":num,"score":avg} 
    
def _getTags(bf):
    anchor = _getInfoAnchor(bf,"ジャンル");
    def _getTag(a):
        tag_id = a.get("href").split("id=")[1][:-1];
        return {"name":a.string,"id":tag_id};
    tags = anchor.find_all("a");
    return list(map(_getTag,tags));

def _getPerformer(bf):
    anchor = _getInfoAnchor(bf,"出演者");

    def _getPerformer(performer):
        actress_id = performer.get("href").split("id=")[1][:-1];
        return {"name":performer.string,"id":actress_id};
    def _getPerformerAjax(code):
        return "https://www.dmm.co.jp/mono/dvd/-/detail/performer/=/cid="+code;
    
    if anchor.span.find("a",string="▼すべて表示する"):#说明有多个演员而且无法一次性显示
        ajax_url = _getPerformerAjax(_getDmmCode(bf));
        response = requests.get(ajax_url,proxies=PROXY);#访问ajax获取a标签列表
        ajax = BeautifulSoup(response.text,features="html.parser");
        performers = ajax.find_all("a");
        return list(map(_getPerformer,performers));
    else:
        if anchor.string=="----":#丢失出演者信息
            return [];
        else:
            return list(map(_getPerformer,anchor.span.find_all("a")));

######预览信息

def _getCoverHref(bf):#封面
    anchor = bf.find("div",id="sample-video").find("a",string="イメージを拡大");
    if not anchor:
        return None;
    else:
        return anchor.get("href");

def _getSnapShots(bf):#截图
    def _getSnapShotHref(a):#通过缩略图url获取大图url
        url = a.img.get("src");
        if("name" not in a):#无大图
            return url;
        url = url.split("-");#有大图
        return url[0]+"jp-"+url[1];
    anchor = bf.find("div",id="sample-image-block");
    if not anchor:#没有截图的情况
        return [];
    else:#分有大图和没大图的情况
        snap_shots = anchor.find_all("a");
        return list(map(_getSnapShotHref,snap_shots));

#DMM是点击按钮后用jQuery加载一个视频的iframe 里面有video js加载视频
#不能直接根据规律预测URL 总有视频地址和番号不匹配的情况
def _getPreview(bf):#预览视频
    def _getPreviewAjax(code):
        return "https://www.dmm.co.jp/service/-/html5_player/=/cid="+code+"/mtype=AhRVShI_/service=mono/floor=dvd/mode=/";
    anchor = bf.find("div",id="detail-sample-movie");
    if not anchor:
        return None;
    ajax_url = _getPreviewAjax(_getDmmCode(bf));
    try:
        html = getHtml(ajax_url);#访问ajax获取iframe
    except:
        return False;
    result = re.search('''("bitrate":1500,"src":"){1}.*?("}]){1}''',html);#正则匹配从js代码里获取视频地址
    if result:
        return "http://"+result.group()[26:-3].replace("\/","/");#去除匹配到的头尾 得到video_url
    else:
        return None;#视频不存在的情形


######汇总接口 解析作品信息
def _parseWorkInfo(bf):
    return {
        "title":_getTitle(bf),
        "description":_getDescription(bf),
        "code":_getCode(bf),
        "dmmCode":_getDmmCode(bf),
        "length":_getLength(bf),
        "publishedTime":_getPublishedTime(bf),
        "director":_getDirector(bf),
        "performer":_getPerformer(bf),
        "producer":_getProducer(bf),
        "publisher":_getPublisher(bf),
        "series":_getSeries(bf),
        "tags":_getTags(bf),
        "score":_getScore(bf),
        "cover":_getCoverHref(bf),
        "snapShots":_getSnapShots(bf),
        "preview":_getPreview(bf)
    };


def _getWorkUrl(dmm_code):
    return "https://www.dmm.co.jp/mono/dvd/-/detail/=/cid="+dmm_code;

def fetchWorkInfo(dmm_code):#本函数完成了下载器和解析器的功能)
    bf = getPage(_getWorkUrl(dmm_code));
    return _parseWorkInfo(bf);
