DB_URL = "mongodb://localhost:27017/";
DB_DOC = "DMM";
IDOL_RANK = "idol_rank";


#DataBase 数据层
#IdolRank 爬取2005年以来DMM的TOP100女优排行榜 rankY全年年榜 rankH1上半年榜 rankH2下半年榜 存入IDOL_RANK表
#IdolCount 从女优排行榜中统计得到女优表 总共700余位 存入IDOL_INFO表 并根据排行进行计分

#IdolSpider    从AV女优出发 爬取其作品列表
#ActressSpider 获取DMM的演员信息
#TagSpider     获取DMM的Tag信息

#WorkSpider     参数输入Tag或演员的信息(或列表)获取作品列表并更新作品信息(依赖WorkInfoSpider)
#WorkInfoSpider 解析作品页面 获取作品信息
#WorkPreviewDownloader 下载作品的截图、封面、PV等预览信息

if __name__ == "__main__":
    from IdolRank import updateIdolRankList;
    from IdolSpider import updateIdolList;
    from DataBase import *;#Work和Actress部分 name？id？alias？


    from TagSpider import updateTagList;#翻译问题  alias name id映射关系问题
    from ActressSpider import updateActressCommended,updateActressList;#异步化

    from WorkInfoSpider import fetchWorkInfo;#异步化？ 番号处理 视频bug？
    from WorkSpider import *;#getWorkList,updateIdolWorks;#异步化  列表下载  新片列表<--给getInfoFromAllPage加一个阻断器？
    from WorkPreviewSpider import downloadWorkCover,downloadWorkSnapShots,downloadWorkPreview,updateWorkCovers #预览信息下载器   异步
else:
    from .IdolRank import updateIdolRankList;
    from .IdolSpider import updateIdolList;
    from .DataBase import *;


    from .TagSpider import updateTagList;#翻译问题
    from .ActressSpider import updateActressCommended,updateActressList;#异步化

    from .WorkInfoSpider import fetchWorkInfo;#异步化？ 番号处理 视频bug？
    from .WorkSpider import *;#getWorkList,updateIdolWorks;#异步化？  下载作品列表
    from .WorkPreviewSpider import downloadWorkCover,downloadWorkSnapShots,downloadWorkPreview,updateWorkCovers #预览信息下载器


