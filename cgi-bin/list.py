#!/usr/bin/python2.7
import sys,os,os.path,json
import cgi

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
	from wshconfig import *
	conf=readconf()
	from lixian import XunleiClient
	client = XunleiClient(conf['username'],conf['password'],conf['LIXIAN_HOME'] +'/.xunlei.lixian.cookies')
except:
	print '[]'
	sys.exit()


if status == 'all':
	tasks = client.read_all_tasks()
elif status == 'completed':
	tasks = filter(lambda x: x['status_text'] == 'completed', client.read_all_tasks()) 
elif status == 'deleted':
	tasks = client.read_all_deleted()
elif status == 'expired':
	tasks = client.read_all_expired()
	
if not id == None:
	from lixian_tasks import find_tasks_by_id
	tasks = find_tasks_by_id(tasks, id)

outputs=[]
for i, t in enumerate(tasks):
	one={}
	one['name']=t['name']
	one['id']=t['id']
	one["status_text"]=t["status_text"]
	outputs.append(one)
	
print "Content-Type: text/plain"
print
print json.dumps(outputs)
	
