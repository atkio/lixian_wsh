#!/usr/bin/python2.7
import sys,os,os.path,json
from lixianwsh import loadpage

print "Content-Type: text/plain"
print
print (json.JSONEncoder().encode(loadpage()))