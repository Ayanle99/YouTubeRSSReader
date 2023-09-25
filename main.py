import requests
from bs4 import  BeautifulSoup as bs
import json
from datetime import datetime
"""
I added this import to format the video timestamps. 
The videos timestamp will be formated based on your local time. 
"""
from tzlocal import get_localzone



class YouTube:

    def __init__(self, url):
        r = requests.get(url).text
        self.soup = bs(r, 'lxml')

        self.channel = {
            'general': {},
            'videos': [],
            "stat": {}
        }

        self._getChannel()

    def _getChannel(self):

        feed = self.soup.find('feed')

        name = feed.find('title').text
        joined = feed.find('published').text
        link = feed.find('link')['href']

        joined = str(joined).split('T')[0]
        joined = datetime.strptime(joined, '%Y-%m-%d')
        joined = joined.strftime('%b %d, %Y')

        self.channel['general'].update({
            'name': name,
            'link': link,
            'joined': str(joined)
        })

        likes_total = 0
        views_total = 0

        for entry in feed.find_all('entry'):

            videoTitle = entry.find('title').text
            vidLink = entry.find('link')['href']
            published = entry.find('published').text

            """
            I added this line to format the UTC time to CST time.
            """
            published = datetime.fromisoformat(published)
            published = published.strftime('%b %d, %Y %I:%M %p')


            """
            A sample output for the videoPublished is:
            
            video published: Sep 19, 2023 11:00 PM
            video published: Sep 12, 2023 11:00 PM
            video published: Sep 12, 2023 12:35 PM
            video published: Sep 09, 2023 06:22 PM
            ....
            """

            media = entry.find('media:group')

            thumbnail = media.find('media:thumbnail')['url']


            com = media.find('media:community')

            likes = com.find('media:starrating')['count']
            views = com.find('media:statistics')['views']

            likes_total += int(likes)
            views_total += int(views)

            video = {
                'title': videoTitle,
                'link': vidLink,
                'published': published,
                'thumbnail': thumbnail,
                'likes': "{:,}".format(int(likes)),
                'views': "{:,}".format(int(views))
            }

            self.channel['videos'].append(video)


        avgLikes = int(int(likes_total)/15)
        avgViews = int(int(views_total)/15)

        self.channel['stat'].update({
            'average likes': '{:,}'.format(avgLikes),
            'average views': '{:,}'.format(avgViews)
        })


    def getChannel(self):

        general = self.channel['general']
        videos = self.channel['videos']
        stat = self.channel['stat']

        print("General info")
        for k,v in general.items():
            print(k,v)
        print("\nVideos\n")

        for vid in videos:
            for k,v in vid.items():
                print(k,v)
            print()
        print('\nStat\n')

        for k,v in stat.items():
            print(k,v)
        print()



base_url = 'https://www.youtube.com/feeds/videos.xml?channel_id='

pbs_channel_id ='UC3ScyryU9Oy9Wse3a8OAmYQ'
cnn_channel_id = 'UCupvZG-5ko_eiXAupbDfxWw'
corey_channel_id = 'UCCezIgC97PvUuR4_gbFUs5g'
url = base_url+pbs_channel_id

yt = YouTube(url)

