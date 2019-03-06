import pymongo;
from datetime import datetime;


#数据库配置
DB_URL = "mongodb://localhost:27017/";
DB_DOC = "DMM";
IDOL_RANK = "idol_rank";
IDOL_INFO = "idol_info";
WORK_INFO = "work_info";
TAG_INFO = "tag_info";
ACTRESS_INFO = "actress_info";


##########

def _getDB():
    client = pymongo.MongoClient(DB_URL);
    return client[DB_DOC];

##########

def _getIdolRankCollection():
    return _getDB()[IDOL_RANK];

def _getIdolInfoCollection():
    return _getDB()[IDOL_INFO];

def _getWorkInfoCollection():
    return _getDB()[WORK_INFO];

def _getTagInfoCollection():
    return _getDB()[TAG_INFO];

def _getActressInfoCollection():
    return _getDB()[ACTRESS_INFO];

##########

def saveIdolRank(year,setter):
    return _getIdolRankCollection().update_one({"year":year},{"$set":setter},True);

def getIdolRankList():
    return _getIdolRankCollection().find({});

##########
    
def getIdolInfo(name):
    return _getIdolInfoCollection().find_one({"name":name});

def setIdolInfo(name,setter):
    return _getIdolInfoCollection().update_one({"name":name},{"$set":setter});
    
def saveIdolInfo(setter,inc={}):
    return _getIdolInfoCollection().update_one({"name":setter["name"]},{"$set":setter,"$inc":inc},True);

def getIdolList(search={},fields=None):
    return _getIdolInfoCollection().find(search,fields,no_cursor_timeout =True);

def clearIdolInfo():
    _getIdolInfoCollection().delete_many({});

def updateIdolWorkSuccess(name):
    setIdolInfo(name,{"lastUpdated":datetime.now()});

def updateIdolWorkFailed(name):
    setIdolInfo(name,{"lastUpdated":False});
    
##########
def saveActressInfo(actress):
    _getActressInfoCollection().update_one({"name":actress["name"]},{"$set":actress},True);

def setActressInfo(name,setter):
    _getActressInfoCollection().update_one({"name":name},{"$set":setter});

def getActressInfo(name):
    return _getActressInfoCollection().find_one({"name":name});
    
def getActressID(name):
    actress = _getActressInfoCollection().find_one({"name":name});
    if actress:
        return actress["id"];
    else:
        return None;

def clearActressCommendedInfo():#清除以前的热门、新人信息
    _getActressInfoCollection().update_many({"$or":[{"hot":True},{"new":True}]},{"$unset":{"hot":1,"new":1}});


##########

def saveWorkInfo(work):
    if work:
        _getWorkInfoCollection().update_one({"dmmCode":work["dmmCode"]},{"$set":work,"$unset":{"failed":1}},True);

def fetchWorkFailed(dmm_code):
    _getWorkInfoCollection().update_one({"dmmCode":dmm_code},{"$set":{"failed":True}},True);

def getWorkList(search={},fields=None):
    return _getWorkInfoCollection().find(search,fields,no_cursor_timeout =True);

def getWorkInfo(dmm_code):
    return _getWorkInfoCollection().find_one({"dmmCode":dmm_code});

def clearWorkInfo(selector={}):
    _getWorkInfoCollection().delete_many(selector);

#根据Actress从数据库获取作品列表
def getWorkListByActress(alias):
    return getWorkList({"performer.name":alias});

#根据Actress从数据库获取作品列表
def getWorkListByTag(tag_name):
    return getWorkList({"tags":tag_name});

def getLatestWork(limit,page=1):
    sorted_list = getWorkList().sort([("publishedTime.year",pymongo.DESCENDING),("publishedTime.month",pymongo.DESCENDING),("publishedTime.day",pymongo.DESCENDING)]);
    final_list = sorted_list.limit(limit).skip(page-1);
    return list(final_list);

##########

def saveTagInfo(tag):
    _getTagInfoCollection().update_one({"id":tag["id"]},{"$set":tag},True);

