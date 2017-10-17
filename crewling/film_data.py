# -*- coding: utf-8 -*-
"""
Spyder Editor

This is spyder file.
"""


import urllib
import re

def crawling(url, user_agent='wswp', retries=2):
    print("Downloading:", url)
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)

    try:
        html = urllib.request.urlopen(request).read()
    except urllib.URLError as e:
        print("Downloading error", e.reason)
        html = None
        if retries > 0:
            if hasattr(e,'code') and 500 <= e.code < 600:
                crawling(url, retries-1)
    return html

def web_process(webpage):

    FilmInfo = {}
    data = re.findall(r'<span class="rec" id="电影.*?">',webpage)
    data_array = re.split(r'<|=|\s|-|"', data[0])
    film_id = data_array[9]
    FilmInfo["id"]=int(film_id)

    data = re.findall(r'<title>.*?</title>', webpage, re.S)
    data_array = data[0].split()
    film_name = data_array[1]
    FilmInfo["name"] = film_name

    data = re.findall(r'<span class="year">\((.*?)\)</span>', webpage, re.S)
    FilmInfo['date'] = int(data[0])

    data = re.findall(r'<div id="info">(.*?)</div>', webpage, re.S)
    print(data)

    print("film info:", FilmInfo)

    return FilmInfo

def main():
    url="https://movie.douban.com/subject/27038183/?from=showing"
    html = crawling(url)

    webpage = html.decode("utf-8")
    #print(html)

    #print(type(html))
    #print(type(webpage))
    #print(webpage)
    #f = open("movie.html","w", encoding='utf-8')
    #f.write(str(webpage))
    #f.close()

    data = web_process(webpage)


if __name__=="__main__":
    main()
