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
    FilmInfo["date"] = int(data[0])


    data = re.findall(r'rel="v:directedBy">(.*?)</a>', webpage, re.S)
    FilmInfo["directeBy"] = data

    data = re.findall(r'''<span ><span class='pl'>编剧</span>: <span class='attrs'>(.*?)</span><br/>''', webpage, re.S)
    data_array = re.findall(r'>(.*?)</a>', data[0], re.S)
    FilmInfo["scriptwriter"] = data_array


    data = re.findall(r'<span class="actor">(.*?)</span><br/>', webpage, re.S)
    data_array = re.findall(r'">(.*?)</a>', data[0], re.S)
    FilmInfo["actor"] = data_array

    data = re.findall(r'<span class="pl">类型:(.*?)<br/>', webpage, re.S)
    data_array = re.findall(r'">(.*?)</span>', data[0], re.S)
    FilmInfo["type"] = data_array

    data = re.findall(r'<span class="pl">制片国家/地区:(.*?)/>', webpage, re.S)
    data_array = re.findall(r'>\s(.*?)<br', data[0], re.S)
    FilmInfo["producer-country"] = data_array

    data = re.findall(r'<span class="pl">语言:(.*?)/>', webpage, re.S)
    data_array = re.findall(r'>\s(.*?)<br', data[0], re.S)
    FilmInfo["laguage"] = data_array

    data = re.findall(r'<span class="pl">上映日期:(.*?)/>', webpage, re.S)
    data_array = re.findall(r'">(.*?)</span>', data[0], re.S)
    FilmInfo["release-time"] = data_array

    data = re.findall(r'<span class="pl">片长:(.*?)/>', webpage, re.S)
    data_array = re.findall(r'">(.*?)</span>', data[0], re.S)
    FilmInfo["film-length"] = data_array

    data = re.findall(r'<span class="pl">又名:(.*?)/>', webpage, re.S)
    print(data)
    data_array = re.findall(r'>\s(.*?)<br', data[0], re.S)
    FilmInfo["alias"] = data_array

    data = re.findall(r'<strong class="ll rating_num" property="v:average">(.*?)</strong>', webpage, re.S)
    FilmInfo["Scores"] = float(data[0])

    data = re.findall(r'<a href="collections" class="rating_people"><span property="v:votes">(.*?)</span>人评价</a>', webpage, re.S)
    FilmInfo["rating_people"] = int(data[0])

    data = re.findall(r'<span class="rating_per">(.*?)</span>', webpage, re.S)
    FilmInfo["rating_grate"] = data


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
