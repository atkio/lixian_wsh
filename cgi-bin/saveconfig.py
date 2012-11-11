#!/usr/bin/python2.7
import sys,os,os.path,json

print "Content-Type: text/plain"
print

import cgi
from wshconfig import *

conf = readconf()
form = cgi.FieldStorage()

if "username" in form:
	conf["username"]=form["username"].value

if "password" in form:
	conf["password"]=form["password"].value

if "LIXIAN_DOWNLOAD_PATH" in form:
	conf["LIXIAN_DOWNLOAD_PATH"]=form["LIXIAN_DOWNLOAD_PATH"].value
	
if "pretask" in form:
	conf["pretask"]=form["pretask"].value
	
if "aftertask" in form:
	conf["aftertask"]=form["aftertask"].value
		
try:
	writeconf(conf)
	print json.dumps(conf)
except:
	print 'err'
	

