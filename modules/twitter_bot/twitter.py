import tweepy
import time

api_key = "LPotDbUaGlxHd3C7fgNoMYuZj"
api_key_secret = "RduzFQBpK1GlNxGVBllncs71kkSRVzrX3X098k7TwV2zakg6g2"
access_token = "1950132579165687808-G0UaT8npy2rfc4hOOQLcu8CThehXZf"
access_token_secret = "sFdw69FBqZvkTOt7qXduumaT7dcStfEUduB9EUPjKPVa2"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAL823QEAAAAAWW2cgil94GuOFYz%2B8YOl5TDoVRc%3DrM53U1CW8obkovBQddynsxbxZIdUjuO3f8n6ecSCyGJiKGHfIU"

auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth)

def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.errors.TooManyRequests:
        time.sleep(300)

for follower in limit_handler(tweepy.Cursor(api.get_followers).items()):
    print(follower)
#Client
# client = tweepy.Client(bearer_token=bearer_token)
# user = client.get_user(username="elonmusk")
# print("User ID:", user.data.id)
# tweets = client.get_users_tweets(id=user.data.id, max_results=5)
# for tweet in tweets.data:
#     print(tweet.text)


# response = client.search_recent_tweets(query="Python", max_results=5)

# for tweet in response.data:
#     print(tweet.text)


# print(dir(api))
# user = api.verify_credentials()

# print(user.name)
# public_tweets = api.home_timeline()

# for tweet in public_tweets:
#     print(tweet)
#     break
# api.update_status("Привет, Twitter API!")
