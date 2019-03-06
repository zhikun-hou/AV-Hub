from .DataBase import saveTagInfo;
from .CommonTools import *;
#从DMM上爬取Tag列表


def _fetchAllTags(bf):
    return bf.find("div",class_="area-category").find_all("a");

def _fetchTagInfo(a):
    tag_id = a.get("href").split("id=")[1][:-1];
    return {"name":a.string,"id":tag_id};

def _saveTag(a):
    saveTagInfo(_getTagInfo(a));

#刷新DMM的Tag列表
def updateTagList():
    bf = getPage("https://www.dmm.co.jp/mono/dvd/-/genre/");
    list(map(_saveTag,_getAllTags(bf)));
    

    
    

