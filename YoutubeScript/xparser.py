#!/usr/bin/python
#clean up imports
from oauth2client.tools import argparser
import re, urllib, requests
import urllib2
import httplib2
import xml.etree.ElementTree as ET
#from lxml import etree

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
#THIS IS THE WORKING ONE FOR NOW; use content as the xml chunk.
h = httplib2.Http()
resp, content = h.request("https://gdata.youtube.com/feeds/api/videos/"+str(args.q), "GET")
#print "content: "+content 

#xmlURL="gdata.youtube.com/feeds/api/videos/"+str(args.q)
#xmlURL="file:///tmp/"+str(args.q)+'-1'
#print xmlURL

#this gives a response but a LOT of junk with it?
#h = httplib2.Http(str(args.q))
#resp, content = h.request("https://gdata.youtube.com/feeds/api/videos/", "GET")
#print content

#http=httplib2.Http()
#response, content = http.request(xmlURL, 'GET')
#print content

#content=urllib.urlopen(xmlURL).read();
#content = str(requests.get(xmlURL));
#content = urllib2.urlopen(xmlURL).read()
#content= requests.get(xmlURL)
#print content

"""""
Once I get down to parsing it: (learn to use beautiful soup?)
http://docs.python.org/2/library/xml.etree.elementtree.html

I suggest ElementTree (there are other compatible implementations, such as lxml, but what they add is "just" even more speed -- the ease of programming part depends on the API, which ElementTree defines.

After building an Element instance e from the XML, e.g. with the XML function, just:

for atype in e.findall('type')
  print(atype.get('foobar'))

and the like.

parsing may be basic/non-robust for now; fix later
"""""
root = ET.fromstring(content)
#print (root)
#print root.findall('{http://gdata.youtube.com/schemas/2007}duration')
#not empty below...
for duration in root.findall('{http://search.yahoo.com/mrss/}group'):
    #print duration
    #print ET.tostring(duration, encoding="us-ascii", method="xml")
    #print(duration.get('{http://gdata.youtube.com/schemas/2007}duration'))
    #all_descendants = list(duration.iter())
    #print all_descendants
    duration_lst=list(duration.iter('{http://gdata.youtube.com/schemas/2007}duration'))
    #this right here is it 
    print duration_lst[0].attrib['seconds'] 
    #print ET.tostring(duration_lst[0])#, encoding="us-ascii", method="xml")

#for child in root: 
#    print child.tag, child.attrib
#for duration in root.iter('yt:duration'):
#    print duration.attrib
#for group in root.findall("."):
#    print(group.get('id'))

