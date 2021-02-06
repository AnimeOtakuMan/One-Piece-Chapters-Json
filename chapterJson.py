from bs4 import BeautifulSoup
from urllib.request import urlopen
from Chapter import Chapter
import time
import os
import requests
import json

start = time.time()

url = "http://mangafox.icu/manga/one-piece"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

page = urlopen(url)

html = page.read().decode("utf-8")

soup = BeautifulSoup(html, "html.parser")

chapter_list_element = soup.find_all("div", {"class":"chapter-list"})

soup = BeautifulSoup(str(chapter_list_element[0]), "html.parser")

chapters_rows_element = soup.find_all("div", {"class":"row"})

chapters = []

for chapter_item in chapters_rows_element:
    soup = BeautifulSoup(str(chapter_item), "html.parser")
    chapter = Chapter(soup.find_all("a")[0].string, soup.find_all("a")[0].get("href"))

    page = urlopen(chapter.chapter_url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    chapter_images = []
    chapter_images_element = soup.find_all("p", {"id":"arraydata"})[0].string

    chapter_image_urls = chapter_images_element.string.split(",")
    chapter.set_image_urls(chapter_image_urls)
    chapters.append(chapter)

chapter_list_json = json.dumps([chapter.__dict__ for chapter in chapters])

f = open("chapter_json.txt", "w")
f.write(chapter_list_json)
f.close()
end = time.time()
print("Time Elapsed")
# Takes like 53 minutes
print(end - start)