import requests;
import re;
import json;
import pprint;
import time;
import random

import urllib.request

def search(keywords):
    url = getURL(keywords)
    return downloadImage(url, keywords)

def downloadImage(url, keywords=None):
    file_name = 'imagen.'
    extension = url.split('.')
    extension = extension[len(extension)-1]
    print(file_name + extension)
    if not (extension.lower == 'png' or extension.lower() == 'jpg' or extension.lower() == 'jpeg'):
        if keywords is not None:
            print('Buscando otra vez por: GIF o extensión incompatible')
            return (search(keywords))
        else:
            return(None)
    try:
        with urllib.request.urlopen(url) as response, open(file_name+extension, 'wb') as out_file:
            data = response.read()  # a `bytes` object
            out_file.write(data)
    except urllib.error.HTTPError as e:
        if keywords is not None:
            print('Buscando otra vez por: '+str(e))
            return(search(keywords))
        else:
            return(None)
    except urllib.error.URLError as e:
        if keywords is not None:
            print('Buscando otra vez por: ' + str(e))
            return (search(keywords))
        else:
            return(None)
    print(file_name+extension+' descargada')
    return (file_name+extension)

def getURL(keywords, max_results=1):
    url = 'https://duckduckgo.com/';
    params = {
    	'q': keywords
    };

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=(\d+)\&', res.text, re.M|re.I);

    headers = {
    'dnt': '1',
    'accept-encoding': 'gzip, deflate, sdch, br',
    'x-requested-with': 'XMLHttpRequest',
    'accept-language': 'es, en-GB;q=0.8,en;q=0.6,ms;q=0.4',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'referer': 'https://duckduckgo.com/',
    'authority': 'duckduckgo.com',
    }

    params = (
    ('l', 'wt-wt'),
    ('o', 'json'),
    ('q', keywords),
    ('vqd', searchObj.group(1)),
    ('f', ',,,'),
    ('p', '2')
    )

    requestUrl = url + "i.js";

    res = requests.get(requestUrl, headers=headers, params=params);
    data = json.loads(res.text);
    #return printJson(data["results"]);
    images = data["results"]
    image = random.choice(images)["image"]
    return image
    '''if "next" not in data:
        exit(0);
    requestUrl = url + data["next"];'''


'''def printJson(objs):
    for obj in objs:
        #print ("Width {0}, Height {1}".format(obj["width"], obj["height"]))
        #print ("Thumbnail {0}".format(obj["thumbnail"]))
        #print ("Url {0}".format(obj["url"]))
        #print ("Title {0}".format(obj["title"].encode('utf-8')))
        return (obj["image"])
        #print ("__________")'''