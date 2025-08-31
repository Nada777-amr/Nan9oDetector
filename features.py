import pandas as pd
from urllib.parse import urlparse
from tld import get_tld

def extract_features(url):
    # hostname length
    hostname_length = len(urlparse(url).netloc)
    
    # count of directories in path
    count_dir = urlparse(url).path.count('/')
    
    # count of 'www' in url
    count_www = url.count('www')
    
    # url length
    url_length = len(str(url))
    
    # first directory length
    try:
        fd_length = len(urlparse(url).path.split('/')[1])
    except:
        fd_length = 0
    
    # count of '-'
    count_dash = url.count('-')
    
    # count of '.'
    count_dot = url.count('.')
    
    # tld length
    try:
        tld_length = len(get_tld(url, fail_silently=True))
    except:
        tld_length = -1
    
    # count of digits
    count_digits = sum(c.isdigit() for c in url)
    
    # count of '='
    count_equal = url.count('=')
    
    features = {
        'hostname_length': hostname_length,
        'count_dir': count_dir,
        'count-www': count_www,
        'url_length': url_length,
        'fd_length': fd_length,
        'count-': count_dash,
        'count.': count_dot,
        'tld_length': tld_length,
        'count-digits': count_digits,
        'count=': count_equal
    }
    
    return features

urls = [
    "https://www.google.com",
    "http://malicious-example.com/path/to/malware",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
]

feature_list = [extract_features(url) for url in urls]
df_features = pd.DataFrame(feature_list)
print(df_features)