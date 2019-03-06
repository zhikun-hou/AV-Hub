from .DataBase import saveActressInfo,clearActressCommendedInfo,setActressInfo;
from .CommonTools import *;


    
def _fetchActressList(base_url):#获取单个首字母对应的多个页面中所有演员信息
    print(base_url);
    def _getPageUrl(page_num=1):
        print(page_num);
        return base_url+"/page="+str(page_num);
    def _findPagenation(bf):
        return bf.find("div",class_="d-boxcaptside d-boxpagenation");
    def _findPageActress(bf):#获取一页中所有的演员信息
        return bf.find("div",class_="act-box").find_all("a");
    def _getActressInfo(a):#获取每个演员的信息
        actress_id = a.get("href").split("id=")[1][:-1];
        profile_url = a.img.get("src");
        name = a.text;
        actress = {"name":name,"alias":getAlias(name),"id":actress_id,"profile":profile_url};
        saveActressInfo(actress);
        
    return fetchInfoFromAllPage(_getPageUrl,_findPagenation,_findPageActress,_getActressInfo);
    
def _markHotActress(table):
    actress_list = table.find_all("a");
    def _mark(a):
        name = a.text;
        setActressInfo(name,{"hot":True});
    list(map(_mark,actress_list));

def _markNewActress(table):
    actress_list = table.find_all("a");
    def _mark(a):
        name = a.text;
        setActressInfo(name,{"new":True});
    list(map(_mark,actress_list));

def updateActressCommended():#更新首页的新人女优、推荐女优信息
    clearActressCommendedInfo();
    front_page = getPage("https://www.dmm.co.jp/mono/dvd/-/actress/");
    tables = front_page.find_all("div",class_="act-box");
    _markNewActress(tables[0]);
    _markHotActress(tables[1]);

def updateActressList():
    
    URL_GENERATOR = ['a','i','u','e','o',"ka","ki","ku","ke","ko","sa","si","su","se","so","ta","ti","tu","te","to","na","ni","nu","ne","no","ha","hi","hu","he","ho","ma","mi","mu","me","mo","ya","yu","yo","ra","ri","ru","re","ro","wa","wo","nn"];
    #DMM的演员信息列表是按五十音图(首字母)再分页的
    url_list = getUrlList("https://www.dmm.co.jp/mono/dvd/-/actress/=/keyword=",URL_GENERATOR); 
    list(map(_fetchActressList,url_list));

    updateActressCommended();
    

    
    
