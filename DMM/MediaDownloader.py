import os;
from .DataBase import getActressInfo,getWorkInfo,getWorkList,getIdolList;
from .CommonTools import *;
import threadpool;


MAX_THREAD_NUM = 100;

def _getFilePath(save_path,dmm_code):
    return save_path + "\\"+dmm_code+".jpg";

def downloadWorkCover(dmm_code,save_path):
    print("-"+dmm_code);
    work = getWorkInfo(dmm_code);
    url = work["cover"];
    if os.path.exists(_getFilePath(save_path,dmm_code)):#文件已存在 跳过
        return;
    if not url:#无封面 跳过
        return;
    download(url,save_path,dmm_code+".jpg");
    print("+"+dmm_code);

def downloadWorkSnapShots(dmm_code,save_path):
    work = getWorkInfo(dmm_code);
    def _download(url):
        download(url,_getSavePath(dmm_code),dmm_code+".jpg");
    list(map(_download,work["snapShots"]));

def downloadWorkPreview(dmm_code,save_path):
    work = getWorkInfo(dmm_code);
    url = work["preview"];
    if not url:
        return;
    download(url,save_path,dmm_code+".jpg");

def updateWorkCovers(save_path):
    def _getCode(work):
        return work["dmmCode"];
    def _download(dmm_code):
        downloadWorkCover(dmm_code,save_path);
    works = getWorkList();
    #多线程
    pool = threadpool.ThreadPool(MAX_THREAD_NUM);
    code_list = list(map(_getCode,works));
    requests = threadpool.makeRequests(_download,code_list);
    [pool.putRequest(req) for req in requests];
    pool.wait();


def _getProfileDownloader(save_path):
    def _downloadProfile(actress):
        print(actress);
        url = actress["profile"];
        if os.path.exists(_getFilePath(save_path,name)):#文件已存在 跳过
            return;
        if not url:#无封面 跳过
            return;
        download(url,save_path,name+".jpg");
    return _downloadProfile;

def downloadProfile(name,save_path):
    print("-"+name);
    actress = getActressInfo(name);
    _downloader = _getProfileDownloader(save_path);
    _downloader(actress);
    print("+"+name);
    
def updateProfies(save_path):
    idols = getIdolList();
    _downloader = _getProfileDownloader(save_path);
    #多线程
    pool = threadpool.ThreadPool(MAX_THREAD_NUM);
    requests = threadpool.makeRequests(_downloader,idols);
    [pool.putRequest(req) for req in requests];
    pool.wait();
