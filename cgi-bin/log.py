#!/usr/bin/python2.7
import sys,os,os.path,json
import cgi
import urllib

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
	
logfile = conf['LIXIAN_HOME'] +"/log/" +id

print "Content-Type: text/plain"
print

if not os.path.exists(logfile):
	print ""
else:
	try:
		print urllib.unquote(file(logfile, "r").readlines()[-2])
	except:
		print 5000
 