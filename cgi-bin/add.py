#!/usr/bin/python2.7
import sys,os,os.path,json
import cgi

form = cgi.FieldStorage()

if "url" in form:
	url=form["url"].value
else:
	url = None
	sys.exit()

bt=0
if "bt" in form:
	if form["bt"].value == "bt":
		bt=1

try:
	from wshconfig import *
	conf=readconf()
except:
	print 1000
	sys.exit()

try:
	logdir = conf['LIXIAN_HOME'] +"/log"
	 
	if not os.path.exists(logdir):
		os.makedirs(logdir)
		
	downdir = conf['LIXIAN_DOWNLOAD_PATH'] 
	 
	if not os.path.exists(downdir):
		os.makedirs(downdir)
		
	import cgitb; cgitb.enable()

	# The subprocess module is new in 2.4
	import urllib, subprocess as sub

	# Retrieve the command from the query string
	# and unencode the escaped %xx chars
	if bt:
		str_command = "/usr/bin/python ./core/lixian_cli.py add --bt '" + url +"'"
	else:
		str_command = "/usr/bin/python ./core/lixian_cli.py add '" + url +"'"
	print str_command
except:
	print 2000
	sys.exit()

#urllib.unquote(os.environ['QUERY_STRING'])
try:
	os.environ['PATH'] = "/usr/bin"
	p=sub.Popen(['/bin/bash', '-c', str_command], stdout=sub.PIPE , stderr=sub.STDOUT)
	print urllib.unquote(p.stdout.read())
#	sub.Popen(['/bin/bash', '-c', str_command], stdout=open(logdir + "/" + id,'a') , stderr=sub.STDOUT)
#	sub.Popen(['/bin/bash', '-c', str_command], stdout=open(logdir + "/" + id,'a') , stderr=sub.STDOUT)
except:
	print 5000
#output = urllib.unquote(p.stdout.read())

