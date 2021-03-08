from bs4 import BeautifulSoup
from urllib.request import urlopen
from Chapter import Chapter
import time
import os
import requests
import json

start = time.time()

url = "https://onepiecechapters.com/"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

page = urlopen(url)

html = page.read().decode("utf-8")

soup = BeautifulSoup(html, "html.parser")

chapter_list_element = soup.find_all("table", {"class":"chap-tab"})

soup = BeautifulSoup(str(chapter_list_element[0]), "html.parser")

chapters_rows_element = soup.find_all("tr")

with open('chapter_json.json') as json_file:
    chapters_dict_list = json.load(json_file)

most_recent_chapter_local = chapters_dict_list[0]['chapter_number']

chapters = []
for chapter_dict in chapters_dict_list:
    chapter = Chapter(chapter_dict['chapter_number'], chapter_dict['chapter_url'])
    chapter.set_image_urls(chapter_dict['image_urls'])
    chapters.append(chapter)

for chapter_item in chapters_rows_element:
    soup = BeautifulSoup(str(chapter_item), "html.parser")
    chapter_number = soup.find_all("a")[0].string
    if (chapter_number == most_recent_chapter_local):
        break
    chapter = Chapter(chapter_number, soup.find_all("a")[0].get("href"))

    page = urlopen(chapter.chapter_url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    chapter_images = []
    chapter_images_elements = soup.find_all("div", {"class":"img_container"})

    chapter_image_urls = []
    for chapter_image_elems in chapter_images_elements:
        soup = BeautifulSoup(str(chapter_image_elems), "html.parser")
        chapter_image_url = soup.find_all("img")[0].get("src")
        chapter_image_urls.append(chapter_image_url)
    chapter.set_image_urls(chapter_image_urls)
    chapters.insert(0, chapter)

chapter_list_json = json.dumps([chapter.__dict__ for chapter in chapters])

f = open("chapter_json.json", "w")
f.write(chapter_list_json)
f.close()
end = time.time()
print("Time Elapsed")
# Takes like 53 minutes
print(end - start)