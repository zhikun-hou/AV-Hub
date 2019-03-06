from functools import *;
from .DataBase import getActressID,getIdolInfo,getIdolList,getWorkList,getWorkInfo,saveWorkInfo,fetchWorkFailed,updateIdolWorkSuccess,updateIdolWorkFailed,getLatestWork;
from .WorkInfoSpider import fetchWorkInfo;
import threadpool;
from .CommonTools import *;
from datetime import datetime;

MAX_THREAD_NUM = 10;


def updateWorkInfo(dmm_code):#更新作品信息
    try:
        print("-"+dmm_code);
        work_info = fetchWorkInfo(dmm_code);
        saveWorkInfo(work_info);
        print("+"+dmm_code);
    except Exception as e:
        print("?"+dmm_code);
        print(e);
        fetchWorkFailed(dmm_code);

def updateFailedWorks():#更新加载失败了的作品信息
    works = getWorkList({ "$or": [ { "failed":True },{"preview":False}]},{"dmmCode":1});
    pool = threadpool.ThreadPool(MAX_THREAD_NUM);
    def _getCode(work):
        return work["dmmCode"];

    code_list = list(map(_getCode,works));
    requests = threadpool.makeRequests(updateWorkInfo,code_list);
    [pool.putRequest(req) for req in requests];
    pool.wait();
    

def updateFailedIdolWorks():
    idols = getIdolList({"lastUpdated":False},{"name":1})
    def _update(idol):
        updateIdolWorks(idol["name"]);
    list(map(_update,idols));


def updateIdolWorks(name=None,past=2592000):#更新演员的作品信息(数据库中已有作品会跳过)
    def _saveWorkInfo(dmm_code):
        work = getWorkInfo(dmm_code);
        if not work or "failed" in work:#判断是否存在failed 以及unset掉failed
            updateWorkInfo(dmm_code);
    
    def _fetchWorks(name):
        idol = getIdolInfo(name);
        if "lastUpdated" not in idol or not idol["lastUpdated"] or (datetime.now()-idol["lastUpdated"]).total_seconds()>past:
            try:
                works = _fetchWorkListByIdol(name);
                requests = threadpool.makeRequests(_saveWorkInfo,works);
                [pool.putRequest(req) for req in requests]
                pool.wait();
                updateIdolWorkSuccess(name);
            except:
                updateIdolWorkFailed(name);
                print("?"+idol["name"]);

    pool = threadpool.ThreadPool(MAX_THREAD_NUM);
    if name:
        print("*"+name);
        _fetchWorks(name);
    else:
        idols = getIdolList({},fields={"name":1});
        count = 0;
        def _fetchWorkList(idol):
            nonlocal count;
            count+=1;
            print("*("+str(count)+")"+idol["name"]);
            _fetchWorks(idol["name"]);
        list(map(_fetchWorkList,idols));
        


def _findPagenation(bf):
    return bf.find("div",class_="list-boxpagenation");

def _findPageWorks(bf):
    return bf.find_all("p",class_="ttl");

def _getWorkDmmCode(p):
    return p.a.get("href").split("cid=")[1][:-1];

def _remoteWorkCounter(pagenation):
    return int(pagenation.find("p").string.split("タイトル中")[0]);


#根据Actress从DMM获取作品列表
def _fetchWorkListByActress(name):
    actress_id = getActressID(name);
    def _getPageUrl(page_num=1):
        return "https://www.dmm.co.jp/mono/dvd/-/list/=/article=actress/format=dvd/id="+actress_id+"/limit=120/view=text/page="+str(page_num);
    if actress_id:
        return fetchInfoFromAllPage(_getPageUrl,_findPagenation,_findPageWorks,_getWorkDmmCode);
    else:
        return [];
              

#根据Actress从DMM获取作品列表 但只获取单体作品
def _fetchWorkListByIdol(name):#format(dvd/bd)  
    actress_id = getActressID(name);
    def _getPageUrl(page_num=1):
        return "https://www.dmm.co.jp/mono/dvd/-/list/=/article=actress/format=dvd/id="+actress_id+"/limit=120/n1=DgRJTglEBQ4GpoD6,YyI,qs_/view=text/page="+str(page_num);
    def _localWorkCounter():
        return getWorkList({"performer.name":name},{"_id":1}).count();
    if actress_id:
        return fetchInfoFromAllPage(_getPageUrl,_findPagenation,_findPageWorks,_getWorkDmmCode,_remoteWorkCounter,_localWorkCounter);
    else:
        return [];

#根据Tag从DMM获取作品列表
def _fetchWorkListByTag(tag_name):
    tag_id = getActressID(name);
    def _getPageUrl(page_num=1):
        return "https://www.dmm.co.jp/mono/dvd/-/list/=/article=keyword/format=dvd/id="+tag_id+"/limit=120/view=text/page="+str(page_num);
    if tag_id:
        return fetchInfoFromAllPage(_getPageUrl,_findPagenation,_findPageWorks,_getWorkDmmCode);
    else:
        return [];

def _updateWorkInfo(dmm_code):
    work = fetchWorkInfo(dmm_code);
    saveWorkInfo(work);

#根据爬取到的作品列表获取作品信息
def fetchWorkListInfo():
    pass;


#新片更新
def _fetchWorkListRecently():
    #获取列表到数据库中已存在时中断
    #https://www.dmm.co.jp/mono/dvd/-/list/=/format=dvd/limit=120/sort=date/view=text/
    pass;


#####################从alias转换为name
