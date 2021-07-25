import praw
import pprint
import urllib
import json
from redvid import Downloader

from scrape import Scraper
from download import ClipDownloader
from edit import Editor
from thumbnail import Thumbnail
from upload import uploadYtvid


# list of subs
sub = ['aww', 'AnimalsBeingBros', 'AnimalsBeingJerks', 'AnimalsBeingDerps',
       'rarepuppers', 'Zoomies', 'AnimalsBeingSleepy', 'MadeMeSmile', 'nostalgia',
       'wholesomememes', 'HumansBeingBros', 'Birbs', 'Delightfullychubby', 'brushybrushy',
       'Eyebleach', 'MasterReturns', 'DadReflexes', 'happycryingdads', 'ContagiousLaughter',
       'CozyPlaces', 'reallifedoodles', 'UnexpectedlyWholesome', 'likeus']

# sub = ['youtubehaiku', 'holdmybeer', 'videos', 'TikTokCringe', 'dankmemes', 'dankvideos', 'memes', 'funny', 'facepalm', 'MemeVideos', 'videomemes', 'Unexpected', 'perfectlycutscreams']

scraper = Scraper(sub)
scraper.scrape()

downloader = ClipDownloader()
downloader.downloadClips(0)

editor = Editor()
editor.makevid()

thumbnail = Thumbnail()
thumbnail.getThumbnail()

uploadYtvid()
