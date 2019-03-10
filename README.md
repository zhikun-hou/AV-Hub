# AV-Hub
AV女优/小电影爬虫  
自动爬取日本最大的成人网站DMM 获取最新的女优/小电影情报

# 使用说明
本爬虫基于**Python3**及**MongoDB**数据库写成，请先配置好基本环境  
//爬虫会读取到大量"脏数据"(比如因为404导致的字段缺失) 使用MySQL等数据库会很难处理  若使用其它Non-SQL数据库，可以在DataBase.py中自行修改数据层  
项目所依赖的第三方库:**requests**(网络请求) **bs4**(html解析) **pymongo**(数据库) **threadpool**(线程池) 运行前请自行使用pip命令下载安装  
以上完成之后，在DataBase.py中配置好数据库，将DMM文件夹复制到你的项目中，然后import DMM; 之后即可使用__init__.py中所导出的函数  

# 使用示范
```
import DMM;  
DMM.updateIdolRankList();#将DMM自2005年以来的TOP100女优榜单更新进入数据库 得到idol_rank表  
DMM.updateIdolList();#根据榜单统计著名女优表 得到idol_info表 目前统计得到731人  
DMM.updateIdolWorks();#根据著名女优表爬取单体作品信息(即排除合集作品) 截止2019-03-07共计50864条  
DMM.updateWorkCovers("covers");#将这些作品的封面全部下载至covers文件夹 共计8.23GB
#顺带一提，直接从女优列表而不是排行榜单爬取到的数量是6753位而不是731位，数据量太大爬起来有点麻烦，所以只爬了上过榜的
```
![](https://github.com/XiaYaoShiXin/AV-Hub/blob/master/preview/idol_info.PNG)
爬取到的女优信息
![](https://github.com/XiaYaoShiXin/AV-Hub/blob/master/preview/work_info.PNG)
爬取到的作品信息
![](https://github.com/XiaYaoShiXin/AV-Hub/blob/master/preview/cover.PNG)
爬取到的封面图片

# 注意事项  
由于是成人网站，DMM自己墙掉了日本以外全世界的ip，所以爬虫使用时会用到代理，你可以在CommonTools.py中修改它  
你可以在[free-proxy-list.net](https://free-proxy-list.net/)找到一个稳定的、使用HTTPS协议的日本代理
![](https://github.com/XiaYaoShiXin/AV-Hub/blob/master/preview/proxy.PNG)
//当然，这网站也是不出所料的被墙掉了2333 所以首先你需要能够科学上网:D  
  
因为我电脑有点菜的原因，线程池最大上限设成了10，可以自行修改  
  
DMM这个网站不知道为啥给番号加了各种莫名其妙的前缀和后缀，毫无规律可寻。本来想用正则匹配一下，放弃治疗了，反正去掉tk dod re h_123这些乱七八糟的前后缀你大概能看懂番号是啥就行行


# 应用展示  
Client.py是调用人脸识别平台Face++接口实现的一个【女优识图】应用
随便从数据库里找了个叫立花里子的女优，谷歌找一张她的不是作品封面的照片  
emmm，效果还不错，今后大概会做个网页版的吧:D  
![](https://github.com/XiaYaoShiXin/AV-Hub/blob/master/preview/立花里子.jpg)
![](https://github.com/XiaYaoShiXin/AV-Hub/blob/master/preview/app.PNG)


# 吐槽  
第一次尝试函数式编程，有点原教旨的几乎连一个for循环都没用wwww闭包警告！  
还有 Python的import机制好蠢啊，还是喜欢es6

