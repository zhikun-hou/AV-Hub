
import DMM;
import requests;
import os;
from functools import reduce;
import threadpool;

MAX_THREAD_NUM = 3;

API_KEY = "q8IbzsBPD4N1xtz2fe2aYhg0e4v0JOLq";
API_SECRET = "ZHTD0ESfmeu8OOaP_6SyhKYS7h4nLC5X";
FACESET_TAG = "CoverFace";

DETECT_FACE_API = "https://api-cn.faceplusplus.com/facepp/v3/detect"
ADD_FACE_API = "https://api-cn.faceplusplus.com/facepp/v3/faceset/addface"
SEARCH_FACE_API = "https://api-cn.faceplusplus.com/facepp/v3/search";

DETAIL_FACESET_API = "https://api-cn.faceplusplus.com/facepp/v3/faceset/getdetail";
CREATE_FACESET_API = "https://api-cn.faceplusplus.com/facepp/v3/faceset/create";
GET_FACESETS_API  = "https://api-cn.faceplusplus.com/facepp/v3/faceset/getfacesets";

def fetchCoverFace(dmm_code):
    work = getWorkInfo(dmm_code);
    return _fetchCoverFace(work);

def _getBiggestFace(faceA,faceB):
    sizeA = int(faceA["face_rectangle"]["width"])*int(faceA["face_rectangle"]["height"]);
    sizeB = int(faceB["face_rectangle"]["width"])*int(faceB["face_rectangle"]["height"]);
    if sizeB>sizeA:
        return faceB;
    else:
        return faceA;

def _fetchCoverFace(work):
    if not work["cover"]:
        return None;
    if "coverFace" in work:
        return True;
    print("-"+work["dmmCode"]);
    try:
        response = requests.post(DETECT_FACE_API,{"api_key":API_KEY,"api_secret":API_SECRET,"image_url":work["cover"]},timeout=10).json();
        work["coverFace"] = reduce(_getBiggestFace,response["faces"])["face_token"];
        DMM.saveWorkInfo(work);#获取到的面部为空或者请求超时 直接跳过此步骤
        print("+"+work["dmmCode"]);
        return True;
    except:
        print("?"+work["dmmCode"]);
        print(response);
        return False;

def fetchCoverFaces():
    works = DMM.getWorkList({"performer":{"$size":1}},{"dmmCode":1,"cover":1,"coverFace":1});
    pool = threadpool.ThreadPool(MAX_THREAD_NUM);
    requests = threadpool.makeRequests(_fetchCoverFace,works);
    [pool.putRequest(req) for req in requests];
    pool.wait();

def getFaceSets():
    response = requests.post(GET_FACESETS_API,{"api_key":API_KEY,"api_secret":API_SECRET},timeout=10).json();
    if "facesets" not in response:
        return [];
    else:
        return response["facesets"];


def getCoverFaceSets():
    response = requests.post(GET_FACESETS_API,{"api_key":API_KEY,"api_secret":API_SECRET,"tags":FACESET_TAG},timeout=10).json();
    if "facesets" not in response:
        return [];
    else:
        def _getOuterId(faceset):
            return faceset["outer_id"];
        return list(map(_getOuterId,response["facesets"]));

def createCoverFaceSet(id):
    name = FACESET_TAG+"_"+str(id);
    response = requests.post(CREATE_FACESET_API,{"api_key":API_KEY,"api_secret":API_SECRET,"tags":FACESET_TAG,"outer_id":name,"display_name":name},timeout=10).json();
    if "error_message" in response:
        print(response["error_message"]);
        if response["error_message"]=="FACESET_EXIST":
            return createCoverFaceSet(id+1);
        else:
            return False;
    else:
        print("+FACESET:"+str(id));
        return id;


def getCoverFaceSet(id):
    name = FACESET_TAG+"_"+str(id);
    response = requests.post(DETAIL_FACESET_API,{"api_key":API_KEY,"api_secret":API_SECRET,"tags":FACESET_TAG,"outer_id":name},timeout=10).json();
    if "error_message" in response:
        print(response["error_message"]);
        return None;
    else:
        return response;


class FaceSetNotExitsError(Exception):
    pass

class FaceSetFullFilledError(Exception):
    pass


def uploadCoverFaces():
    faceset_id = 1;
    works = list(DMM.getWorkList({"coverFace":{"$exists":True},"coverFaceSet":{"$exists":False}},{"dmmCode":1,"coverFace":1}).limit(5));
    def _combine(workA,workB):
        temp = workA;
        if type(temp) is not str:
            temp = workA["coverFace"];
        return temp+","+workB["coverFace"];
    def _save(work):
        work["coverFaceSet"] = outer_id;
        DMM.saveWorkInfo(work);
    
    while len(works)!=0:
        tokens = reduce(_combine,works);
        outer_id = FACESET_TAG+"_"+str(faceset_id);
        print(outer_id+":"+tokens);
        try:
            response = requests.post(ADD_FACE_API,{"api_key":API_KEY,"api_secret":API_SECRET,"tags":FACESET_TAG,"outer_id":outer_id,"face_tokens":tokens},timeout=10).json();
            if "failure_detail" in response and len(response["failure_detail"])!=0:
                print(response["failure_detail"]);
                if response["failure_detail"][0]["reason"]=="QUOTA_EXCEEDED":#FaceSet容量不够 创建新的
                    raise FaceSetFullFilledError;
                else:
                    raise Exception;
            elif "error_message" in response:
                print(response["error_message"]);
                if response["error_message"]=="INVALID_OUTER_ID":#初始id不存在
                    raise FaceSetNotExitsError;
                else:
                    raise Exception;
            else:
                list(map(_save,works));#添加成功 本地保存信息
                print(outer_id+"+"+tokens);
        except FaceSetNotExitsError:
            faceset_id = createCoverFaceSet(faceset_id+1);
        except FaceSetFullFilledError:
            faceset_id = createCoverFaceSet(faceset_id);
        except Exception as e:
            print(e);
        finally:
          works = list(DMM.getWorkList({"coverFace":{"$exists":True},"coverFaceSet":{"$exists":False}},{"dmmCode":1,"coverFace":1}).limit(5));#继续
  

def _searchFace(face_token):
    face_sets = getCoverFaceSets();
    results = [];
    dic = {};
    def _searchFaceSet(face_set):
        nonlocal results;
        response = requests.post(SEARCH_FACE_API,{"api_key":API_KEY,"api_secret":API_SECRET,"face_token":face_token,"outer_id":face_set,"return_result_count":5},timeout=10).json();
        if "error_message" not in response:
            results += response["results"];
    def _getWorkInfo(result):
        result["work"] = DMM.getWorkInfoBy("coverFace",result["face_token"],{"performer":1});
        performer = result["work"]["performer"][0]["id"];
        dic.setdefault(performer,{});
        dic[performer]["name"] = result["work"]["performer"][0]["name"];
        #sum count avg  
        dic[performer].setdefault("sum",0);
        dic[performer]["sum"] += result["confidence"];
        dic[performer].setdefault("count",0);
        dic[performer]["count"] += 1;
        dic[performer]["avg"] = dic[performer]["sum"] / dic[performer]["count"];
    list(map(_searchFaceSet,face_sets));
    list(map(_getWorkInfo,results));
    return dic;

def searchFace(path):
    response = requests.post(DETECT_FACE_API,{"api_key":API_KEY,"api_secret":API_SECRET},files={"image_file":open(path,'rb')},timeout=10).json();
    if "error_message" in response:
        print(response["error_messagee"]);
    else:
        face = reduce(_getBiggestFace,response["faces"])["face_token"];
        return _searchFace(face);



#妈卖批 写完才发现python没有尾递归优化
print(searchFace("test/f_2300457_1.jpg"));

#DMM.updateProfies("profile");
