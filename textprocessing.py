import simplejson
import re
from collections import Counter

fname='twitter_stream.2.txt'
 
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

with open(fname,'r') as f:
    count_all = Counter()
    lines = (line.rstrip() for line in f) # All lines including the blank ones
    lines = (line for line in lines if line) # Non-blank lines
    for line in lines:
        #line = f.readline()
        #converts json string to a dict:
        tweet = simplejson.loads(line)
        terms_all = [term for term in preprocess(tweet['text'])]
        count_all.update(terms_all)
    print(count_all.most_common(5))
        #tweettext = preprocess(tweet['text'])
        #tweettext is a list of unicode char
        #tweettext=[x.encode('UTF8') for x in tweettext]
        #print tweettext
#    tweet = "You may be told that children petting and playing with the cubs, helps them to appreciate conservation. #FALSE https:\/\/t.co\/paLTnMmXNj"
#    print(preprocess(tweettext))
#    print tweet['text']
#    print(json.dumps(tweet, indent=4))