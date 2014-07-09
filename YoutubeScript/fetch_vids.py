#!/usr/bin/python
#The code sample below calls the API's search.list method
#to retrieve search results associated with a particular keyword.
#https://developers.google.com/youtube/v3/code_samples/python#search_by_keyword

import sys
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
#DEVELOPER_KEY = "AIzaSyAPYdtTZ-m0ZxMmVC1Gap1izSfO6jaNtIc"
DEVELOPER_KEY = "AIzaSyC5E2wUN8L0_RvrwgXangWv9E5t0i7uli4"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  """
  #is this the correct usage?  passing arg to default...
  total = len(sys.argv)
  cmdargs = str(sys.argv)
  print "total: " + str(total)
  searchTerm = str(sys.argv[1])
  print "term: " + searchTerm
  """

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    #q=searchTerm,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []

  #print search_response

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))
   
  #sys.stdout = open('out.txt', 'w')
  encoding = sys.stdout.encoding or 'utf-8'
  #print "Videos:\n", "\n".join(videos), "\n"
  for video in videos:
      print video.encode('utf-8').strip()
  #print "Channels:\n", "\n".join(channels), "\n"
  #print "Playlists:\n", "\n".join(playlists), "\n"


if __name__ == "__main__":
  #example usage: python fet*py --q drphil
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
