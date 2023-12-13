import pandas as pd
import gzip
import json
import re
import string

def clean_comments(df):
    patterns = [
      "\n", #removing new line characters
      "\w*\d\w*", #removing digits
      r"(http\S+)", #removing URLs
      r"([\w\.\-\_]+@[\w\.\-\_]+)", #removing e-mails
      r"([^a-zA-Z\s])" #removing special characters
      r"(@[A-Za-z0-9_]+)", #removing @pings
      r"([[]\-;',./?><:{}|_=+]`)",
      r"(#[A-Za-z0-9_]+)" #removing hashtags
      r"[\n\t\s]*"] #Remove all white \t spaces, new lines \n and tabs \t

    for pattern in patterns:
      df['Comment'] = df['Comment'].apply(lambda x: re.sub(pattern, '', str(x)))

    def remove_emoji(text):
        emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U0001F91E"
                               u"\U0001FA75"
                               "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
    
    df['Comment'] = df['Comment'].apply(lambda x: remove_emoji(str(x)))

    df = df.dropna()
    df = df.drop_duplicates()
    return df