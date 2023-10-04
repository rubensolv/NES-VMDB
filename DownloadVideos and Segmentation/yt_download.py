import os
import argparse

from pytube import Playlist

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='clean.py')
    parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--out', type=str, default='./')
    args = parser.parse_args()

    p = Playlist(args.url)

    print(f'Playlist Name: {p.title}')
    for i, video in enumerate(p.videos):
        try:
            video_title = video.title
        except:
            video_title = '%03d' % i + "_video"

        video_title = video_title.replace('/', '_')
        video_title += '.mp4'
        video_title = os.path.join(args.out, video_title)

        if not os.path.exists(video_title):
            try:
                streams = video.streams.filter(file_extension='mp4')

                if len(streams) > 0:
                    print(f'Downloading video: {video_title}')
                    streams[0].download(filename=video_title, max_retries=3)
                else:
                    print("No streams found!")
            except KeyError:
                print('No streams found')
        else:
            print(f'{video_title} already downloaded')