import sys,os,os.path,json
import cgi
import urllib, subprocess as sub
import cgitb; cgitb.enable()
import time
import re
import base64
from wshconfig import *

def chkscript(scr):
	try:
		return os.path.basename(urllib.unquote(unicode(scr).strip())).replace(" ", "")
	except:
		return ""
		
def startup():
	rs={'msg':'','log':'','rst':'','data':{}}
	rs['data'] = {'startup':'false' ,'logined':'false'}

	#lixian core check
	try:
		sys.path.append('core')
		from lixian import XunleiClient
	except Exception as e:
		rs['msg'] = "coreerr"
		rs['log'] = str(e)
		return rs

	#config check
	try:		
		conf=readconf()
	except Exception as e:
		rs['msg'] = "configerr"
		rs['log'] = str(e)
		return rs

	rs['data']['startup'] = 'true'

	#login check
	try:
		client = XunleiClient(conf['username'],conf['password'],os.environ['LIXIAN_HOME'] +'/.xunlei.lixian.cookies')
	except Exception as e:
		rs['msg'] = "needlogin"
		rs['log'] = str(e)
		return rs

	#client.login
	if not client.has_logged_in():
		rs['msg'] = "needlogin"
		return rs

	rs['data']['logined'] = 'true'
	rs['msg'] ="loginok"
	return rs

def list():
	rs={'msg':'','log':'','rst':'','data':{}}
	form = cgi.FieldStorage()

	if "tasktype" in form:
		status=form["tasktype"].value
	else:
		status = 'all'

	if "id" in form:
		id=form["id"].value
	else:
		id = None

	try:
		sys.path.append('core')
		from wshconfig import readconf
		conf=readconf()
		from lixian import XunleiClient
		client = XunleiClient(conf['username'],conf['password'],conf['LIXIAN_HOME'] +'/.xunlei.lixian.cookies')
	except  Exception as e:
		rs['msg'] = "needlogin"
		rs['log'] = str(e)
		return rs

	if status == 'all':
		tasks = client.read_all_tasks()
	elif status == 'completed':
		tasks = filter(lambda x: x['status_text'] == 'completed', client.read_all_tasks())
	elif status == 'deleted':
		tasks = client.read_all_deleted()
	elif status == 'expired':
		tasks = client.read_all_expired()

	outputs=[]
	for i, t in enumerate(tasks):
		one={}
		one['name']=t['name']
		one['id']=t['id']
		one["status"]=t["status_text"]
		one["size"]=t["size"]
		one["progress"]=t["progress"]
		one["type"]=t["type"]
		outputs.append(one)

	rs["data"]=outputs

	return rs

def readloglines():
	rs={'msg':'','log':'','rst':'false','data':{}}
	form = cgi.FieldStorage()

	try:
		if "id" in form:
			id=form["id"].value
		else:
			id = None
			rs['msg'] = "configerr"
			return rs

		if "lines" in form:
			lnum=int(form["lines"].value)
		else:
			lnum = 1
			
		conf=readconf()
	except  Exception as e:
		rs['msg'] = "configerr"
		rs['log'] = str(e) +"//"+id +","+form["lines"].value
		return rs

	logfile = conf['LIXIAN_HOME'] +"/log/log_" +id
	if not os.path.exists(logfile):
		return rs
	else:
		try:
			rs['data'] = file(logfile, "r").readlines()[-1*lnum:]
			rs['rst'] = "true"
		except  Exception as e:
			rs['log'] = str(e)
			return rs
	return rs
	
def savepage():
	rs={'msg':'','log':'','rst':'','data':{}}

	form = cgi.FieldStorage()
	conf = readconf()
	if "username" in form:                
		conf["username"]=form["username"].value

	if "password" in form:
		conf["password"]=form["password"].value

	if "LIXIAN_DOWNLOAD_PATH" in form:
		conf["LIXIAN_DOWNLOAD_PATH"]=form["LIXIAN_DOWNLOAD_PATH"].value		

	if "pretask" in form:
		if form["pretask"].value == '-':
			conf["pretask"]=""		
		else:
			conf["pretask"]=chkscript(form["pretask"].value)
			
	if "aftertask" in form:
		if form["aftertask"].value == '-':
			conf["aftertask"]=""		
		else:
			conf["aftertask"]=chkscript(form["aftertask"].value)

	try:
		writeconf(conf)
		if not "username" in form and not "password" in form:
			rs['msg']="changeok"
			return rs
		sys.path.append('core')
		from lixian import XunleiClient
		client = XunleiClient(conf['username'],conf['password'],os.environ['LIXIAN_HOME'] +'/.xunlei.lixian.cookies')
		if client.has_logged_in():
			rs['msg']="loginok"
			return rs
		else:
			rs['msg']="faillogin"
			return rs
	except Exception as inst:
		rs['msg']="faillogin"
		rs['log']=str(inst)
		return rs

def addtask():
	rs={'msg':'','log':'','rst':'','data':{}}
	form = cgi.FieldStorage()
	if "url" in form:
		url=form["url"].value
	else:
		url = None
		rs['msg']="needurl"
		return rs	
		
	bt = 0
	if "tasktype" in form:
		bt = (form["tasktype"].value == "bt")	
		
	try:
		sys.path.append('core')
		from lixian_url import url_unmask
		url = url_unmask(url)			
		conf=readconf()		
		from lixian import XunleiClient
		client = XunleiClient(conf['username'],conf['password'],conf['LIXIAN_HOME'] +'/.xunlei.lixian.cookies')		
		if (url.startswith('http://') or url.startswith('ftp://')) and bt:
			torrent = urllib2.urlopen(url, timeout=60).read()
			info_hash = lixian_hash_bt.info_hash_from_content(torrent)		
			client.add_torrent_task_by_content(torrent, os.path.basename(url))
			rs['msg']="addok"
		else:
			client.add_task(url)	
			rs['msg']="addok"
	except Exception as inst:
		rs['msg']="addng"
		rs['log']=str(inst)
		
	return rs

def checkpid(pid):
	try:
		os.kill(pid,0)
		return 1
	except:
		return 0
	
def download():
	rs={'msg':'','log':'','rst':'false','data':{}}	
	form = cgi.FieldStorage()
	if "id" in form:
		id=form["id"].value
	else:
		id = None
		rs['msg']="needurl"
		return rs
	
	if "name" in form:
		name=form["name"].value
	else:
		name = "noname"
		
	try:
		conf=readconf()
		procdir = conf['LIXIAN_HOME'] +"/proc"		 
		if not os.path.exists(procdir):
			os.makedirs(procdir)
		
		if os.path.exists(procdir+"/"+id):
			pid=int(open(procdir+"/"+id, "r").read())
			if checkpid(pid):
				rs['msg']="downloadexist"
				return rs							
			else:
				rs['msg']="downloadagain"
				
		logdir = conf['LIXIAN_HOME'] +"/log"		 
		if not os.path.exists(logdir):
			os.makedirs(logdir)
			
		downdir = conf['LIXIAN_DOWNLOAD_PATH'] 		 
		if not os.path.exists(downdir):
			os.makedirs(downdir)
				
		shdir = conf['LIXIAN_HOME'] +"/sh"
		if not os.path.exists(shdir):
			os.makedirs(shdir)
		
		shcmd=open(shdir + "/" + id,'w+')
		if not chkscript(conf['pretask']).strip()=="":
			shcmd.write("./core/script/" + chkscript(conf['pretask']) + " '" + name + "' " + os.linesep)
		shcmd.write("/usr/bin/python ./core/lixian_cli.py download  " + id + " --continue  --output-dir '" + downdir + "'" +  os.linesep)
		if not chkscript(conf['aftertask']).strip()=="":
			shcmd.write("./core/script/" + chkscript(conf['aftertask']) + " '" + name+ "' ")
		shcmd.close()
		
		os.environ['PATH'] = "/usr/bin"
		proc=sub.Popen(['/bin/bash', '-f', shdir + "/" + id], stdout=file(logdir + "/log_" + id,"w+"),stderr=sub.STDOUT )
		open(procdir+"/"+id, "w+").write(str(proc.pid))
		
		if checkpid(proc.pid):
			if rs['msg']=="":
				rs['msg']="downloadok"		
			rs['rst']="true"			
		else:
			rs['msg']="downloadng"
			rs['log']=urllib.unquote(proc.stdout.read())
			rs['rst']="false"
		
	except Exception as inst:
		rs['msg']="downloadng"
		rs['log']=str(inst)
		rs['rst']="false"
		
	return rs
	
def loadpage():
	rs={'msg':'','log':'','rst':'','data':{}}
	conf = readconf()
	form = cgi.FieldStorage()
	rtn={}
	if "username" in form:
		rtn["username"]=conf["username"]

	if "password" in form:
		rtn["password"]=conf["password"]

	if "LIXIAN_DOWNLOAD_PATH" in form:
		rtn["LIXIAN_DOWNLOAD_PATH"]=conf["LIXIAN_DOWNLOAD_PATH"]
		
	if "pretask" in form:
		rtn["pretask"]=conf["pretask"]
		
	if "aftertask" in form:
		rtn["aftertask"]=conf["aftertask"]
			
	rs['data'] = rtn
	return rs
