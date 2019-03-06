from .DataBase import clearIdolInfo,getIdolRankList,getIdolInfo,setIdolInfo,saveIdolInfo;
from .CommonTools import *;
from datetime import datetime;
from .IdolRank import updateIdolRankList;

CURRENT_YEAR = datetime.now().year;

'''
sum:按每年名次的累加分
avg:按照参与评分的次数平均
weight：加权分 3年内系数2 ，3-6系数1.5 6-9系数1 超过9年系数0.5
'''

def _getWeight(year):
    delta = CURRENT_YEAR - year;
    if delta > 9:
        return 0.5;
    elif delta > 6:
        return 1;
    elif delta >3:
        return 1.25;
    else:
        return 1.5;


def _countEachYear(ranks):
    year = ranks["year"];
    def _countRank(rank_type,rank):
        def _countEachIdol(num):
            actress_id = rank[num]["id"];
            name = rank[num]["name"];
            point = 101 - int(num);
            point_weighted = point * _getWeight(year);

            info_set = {"id":actress_id,"name":name,"alias":getAlias(name),"rank."+str(year)+"_"+rank_type:num};
            points_inc = {"points.sum":point,"points.weight":point_weighted};
            saveIdolInfo(info_set,points_inc);
            
            idol = getIdolInfo(name);
            avg = idol["points"]["sum"] / len(idol["rank"]);
            setIdolInfo(name,{"points.avg":avg});

        list(map(_countEachIdol,rank));

    _countRank("H1",ranks["rankH1"]);
    _countRank("H2",ranks["rankH2"]);
    _countRank("Y",ranks["rankY"]);



def updateIdolList():
    updateIdolRankList();
    clearIdolInfo();
    ranks = getIdolRankList();
    list(map(_countEachYear,ranks));

