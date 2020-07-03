#!/usr/bin/env python3

import os
import sys
import json
import test_display
import pprint
import requests

# Constants

KEY = 'BIBIh4HMIunzyZLz8GagHC9GW7ZYmbjV'
NYT_URL = 'https://api.nytimes.com/svc/topstories/v2/home.json?api-key='

# Functions

def load_nyt_data(url):
    
    # set up headers
    headers  = {'user-agent': 'nyt-{}'.format(os.environ.get('USER', 'me'))}

    # send request, get JSON back
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = json.loads(response.text)
    
    articles = data['results']
    titles = list(map(lambda x: x['title'], articles))
    return titles


def main():
    url = NYT_URL + KEY
    titles = load_nyt_data(url)
    for title in titles:
	print(title)
	test_display.scroll_word(0, 4,'       ' + title, 7)

# Main Execution

if __name__ == '__main__':
    main()
