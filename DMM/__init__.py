
if __name__ == "__main__":
    from DataBase import *;#数据层
    from IdolRank import updateIdolRankList;#爬取2005年以来DMM的TOP100女优排行榜 rankY全年年榜 rankH1上半年榜 rankH2下半年榜 存入IDOL_RANK表
    from IdolSpider import updateIdolList;#从女优排行榜中统计得到知名女优表 总共700余位 存入IDOL_INFO表 并根据排行进行计分

    from TagSpider import updateTagList;#Tag爬虫 爬取DMM的Tag列表
    from ActressSpider import updateActressCommended,updateActressList;#爬取女优列表和更新推荐女优信息

    from WorkInfoSpider import fetchWorkInfo;#作品信息抓取/解析器
    from WorkSpider import updateWorkInfo,updateFailedWorks,updateFailedIdolWorks,updateIdolWorks;#作品爬虫
    from MediaDownloader import downloadProfile,updateProfies,downloadWorkCover,downloadWorkSnapShots,downloadWorkPreview,updateWorkCovers #预览信息下载器 下载封面、下载截图、下载宣传片、批量更新封面
else:
    from .DataBase import *;
    from .IdolRank import updateIdolRankList;
    from .IdolSpider import updateIdolList;

    from .TagSpider import updateTagList;
    from .ActressSpider import updateActressCommended,updateActressList;

    from .WorkInfoSpider import fetchWorkInfo;
    from .WorkSpider import *;
    from .MediaDownloader import downloadProfile,updateProfies,downloadWorkCover,downloadWorkSnapShots,downloadWorkPreview,updateWorkCovers 


