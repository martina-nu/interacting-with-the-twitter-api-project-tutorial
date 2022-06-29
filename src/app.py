#Import

from dotenv import load_dotenv
import os 
import tweepy
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import re

# Step 1: Create a twitter developer account

#Step 2: initial setup

#Step 3: Environment variables

load_dotenv()                    


consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
bearer_token = os.environ.get('BEARER_TOKEN')

# Step 4: Innitialize the tweepy library
client = tweepy.Client( bearer_token=bearer_token, 
                        consumer_key=consumer_key, 
                        consumer_secret=consumer_secret, 
                        access_token=access_token, 
                        access_token_secret=access_token_secret, 
                        return_type = requests.Response,
                        wait_on_rate_limit=True)




#step 5: Start making requests to the API

query = '#100daysofcode (pandas OR python) -is:retweet'

tweets = client.search_recent_tweets(query=query, 
                                    tweet_fields=['author_id','created_at','lang'],
                                     max_results=100)


# Step 6: Convert to pandas Dataframe

tweets_dict = tweets.json() #Save tweets as dictionary

data = tweets_dict['data'] #Extract "data" value from dictionary

df = pd.json_normalize(data) #Transform to pandas df


#Take a look at the dataframe to make sure is correct `df.head()`

print(df.head()) # Go to explore.ipynb for better visualization

#Save data to csv
df.to_csv("coding-tweets.csv")

#Step 7: Search for the words

#text analysis

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)

    if match:
        return True
    return False
pandas = 0
python = 0

for index, row in df.iterrows():
    pandas += word_in_text('pandas', row['text'])
    python += word_in_text('python', row['text'])

print(f"The word python was mentioned {python} times")
print(f"The word pandas was mentioned {pandas} times")



#Visualize data


# Set seaborn style
sns.set(color_codes=True)

# Create a list of labels:cd
cd = ['pandas', 'python']

# Plot the bar chart
ax = sns.barplot(cd, [pandas, python])
ax.set(ylabel="number of tweets", title='Number of tweets in which pandas and python are mentioned.')

plt.show()

