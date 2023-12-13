from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import langid
import csv
from clean_comments import clean_comments
import pandas as pd

api_key = 'AIzaSyAiyl4nGKH6EPsZoXNOCqkUCuhieNNybbQ'
api_service_name = "youtube"
api_version = "v3"

youtube = build(api_service_name, api_version, developerKey=api_key)

def get_video_id_from_url(url):
    video_id = url.split("v=")[1]
    return video_id

def is_english(comment):
    try:
        lang, _ = langid.classify(comment)
        return lang == 'en'
    except:
        return False

def scrape_comments(video_url):
    video_id = get_video_id_from_url(video_url)

    try:
        comments = []
        nextPageToken = None

        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                order='relevance',
                maxResults=100,
                pageToken=nextPageToken
            )
            response = request.execute()

            for comment in response.get("items", []):
                text = comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                if is_english(text):
                    comments.append(text)

            comments_df = pd.DataFrame(columns=["Comment"])
            for comment in comments:
                comments_df = comments_df._append({"Comment": comment}, ignore_index=True)

            comments_df = clean_comments(comments_df)

            nextPageToken = response.get("nextPageToken")

            if nextPageToken is None:
                break
            
        comments_df.to_csv('youtube_comments.csv', index=False, encoding="utf-8")

        print(f"Comments have been scraped and saved to csv")

    except HttpError as e:
        print(f"An error occurred: {str(e)}")

    return comments_df
