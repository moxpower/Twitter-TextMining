import json
import re
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
""" 
tweet = "RT @marcobonzanini: just an example! :D http://example.com #NLP"
print(preprocess(tweet))
"""

with open('twitter_stream.1.json','r') as f:
    line = f.readline()
    #converts json string to a dict:
    tweet = json.loads(line)
    tweettext = preprocess(tweet['text'])
    #tweettext is a list of unicode char
    tweettext=[x.encode('UTF8') for x in tweettext]
    print tweettext
#    tweet = "You may be told that children petting and playing with the cubs, helps them to appreciate conservation. #FALSE https:\/\/t.co\/paLTnMmXNj"
#    print(preprocess(tweettext))
#    print tweet['text']
#    print(json.dumps(tweet, indent=4))