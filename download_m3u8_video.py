from time import sleep

import requests
import re
from tqdm import tqdm

def ts_long(video_link, video_name, store_path):
    url = video_link
    url = url.replace('dh5', 'hls').replace('myalicdn', 'kcdnvip')
    delete_place = url.find('h5e')
    url = url[: delete_place] + url[delete_place + 4:]
    place = url.find('?')
    url = url[:place]
    url = url.replace('main', '2000')

    resp = requests.get(url)
    data = resp.text
    # print(data)
    sleep(20) #todo
    video_clip_list = re.findall(r'.*?.ts', data)
    # print(video_clip_list)
    print("\033[1;37mdownloading: %s.mp4m\033[0m" % video_name)
    download_video(url, video_clip_list, video_name, store_path)

def download_video(original_video_link, video_clip_list, video_name, store_path):
    number = len(video_clip_list)
    for i in tqdm(range(0, number),ncols=100):
        url = original_video_link.replace('2000.m3u8', video_clip_list[i])

        res = requests.get(url)
        data = res.content
        with open(store_path + video_name + '.mp4', 'ab+') as f:
            f.write(data)
            f.flush()
    print("\033[1;37mdownload %s successfullym\033[0m" % video_name + '.mp4')
