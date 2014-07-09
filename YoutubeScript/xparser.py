#!/usr/bin/python
#get the length of the candidate video via an xml page
from oauth2client.tools import argparser
import re, urllib, requests
import urllib2
import httplib2
import xml.etree.ElementTree as ET

if __name__ == "__main__":
  #example usage: python fet*py --q drphil
  #accept the args and strip off the two quotes passed to escape chars... better way to clean the vars?
  argparser.add_argument("--q", help="video ID", default=None)
  args = argparser.parse_args()
  
  #stripping off the quotes
  arglen = len(args.q)-1
  args.q=args.q[1:arglen]
  #print args.q

  #try:
  #youtube_search(args)
  #except HttpError, e:
  #  print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

"""""
making http request for xml page:
http://stackoverflow.com/questions/17178483/how-do-you-send-an-http-get-web-request-in-python
http://code.google.com/p/httplib2/wiki/Examples
"""""
#print "testing: "+"https://gdata.youtube.com/feeds/api/videos/"+str(args.q)
h = httplib2.Http()
resp, content = h.request("https://gdata.youtube.com/feeds/api/videos/"+str(args.q), "GET")

root = ET.fromstring(content)
for duration in root.findall('{http://search.yahoo.com/mrss/}group'):
    #print all_descendants
    duration_lst=list(duration.iter('{http://gdata.youtube.com/schemas/2007}duration'))
    #this right here is the length 
    print duration_lst[0].attrib['seconds'] 

