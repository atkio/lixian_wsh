#!/usr/bin/python2.7
import sys,os,os.path,json

WSH_CONFIG = "/tmp/lixian/.lixian_wsh.conf"

def readconf():
	if not os.path.exists(WSH_CONFIG):
		str='{"LIXIAN_HOME":"/tmp/lixian","LIXIAN_DOWNLOAD_PATH":"/tmp/lixian/download","username":"username","password":"password","pretask":"","aftertask":""}'
		os.environ['LIXIAN_HOME'] = "/tmp/lixian"
		file(WSH_CONFIG, "w+").write(str)
		
	config= json.loads(file(WSH_CONFIG,"r").read())
	os.environ['LIXIAN_HOME'] = config['LIXIAN_HOME']
	return config
		

def readconfstr():
	if not os.path.exists(WSH_CONFIG):
		str='{"LIXIAN_HOME":"/tmp/lixian","LIXIAN_DOWNLOAD_PATH":"/tmp/lixian/download","username":"username","password":"password","pretask":"","aftertask":""}'
		os.environ['LIXIAN_HOME'] = "/tmp/lixian"
		file(WSH_CONFIG, "w+").write(str)
	
	return file(WSH_CONFIG,"r").read()
		
		
def writeconf(data):
	file(WSH_CONFIG, "w+").write(json.dumps(data)) 
	