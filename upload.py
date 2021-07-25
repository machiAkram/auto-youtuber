import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import json

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Note: Lots of Credit To Jie Jenn 

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def uploadYtvid(VIDEO_FILE_NAME='./clips/final/my_concatenation.mp4',
                title='your daily dose of wholesomeness #',
                description="if you enjoyed don't forget to like the video and hit the notification bell for more.\n\nthese videos aren't mine i simply make compilations\n\nCopyright Disclaimer under section 107 of the Copyright Act 1976, allowance is made for “fair use” for purposes such as criticism, comment, news reporting, teaching, scholarship, education and research. Fair use is a use permitted by copyright statute that might otherwise be infringing.\n outro song: lemon cake by daystar.",
                tags=["wholesome", "cute", "animals", "pets"]):

    print("uploading vid and setting thumbnail...")

    flogs = open('./clips/logs.json', 'r')
    logs = json.load(flogs)
    flogs.close()
    
    now = datetime.datetime.now()
    upload_date_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, int(now.second)).isoformat() + '.000Z'

    request_body = {
        'snippet': {
            'categoryId': 15,
            'title': title + str(logs["Number"]),
            'description': description,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False, 
        },
        'notifySubscribers': True
    }

    mediaFile = MediaFileUpload(VIDEO_FILE_NAME, chunksize=-1, resumable=True)

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    
    service.thumbnails().set(
        videoId=response_upload.get('id'),
        media_body=MediaFileUpload('./clips/thumbnail/thumbnail.jpg')
    ).execute()
    
    with open('./clips/logs.json', 'r') as fp:
        information = json.load(fp)

    information["Number"] += 1

    with open('./clips/logs.json', 'w') as fp:
        json.dump(information, fp, indent=2)

    print("Upload Successful!")
