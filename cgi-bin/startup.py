#!/usr/bin/python2.7
import sys,os,os.path,json


print "Content-Type: text/plain"
print

#lixian core check
try:
	sys.path.append('core')
	from lixian import XunleiClient
except:
	print 1000 #Error core not exist
	sys.exit()
	
#config check
try:
	from wshconfig import *
	conf=readconf()
except:
	print 2000 
	sys.exit()
	
#login check	
try:
	client = XunleiClient(conf['username'],conf['password'],os.environ['LIXIAN_HOME'] +'/.xunlei.lixian.cookies')
except:
	print 3000 
	sys.exit()



#client.login
if not client.has_logged_in(): 
	print 4000
	sys.exit()


print 0