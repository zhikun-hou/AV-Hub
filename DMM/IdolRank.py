import requests;
from bs4 import BeautifulSoup;
from functools import *;
from .DataBase import saveIdolRank;
from .CommonTools import *;
import datetime;

#URL生成器 DMM把每个排行榜分成了五个页面
RANK_GENERATOR = ("1_20","21_40","41_60","61_80","81_100");




def _getUrl(year,type_name,rank):#获取排名页的URL
    return "https://www.dmm.co.jp/mono/dvd/-/ranking/=/mode=actress/term="+type_name+"_"+str(year)+"/rank="+rank;

def _getRank(td):#获取排名表格中每个方块的内容
    anchor = td.find_next_sibling("a");
    name = anchor.img.get("alt");
    actress_id = anchor.get("href").split("id=")[1][:-1];
    rank = td.string;
    print(rank.zfill(3)+":"+name);
    return {rank:{"name":name,"id":actress_id}};

def _combineRank(a,b):#将每个方块中的内容合并成一个排名
    a.update(b)
    return a;


def _getRankListOfYear(year):
    print("["+str(year)+"]=========================");
    def _getRankListOfType(type_name):
        def _getRankRange(rank):#获取某个排名区间
            bf = getPage(_getUrl(year,type_name,rank));
            td = bf.find_all("span",class_="rank");#空页面bug 原网页2017/2018下半年排名丢失了
            if len(td)==0:
                return {};
            else:
                rank_list = map(_getRank,td);
                return reduce(_combineRank,rank_list);
        print("["+type_name+"]-------------------------");
        range_list = map(_getRankRange,RANK_GENERATOR);
        return reduce(_combineRank,range_list);
        
    return {"year":year,"rankH1":_getRankListOfType("first"),"rankH2":_getRankListOfType("last"),"rankY":_getRankListOfType("year")};
            

def _getAllRank(last_year):
    year_range = list(range(2005,last_year+1));
    return list(map(_getRankListOfYear,year_range));

def updateIdolRankList():
    t = datetime.datetime.now();
    year = t.year;
    idol_ranks = _getAllRank(year);
    
    def _saveIdolRank(rank):
        saveIdolRank(rank["year"],rank);
        
    list(map(_saveIdolRank,idol_ranks));


