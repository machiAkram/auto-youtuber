import praw
import urllib
import random
import json

class Thumbnail :
    
    

    def getThumbnail(self):

        print("downloading thumbnails started...")

        fsecret = open('./reddit_secret.json', 'r')
        secret = json.load(fsecret)
        fsecret.close()
        
        sub = ['aww', 'AnimalsBeingBros', 'AnimalsBeingJerks', 'AnimalsBeingDerps',
            'rarepuppers', 'AnimalsBeingSleepy', 'MadeMeSmile', 'HumansBeingBros', 
            'Birbs', 'Delightfullychubby', 'brushybrushy', 'cats', 'barkour',
            'dogswithjobs', 'LilGrabbies', 'reallifedoodles', 'Catloaf', 'curledfeetsies',
            'tuckedinkitties', 'foxes', 'Eyebleach', 'Blep']

        for attemt in range(10):
            try:
                reddit = praw.Reddit(
                        client_id=secret["client_id"],
                        client_secret=secret["client_secret"],
                        user_agent=secret["user_agent"]
                )
            except praw.exceptions.WebSocketException as e:
                print('Connection to praw api failed. retrying >>>')
            else: 
                break
        else:
            print('Connection to praw api failed completely! retry running the script.')
            sys.exit()
            
        imgs = []

        for s in sub:

            subreddit = reddit.subreddit(s)   # Chosing the subreddit
    
            for submission in subreddit.top("day"):
                domain = submission.domain

                if (submission.is_video == False) and (domain == 'i.redd.it') and (submission.is_self == False):
                    if (int(submission.thumbnail_height) == 78) or (int(submission.thumbnail_height) == 79):
                        if submission.url.endswith(".jpg"):
                            imgs.append(submission.url)

        
        thurl = random.choice(imgs)
        try:
            urllib.request.urlretrieve(thurl, "./clips/thumbnail/thumbnail.jpg")
        except Exception as e:
            print(e)

        print("possible thumbnails downloaded...")

