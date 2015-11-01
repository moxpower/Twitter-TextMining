import simplejson
import re
from collections import Counter
from nltk.corpus import stopwords
import string
import pandas as pd

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + stopwords.words('german') + ['rt','via',':','RT',u'\u2026', u'\ud83d', u'\xfcck']

fname='twitter_stream.4.json'
oname='data.tsv'
 
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
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.UNICODE | re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

with open(fname,'r') as f:
    count_all = Counter()
    lines = (line.rstrip() for line in f) # All lines including the blank ones
    lines = (line for line in lines if line) # Non-blank lines
    for line in lines:
        """        #line = f.readline()
        #converts json string to a dict:"""
        tweet = simplejson.loads(line)
        terms_all = [term.encode('utf-8') for term in preprocess(tweet['text']) if term not in stop]
        count_all.update(terms_all)
        countres = count_all.most_common(30)
        df=pd.DataFrame(countres)
        df.columns=['token','quantity']
        df=df.set_index(['token'])
        df.to_csv(oname,sep = ',')
            
    print(count_all.most_common(30))
#        tweettext = preprocess(tweet['text'].encode('utf-8'))
        #tweettext is a list of unicode char
        #tweettext=[x for x in tweettext]
#        print tweettext

#    tweet = "You may be told that children petting and playing with the cubs, helps them to appreciate conservation. #FALSE https:\/\/t.co\/paLTnMmXNj"
#    print(preprocess(tweettext))
#    print tweet['text']
#    print(json.dumps(tweet, indent=4))