## expshare
一个基于django，部署在docker上的经验共享平台，可以随手记下需要百度或谷歌的内容、学习和工作中遇到的坑等，方便以后查看。
同时提供检索功能，当别人遇上和你一样的问题时不用再重新去网上找答案，就像一个字典，查阅即可得到答案。<br/>

## 环境
python3
```
asgiref==3.3.1
Django==3.1.4
django-haystack==3.0
jieba==0.42.1
PyMySQL==0.10.1
pytz==2020.4
sqlparse==0.4.1
Whoosh==2.7.4
```

## 使用
```
python manage.py runserver
```