import time
import datetime

def addCurrentTime(dic):
    dic['createdate'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    dic['updatedate'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
   # print('时间：'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    return dic

if __name__=="__main__":
    print('当前时间：{0}'.format(datetime.datetime.now()))