import json
import os
import urllib

from redvid import Downloader

class ClipDownloader:

    def downloadClips(self, nbclips):
        print("starting download...")
        f = open('./clips/output.json', 'r')
        clips = json.load(f)
        f.close()
        
        if(nbclips == 0):
            nbclips = len(clips)

        path = './clips/individualVids/'
        

        for i in clips :
            title = i['Title']
            url = i['Url']
            downloaded = False

            for filename in os.listdir(path):
                if filename[:13] == url[-13:]:
                    downloaded = True
            
            if not downloaded:
                clip = Downloader()
                clip.max = True
                clip.path = './clips/individualVids'
                clip.url = url

                for attemts in range(10):
                    try:
                        clip.download()
                    except BaseException as e:
                        print('failed. retrying>>>')
                        if attemts == 9:
                            break
                            break
                    else:
                        break
                else:
                    print('no internet connection ;( exiting...')
                    sys.exit()

                nbclips = nbclips - 1
            
                if (nbclips == 0):
                    break

        print("downloading completed...")
            
        