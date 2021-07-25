import praw
import urllib
import json
import datetime

class Scraper :
    sub = []
    
    def __init__(self, sub):

        self.sub = sub

    def scrape(self):

        flogs = open('./clips/logs.json', 'r')
        logs = json.load(flogs)
        flogs.close()

        fsecret = open('./reddit_secret.json', 'r')
        secret = json.load(fsecret)
        fsecret.close()

        if logs['Date'] == datetime.date.today().strftime('%d-%m-%Y'):
            today = False
        else:
            today = True

        if today:

            f0 = open('./clips/output.json', 'r')
            oldclips = json.load(f0)
            f0.close()

            clips = []

            nbposts = 0
            total_duration = 0

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
            
            print("scraping...")
            for s in self.sub:

                subreddit = reddit.subreddit(s)   # Chosing the subreddit
    
                for submission in subreddit.top("day"):
                    nbposts += 1

                    if (submission.is_video) :
            
                        duration = submission.media['reddit_video']['duration']
                        ratio = submission.upvote_ratio
                        score = submission.score
                        title_lenth = len(submission.title)

                        audio_url = submission.url + '/DASH_audio.mp4'
                        try :
                            with urllib.request.urlopen(audio_url) as response:
                                if response.getcode() == 200 :
                                    has_audio = True
                        except urllib.error.HTTPError as e:
                            has_audio = False
            
                        if has_audio and duration <= 35 and ratio >= 0.95 and score >= 50 and title_lenth <= 65 and not submission.over_18:
                            print(submission.subreddit_name_prefixed + ": " + submission.title)
                            total_duration = total_duration + duration
                            try:
                                jsonclip = {
                                    'Title': submission.title,
                                    'Url': submission.url,
                                }
                            except AttributeError as ex:
                                print('Error:', ex)
                                continue
                            
                            if jsonclip not in oldclips:
                                clips.append(jsonclip)

            f = open('./clips/output.json', 'w')
            f.write(json.dumps(clips, indent=2))
            f.close()

            with open('./clips/logs.json', 'r') as fp:
                information = json.load(fp)

            information["Date"] = datetime.date.today().strftime('%d-%m-%Y')

            with open('./clips/logs.json', 'w') as fp:
                json.dump(information, fp, indent=2)
        
            print("scraping completed...")
            print("posts scraped -> " + str(nbposts))
            print("videos saved -> " + str(len(clips)))
            print("total duration -> " + str((total_duration / 60)))
        
        else:
            print("already scraped today's data...")

                        