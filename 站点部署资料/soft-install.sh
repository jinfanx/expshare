#更新apt-get源
apt-get update

#安装vi
apt-get install vim

#安装locate
apt-get install locate

updatedb

#网络管理工具包
apt-get install net-tools

#项目依赖安装
pip install -r /data/requirements.txt

#django-haystack中文检索配置
cp /data/whoosh_cn_backend.py /usr/local/lib/python3.7/site-packages/haystack/backends/whoosh_cn_backend.py
cp /data/ChineseAnalyzer.py /usr/local/lib/python3.7/site-packages/haystack/backends/ChineseAnalyzer.py

#启动项目
nohup uwsgi --http 0.0.0.0:8001 --chdir /data/expshare --module expshare.wsgi>nohup.out &
