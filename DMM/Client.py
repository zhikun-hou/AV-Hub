
import DMM;
import requests;





DMM.updateIdolWorks("高橋しょう子");


'''
pool = Pool(2);

def get(url):

    def _get():
        print("start");
        gevent.sleep(0);
        re = requests.get(url).text;
        print("over");
        return re;
    task = pool.spawn(_get);
    task.join();
    return task.value;

t = get("http://www.baidu.com");
print(t);
k = get("http://www.baidu.com");
print(k);

'''
'''
from Pornhub import *;
from Spider import *;
from FaceApi import *;

    

def Test():
    face = FaceApi.getFace(".","有村千佳2");
    response = FaceApi.searchFace(face["face_token"],"profile");
    print(response);

Test();

'''
#尽量选择正面、清晰、无夸张表情、无马赛克、无他人脸部的截图，提供多张截图可提高准确率


       
#FaceApi.clearFaceSet("profile");
#Pornhub.clearProfileToken();

