# -*- coding: utf-8 -*-
"""
Spyder Editor

This is spyder file.
"""


import urllib
import re
import sqlite3 as sql
import csv

def crawling(url, user_agent='wswp', retries=2):
    print("Downloading:", url)
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)

    try:
        html = urllib.request.urlopen(request).read()
    except urllib.error.URLError as e:
        print("Downloading error reason:%s, code:%d" %(e.reason,e.code))
        html = None
        if retries > 0:
            if hasattr(e,'code') and 500 <= e.code < 600:
                crawling(url, retries-1)
    return html

def web_process(webpage, target_id):

    FilmInfo = {}

    data = re.findall(r'<span class="rec" id="电影.*?">',webpage)
    if data:
        data_array = re.split(r'<|=|\s|-|"', data[0])
        if data_array:
            film_id = data_array[9]
            FilmInfo["id"]=int(film_id)
        else:
            FilmInfo["id"]=target_id
    else:
        FilmInfo["id"]=target_id

    data = re.findall(r'<title>.*?</title>', webpage, re.S)
    if data:
        data_array = data[0].split()
        film_name = data_array[1]
        FilmInfo["name"] = film_name
    else:
        FilmInfo["name"] = None

    data = re.findall(r'<span class="year">\((.*?)\)</span>', webpage, re.S)
    if data:
        FilmInfo["date"] = int(data[0])
    else:
        FilmInfo["date"] = None

    data = re.findall(r'rel="v:directedBy">(.*?)</a>', webpage, re.S)
    if data:
        FilmInfo["directeBy"] = data
    else:
        FilmInfo["directeBy"] = None

    data = re.findall(r'''<span ><span class='pl'>编剧</span>: <span class='attrs'>(.*?)</span><br/>''', webpage, re.S)
    if data:
        data_array = re.findall(r'>(.*?)</a>', data[0], re.S)
        if data_array:
            FilmInfo["scriptwriter"] = data_array
        else:
            FilmInfo["scriptwriter"] = None
    else:
        FilmInfo["scriptwriter"] = None

    data = re.findall(r'<span class="actor">(.*?)</span><br/>', webpage, re.S)
    if data:
        data_array = re.findall(r'">(.*?)</a>', data[0], re.S)
        if data_array:
            FilmInfo["actor"] = data_array
        else:
            None
    else:
        FilmInfo["actor"] = None

    data = re.findall(r'<span class="pl">类型:(.*?)<br/>', webpage, re.S)
    if data:
        data_array = re.findall(r'">(.*?)</span>', data[0], re.S)
        if data_array:
            FilmInfo["type"] = data_array
        else:
            FilmInfo["type"] = None
    else:
        FilmInfo["type"] = None

    data = re.findall(r'<span class="pl">制片国家/地区:(.*?)/>', webpage, re.S)
    if data:
        data_array = re.findall(r'>\s(.*?)<br', data[0], re.S)
        if data:
            FilmInfo["producer-country"] = data_array
        else:
            FilmInfo["producer-country"] = None
    else:
        FilmInfo["producer-country"] = None

    data = re.findall(r'<span class="pl">语言:(.*?)/>', webpage, re.S)
    if data:
        data_array = re.findall(r'>\s(.*?)<br', data[0], re.S)
        if data_array:
            FilmInfo["laguage"] = data_array
        else:
            FilmInfo["laguage"] = None
    else:
        FilmInfo["laguage"] = None

    data = re.findall(r'<span class="pl">上映日期:(.*?)/>', webpage, re.S)
    if data:
        data_array = re.findall(r'">(.*?)</span>', data[0], re.S)
        if data_array:
            FilmInfo["release-time"] = data_array
        else:
            FilmInfo["release-time"] = None
    else:
        FilmInfo["release-time"] = None

    data = re.findall(r'<span class="pl">片长:(.*?)/>', webpage, re.S)
    if data:
        data_array = re.findall(r'">(.*?)</span>', data[0], re.S)
        if data_array:
            FilmInfo["film-length"] = data_array
        else:
            FilmInfo["film-length"] = None
    else:
        FilmInfo["film-length"] = None

    data = re.findall(r'<span class="pl">又名:(.*?)/>', webpage, re.S)
    if data:
        data_array = re.findall(r'>\s(.*?)<br', data[0], re.S)
        if data_array:
            FilmInfo["alias"] = data_array
        else:
            FilmInfo["alias"] = None
    else:
        FilmInfo["alias"] = None

    data = re.findall(r'<strong class="ll rating_num" property="v:average">(.*?)</strong>', webpage, re.S)
    if data[0]:
        FilmInfo["Scores"] = float(data[0])
    else:
        FilmInfo["Scores"] = None

    data = re.findall(r'<a href="collections" class="rating_people"><span property="v:votes">(.*?)</span>人评价</a>', webpage, re.S)
    if data[0]:
        FilmInfo["rating_people"] = int(data[0])
    else:
        FilmInfo["rating_people"] = None

    data = re.findall(r'<span class="rating_per">(.*?)</span>', webpage, re.S)
    if data:
        FilmInfo["rating_per"] = data
    else:
        FilmInfo["rating_per"] = None

    data = re.findall(r'&action=">(.*?)</a><br/>', webpage, re.S)
    if data:
        FilmInfo["rating_betterthan"] = data
    else:
        FilmInfo["rating_betterthan"] = None

    return FilmInfo

def main():

    with open('film.csv', 'w') as csvfile:
        fieldnames = ['id', 'name', 'date', 'directeBy', 'scriptwriter', 'actor', 'type', 'producer-country', 'laguage',
                'release-time', 'film-length', 'alias', 'Scores', 'rating_people', 'rating_per', 'rating_betterthan']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        #url="https://movie.douban.com/subject/27038183/?from=showing"

        start_url = "https://movie.douban.com/subject/"
        start_id = 26000000
        #start_id = 27038209
        id = start_id

        for i in range(100000):
            id = start_id+i
            url = start_url + str(id)

            print("The url:", url)
            html = crawling(url)
            if html is None:
                continue

            webpage = html.decode("utf-8")
            #print(html)

            #print(type(html))
            #print(type(webpage))
            #print(webpage)
            #f = open("movie.html","w", encoding='utf-8')
            #f.write(str(webpage))
            #f.close()

            data = web_process(webpage,id)

            writer.writerow(data)

    with open('film.csv', 'r') as rcsvfile:
        reader = csv.DictReader(rcsvfile)
        for row in reader:
            #print("The row data:", row)
            print("The film info:", row['id'], row['name'], row['date'])

if __name__=="__main__":
    main()
