#!/usr/bin/python2.7
import sys,os,os.path,json

WSH_CONFIG = "/tmp/lixian/.lixian_wsh.conf"

def readconf():
	try:
		config= json.loads(file(WSH_CONFIG).read())
		os.environ['LIXIAN_HOME'] = conf['LIXIAN_HOME']
		return config
	except:
		str='{"LIXIAN_HOME":"/tmp/lixian","LIXIAN_DOWNLOAD_PATH":"/tmp/lixian/download","username":"username","password":"password","pretask":"","aftertask":""}'
		os.environ['LIXIAN_HOME'] = "/tmp/lixian"
		file(WSH_CONFIG, "w").write(str)  
		return json.loads(str)
		

def readconfstr():
	try:
		return file(WSH_CONFIG).read()
	except:
		str='{"LIXIAN_HOME":"/tmp/lixian","LIXIAN_DOWNLOAD_PATH":"/tmp/lixian/download","username":"username","password":"password","pretask":"","aftertask":""}'
		os.environ['LIXIAN_HOME'] = "/tmp/lixian"
		file(WSH_CONFIG, "w").write(str)  
		return str
		
def writeconf(data):
	file(WSH_CONFIG, "w").write(json.dumps(data)) 