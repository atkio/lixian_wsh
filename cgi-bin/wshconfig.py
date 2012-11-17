#!/usr/bin/python2.7
import sys,os,os.path,json

WSH_HOME = "/tmp/.lixian"
WSH_CONFIG = "/tmp/.lixian/.lixian_wsh.conf"
os.environ['LIXIAN_HOME'] = WSH_HOME
DEFUALT_CONFIG={ "LIXIAN_HOME":WSH_HOME,"LIXIAN_DOWNLOAD_PATH":"/tmp/lixian/download","username":"username","password":"password","pretask":"","aftertask":""}


def readconf():
	if not os.path.exists(WSH_HOME):
		os.mkdir(WSH_HOME)
	if not os.path.exists(WSH_CONFIG):		
		file(WSH_CONFIG, "w+").write(json.dumps(DEFUALT_CONFIG))
		
	config= json.loads(file(WSH_CONFIG,"r").read())
	return config
		

def readconfstr():
	if not os.path.exists(WSH_HOME):
		os.mkdir(WSH_HOME)
	if not os.path.exists(WSH_CONFIG):
		file(WSH_CONFIG, "w+").write(json.dumps(DEFUALT_CONFIG))
	
	return file(WSH_CONFIG,"r").read()
		
		
def writeconf(data):
	if not os.path.exists(WSH_HOME):
		os.mkdir(WSH_HOME)
	file(WSH_CONFIG, "w+").write(json.dumps(data)) 

	
