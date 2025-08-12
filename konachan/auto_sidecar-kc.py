#!/bin/env python3
from bs4 import BeautifulSoup

import requests
import time
import os

# .com will show [[EVERY]] post, so we'll use that.
konachan_api_url = "https://konachan.com/post/show/{}"

wallpaper_dir = "../../media"

# rate limit is ... idk
time_between_requests = 1
timeout_time = 15
timeout_request_count = 12

# free to adjust!!
tag_translation = {
  "safe": "safe",
  "questionable": "questionable",
  "explicit": "unsafe",
}

# utils

def get_wallpaper_info(id):
  time.sleep(time_between_requests)
  url = konachan_api_url.format(id, konachan_api_url)
  req = requests.get(url=url)

  soup = BeautifulSoup(req.content, 'html.parser')

  content_tags = soup.find('ul', id="tag-sidebar")

  parsed_tags = []

  if content_tags:
    for tag in content_tags.find_all("li"):
      parsed_tags.append(tag.get("data-name"))
  else:
    pass
  
  content_rating = soup.find("div", id="stats")
  content_rating = content_rating.find("ul")
  content_rating = content_rating.find_all("li")
  rating_str = ""
  for li in content_rating:
    li = li.get_text(strip=True)
    if li.startswith("Rating"):
      rating = li.split(' ')
      rating = rating[1].lower()
      rating_str = f"purity:{tag_translation.get(rating)}"
      break

  parsed_tags.append(rating_str)

  return parsed_tags

def extract_tag(tag):
  tag_name = str(tag["name"])
  tag_name = tag_name.lower()
  tag_name = '_'.join(tag_name.split(' '))
  return tag_name

def write_tags(file_name, tags):
  data = '\n'.join(tags)
  with open(wallpaper_dir + "/" + file_name, "w") as f:
    f.write(data)

def scan_dir():
  files = os.listdir(wallpaper_dir)
  for file in files:
    if file.endswith(".txt"):
      files.remove(file)
    if not file.startswith("konachan_"):
      files.remove(file)
  return files

def print_list(l, prefix="- ", suffix=""):
  for e in l:
    print("{}{}{}".format(prefix, e, suffix))

# sides

def create_sidecar(file):
  print("Creating sidecar for " + file)
  wallpaper_id = file[9:-4]
  tags = get_wallpaper_info(wallpaper_id)
  sidecard_file_name = file + ".txt"
  write_tags(sidecard_file_name, tags)

# main

def main():
  list_of_files = scan_dir()

  print("""This script will scan every file named: konachan_<id>.<ext>
and scrape konachan.com to get tags and purity.
then put these, separated by newlines, in a sidecar file named the same as original, but with a txt extension at the end, 
so for example: konachan_123456.png.txt <- the sidecar file
        """)

  print("These files will be processed: ")
  print_list(list_of_files)

  for i, file in enumerate(list_of_files):
    # i want it to not wait at the start of the script, so i add 1 to i.
    if (i+1) % timeout_request_count == 0:
      print("Waiting for " + str(timeout_time) + "s, to not to get rate limited")
      time.sleep(timeout_time)
    create_sidecar(file)

if __name__ == "__main__":
  main()