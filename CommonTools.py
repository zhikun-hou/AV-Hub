import requests;
from bs4 import BeautifulSoup;
from functools import *;
import os;
#多个模块中共用的工具函数



PROXY={"https":"140.227.201.218:60088"};


def getAlias(name):
    alias = name.split("（");
    if len(alias)==1:
        return (name);
    else:
        first = alias[0];
        others = alias[1].split("、");
        others[-1] = others[-1][:-1];#去掉最后的括号
        alias = first,*others;
        return alias;
    

def getPageList(pagenation):
    nav_box = pagenation.find("ul");
    children = len(nav_box.find_all("li"));
    if children==1:#1
        return [1];
    else:
        last = nav_box.find("li",class_="terminal");
        if last:
            href = last.a.get("href");#1 2 3 4 5 下一页 ... 最后一页
            page_num = int(href.split("page=")[1][:-1]);
            return list(range(1,page_num+1));
        else:
            return list(range(1,children));#1 2 3 4 下一页


def combine(pageA,pageB):#用于reduce将若干页面合并
    return pageA+pageB;

def getResponse(url):
    return requests.get(url,proxies=PROXY,timeout=10);
    
def getHtml(url):
    response = getResponse(url);
    if "status_code" not in response or response.status_code != requests.codes.ok:
        response.raise_for_status();
    return response.text;

def getPage(url):
    return BeautifulSoup(getHtml(url),features="html.parser");

def getUrlList(base_url,generators):
    return [base_url+generator for generator in generators];

def fetchInfoFromAllPage(_getPageUrl,_findPagenation,_findPageUnits,_getUnitInfo,_remoteCounter=None,_localCounter=None):
    front_page = getPage(_getPageUrl());#加载首页
    pagenation = _findPagenation(front_page);#获取分页导航栏
    #远程数量获取器与本地数量获取器比较(页面中的总数与数据库中的总数) 一致就跳过首页之后的页面爬取
    if _remoteCounter(pagenation)<=_localCounter():
        return [];
    page_list = getPageList(pagenation);#解析首页 获取页码列表
    def _getPage(page_num):
        if page_num==1:
            return front_page;
        else:
            return getPage(_getPageUrl(page_num));
    def _getPageUnits(page_num):
        page = _getPage(page_num);
        units = _findPageUnits(page);
        return list(map(_getUnitInfo,units));
    page_units = map(_getPageUnits,page_list);#获取页面列表中每个页面的信息单元列表
    return reduce(combine,page_units);#二维数组合并成一维数组


def getFileNameFromPath(path):
    return path.split("/")[-1];


def createPath(path):
    try:
        os.mkdir(path);
    except FileNotFoundError:
        joiner = "\\";
        parent = joiner.join(path.split("\\")[:-1]);
        createPath(parent);
        os.mkdir(path);

        
    
def download(url,save_path,name):
    path = save_path+"/"+name;
    def _save(content):
        try:
            file = open(path, 'wb');
        except FileNotFoundError:
            createPath(save_path);
            file = open(path,'wb');
        try:
            file.write(content);
        except:
            pass;#不能写入就空文件直接保存
        file.close();
    try:
        res = getResponse(url);
        _save(res.content);
    except:
        _save(None);#下载失败 保存空文件
