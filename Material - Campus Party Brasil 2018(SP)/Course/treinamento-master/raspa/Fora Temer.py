#author: @ Wei Xu
# Import the necessary package to process data in JSON format
import json

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

t = TwitterStream(auth = OAuth('14502701-Rv3I8pkWc5MqKSc8mgRwKTUCMjXRIZTQzoSvvJlIr',
            'aZdgnQKbsmyx8IDV7B3mkl34gckpJsL84Xy76wTgnUcyQ',
            'rmQpKJbQIWSG7sJu0x7YgFV2t',
            'mYKBEBm5JIn08xO0waEoQRe4TUOHlEtl6ByK463yoDTVsePfIr'))

iterator = t.statuses.filter(track="#ForaTemer",language="pt")

count = 100
for tweet in iterator:
    count -= 1
    print (json.dumps(tweet))
    print ()
    if count <= 0:
        break
