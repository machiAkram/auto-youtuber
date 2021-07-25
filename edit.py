from moviepy.editor import VideoFileClip, concatenate_videoclips
from os.path import isfile, join
import random
from moviepy.video.fx.resize import resize
import os, shutil

class Editor:

    def makevid(self):
        print("making compilation...")
        clips = []
        path = './clips/individualVids/'

        for fileName in os.listdir(path):
            if isfile(join(path, fileName)) and fileName.endswith(".mp4"):
                filePath = os.path.join(path, fileName)
                clip = VideoFileClip(filePath)
                clip = clip.resize(width=1920)
                clip = clip.resize(height=1080)
                clips.append(clip)
        
        random.shuffle(clips)

        outro = VideoFileClip('./clips/outro.mp4')
        clips.append(outro)

        final_clip = concatenate_videoclips(clips, method="compose")

        audio_path = "/tmp/temoaudiofile.m4a"
        final_clip.write_videofile("./clips/final/my_concatenation.mp4", threads=4, temp_audiofile=audio_path, remove_temp=True, codec="libx264", audio_codec="aac")

        for i in clips:
            i.close()
        
        print("compilation completed...")
        print("deleting individual clips...")

        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        print("clips removed...")