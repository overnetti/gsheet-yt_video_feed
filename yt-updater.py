import httplib2
import os
import sys
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

#Sets up connection to Youtube API.
CLIENT_SECRETS_FILE = "credentials.json"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the Developers Console
https://console.developers.google.com/
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
CLIENT_SECRETS_FILE))

YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3" ##make sure Youtube API v3 is authorized in Google Developer Console

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,message=MISSING_CLIENT_SECRETS_MESSAGE,scope=YOUTUBE_SCOPE)
storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
    flags = argparser.parse_args()
    credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,http=credentials.authorize(httplib2.Http()))

#Update the playlist ID here.
playlist_response = youtube.playlistItems().list(part="snippet,contentDetails,id,status",playlistId="INSERTPLAYLISTID", maxResults=50)

#Puts all of the video IDs in a playlist into a list.
video_ids = [playlist_response.execute()['items'][x]['contentDetails']['videoId'] for x in range(0,len(playlist_response.execute()['items']))]
print(video_ids) 

#Use the video IDs to push the video titles and Youtube descriptions to each video's metadata.

