import numpy as np
import pandas as pd
import os
import random
import time
#import selenium
#from textblob import TextBlob
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

api_key = os.environ.get("API_KEY")

def get_related_data(driver, url):

    # possibly excessive amount of time to wait for data to load
    time.sleep(2)

    # selected video title
    selected_title_path = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string')
    selected_title = selected_title_path.text

    # get titles - unnecessary due to API calls but does work consistently
    related_videos = driver.find_elements_by_xpath("//*[@id='video-title']")
    related_video_titles = [videos.text for videos in related_videos]
    related_video_titles = related_video_titles[:10]
    # add selected title to top of list
    related_video_titles.insert(0, selected_title)

    # get links
    related_links = driver.find_elements_by_xpath("//*[@id='dismissible']/div/div[1]/a")
    related_links_out = [link.get_attribute('href') for link in related_links]
    related_links_out = related_links_out[:10]
    # add selected link to top of list
    related_links_out.insert(0, url)

    # we need to remove playlists from suggestions, as they require a different API call.
    # dictionary to zip links/titles together for filtering.
    data_dict = dict(zip(related_links_out, related_video_titles))
    # store filtered values.
    filt_dict = {}

    # removing links with substring 'list' will avoid all suggested playlists/mixes.
    for link in data_dict.keys():
        if 'list' not in link:
            filt_dict.update({link:data_dict[link]})


    # store in dataframe
    out_df = pd.DataFrame()
    out_df['Title'] = filt_dict.values()
    out_df['Link'] = filt_dict.keys()

    # parse for URI for API use
    out_df['Id'] = out_df['Link'].apply(lambda x: x.split('=')[1])

    return out_df



def related_api_requests(in_df):
    api_key = os.environ.get("API_KEY")

    # build youtube resource object
    youtube = build('youtube', 'v3', developerKey=api_key)

    # video Ids to feed into API
    # video Ids to feed into API
    related_Ids = list(in_df['Id'])

    # contentDetails videos request to get video length
    vid_request = youtube.videos().list(
        part = 'contentDetails',
        id = related_Ids)
    vid_response = vid_request.execute()

    # loop through durations
    durations = []
    for item in vid_response['items']:
        durations.append(item['contentDetails']['duration'])

    # stat request for likes, dislikes, comment counts, and view counts
    stat_request = youtube.videos().list(
        part = 'statistics',
        id = related_Ids)
    stat_response = stat_request.execute()

    # empty lists to store data
    likes = []
    dislikes = []
    views = []
    comments = []

    # loop through stats
    for stat in stat_response['items']:
        try:
            likes.append(stat['statistics']['likeCount'])
        except KeyError:
            likes.append(0)
        try:
            dislikes.append(stat['statistics']['dislikeCount'])
        except KeyError:
            dislikes.append(0)
        try:
            views.append(stat['statistics']['viewCount'])
        except KeyError:
            views.append(0)
        try:
            comments.append(stat['statistics']['commentCount'])
        except KeyError:
            comments.append(0)

    # get channel titles
    snip_request = youtube.videos().list(
        part = 'snippet',
        id = related_Ids)
    snip_response = snip_request.execute()

    # lists for titles
    channels = []
    #titles = []
    upload_date = []

    # loop through snippets
    for snip in snip_response['items']:
        try:
            channels.append(snip['snippet']['channelTitle'])
        except:
            channels.append('api_error')
        #titles.append(snip['snippet']['title'])
        try:
            upload_date.append(snip['snippet']['publishedAt'])
        except:
            upload_date.append('api_error')

    # add fields to dataframe
    #fields = [durations, likes, dislikes, views, comments]
    df = pd.DataFrame()
    df['Title'] = in_df['Title']
    df['Channel'] = channels
    df['Length'] = durations
    df['Likes'] = likes
    df['Dislikes'] = dislikes
    df['Views'] = views
    #df['LikeRatio'] =
    df['Comments'] = comments
    df['Uploaded'] = upload_date
    df['Depth'] = in_df['depth']

    # convert to int
    fields = ['Likes', 'Dislikes', 'Views', 'Comments']
    #fields = ['Likes', 'Dislikes', 'Views']
    for field in fields:
        df[field] = df[field].apply(lambda x: int(x))

    # create LikeRatio
    df['LikeRatio'] = df['Likes'] / (df['Likes'] + df['Dislikes'])
    return df

def gather_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # https://www.jtrocinski.com/posts/Heroku-Use_Selenium_to_run_Google_Chrome_in_Python.html
    chrome_options.add_argument("disable-dev-shm-usage")

    driver = webdriver.Chrome(executable_path = 'app/dashapp1/chromedriver_linux64/chromedriver', options = chrome_options)
    #url = 'https://www.youtube.com/watch?v=XcOG5iZpV-k' # community
    #url = 'https://www.youtube.com/watch?v=a7RoP1LKMeM' # office
    #watched_links = [] # store watched videos
    #watched_titles = [] # store watched titles
    final_df = pd.DataFrame()

    for i in range(10):
        # add selected video
        #watched_videos.append(url)
        # go to selected video
        driver.get(url)
        # get video title, link, and id
        df = get_related_data(driver, url)
        # add depth
        df['depth'] = i
        # append to output dataframe
        final_df = final_df.append(df)
        # select next video (random)
        # selected video is at top of df, so we start at 1 to avoid repeats
        url = df['Link'][random.randint(1 ,len(df) - 1)]

    stuff = pd.DataFrame()
    # feeding in more than 50 videos per api call causes it to fail?
    # feed 50 at a time, then get the remaining videos and feed them into the api
    for i in range(0,len(final_df)-50,50):
        temp = related_api_requests(final_df[i:i+50])
        stuff = stuff.append(temp)
    # verbose way to get the starting index of the remainder
    remainder = len(final_df) - (len(final_df) % 50)
    temp = related_api_requests(final_df[remainder:remainder + len(final_df) % 50])
    stuff = stuff.append(temp)

    return stuff
