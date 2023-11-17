import os
import json
import time
import sys
from multiprocessing.dummy import Pool
import random
import logging

logging.basicConfig(filename='download_{}.log'.format(int(time.time())), filemode='w', level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# youtube_downloader = "youtube-dl"
youtube_downloader = "yt-dlp"


def check_youtube_dl_version():
    ver = os.popen(f'{youtube_downloader} --version').read()

    assert ver, f"{youtube_downloader} cannot be found in PATH. Please verify your installation."
    
def download_yt_videos(indexfile, saveto='raw_videos'):
    content = json.load(open(indexfile))
    
    if not os.path.exists(saveto):
        os.mkdir(saveto)
    
    for entry in content:
        gloss = entry['gloss']
        instances = entry['instances']

        for inst in instances:
            video_url = inst['url']
            video_id = inst['video_id']

            if 'youtube' not in video_url and 'youtu.be' not in video_url:
                continue

            if os.path.exists(os.path.join(saveto, video_url[-11:] + '.mp4')) or os.path.exists(os.path.join(saveto, video_url[-11:] + '.mkv')):
                logging.info('YouTube videos {} already exists.'.format(video_url))
                continue
            else:
                cmd = f"{youtube_downloader} \"{{}}\" -o \"{{}}%(id)s.%(ext)s\""
                cmd = cmd.format(video_url, saveto + os.path.sep)

                rv = os.system(cmd)
                
                if not rv:
                    logging.info('Finish downloading youtube video url {}'.format(video_url))
                else:
                    logging.error('Unsuccessful downloading - youtube video url {}'.format(video_url))

                time.sleep(random.uniform(1.0, 1.5))

if __name__ == '__main__':
    check_youtube_dl_version()
    logging.info('Start downloading youtube videos.')
    download_yt_videos('example.json')