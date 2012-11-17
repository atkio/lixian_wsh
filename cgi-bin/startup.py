#!/usr/bin/python2.7
from lixianwsh import startup
import json

print "Content-Type: text/plain"
print
print (json.JSONEncoder().encode(startup()))