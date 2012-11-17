#!/usr/bin/python2.7
import json
from lixianwsh import addtask

print "Content-Type: text/plain"
print
print (json.JSONEncoder().encode(addtask()))
	
