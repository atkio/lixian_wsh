#!/usr/bin/python2.7
import sys,os,os.path,json
import cgi

form = cgi.FieldStorage()

if "id" in form:
	id=form["id"].value
else:
	id = None

	
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
	str_command = "/usr/bin/python ./core/lixian_cli.py download  " + id + " --output-dir " + downdir
	print str_command
except:
	print 2000
	sys.exit()

#urllib.unquote(os.environ['QUERY_STRING'])
try:
	os.environ['PATH'] = "/usr/bin"
	sub.Popen(['/bin/bash', '-c', str_command], stdout=open(logdir + "/" + id,'w+') , stderr=sub.STDOUT)
#	sub.Popen(['/bin/bash', '-c', str_command], stdout=open(logdir + "/" + id,'a') , stderr=sub.STDOUT)
#	sub.Popen(['/bin/bash', '-c', str_command], stdout=open(logdir + "/" + id,'a') , stderr=sub.STDOUT)
except:
	print 5000
#output = urllib.unquote(p.stdout.read())

print 0