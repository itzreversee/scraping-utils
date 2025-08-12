#!/bin/env python3
import requests
import time
import os

# key here          \/
wallhaven_api_key = ""
wallhaven_api_url = "https://wallhaven.cc/api/v1/w/{}?apikey={}"

wallpaper_dir = "../../media"

# rate limit is 45 per minute!
# so just to be safe, we'll do 44, with 1 every second and 16s of timeout
# that should give us 61 seconds?
# should have just made it 30 requests, 30 pause. or make it so it does request every 1.5? or 2 and no rate limit??? ugh too lazy!!

time_between_requests = 1
timeout_time = 16
timeout_request_count = 44 # every x request, we will wait, to not to get stopped by api

# free to adjust!!
tag_translation = {
  "sfw": "safe",
  "sketchy": "questionable",
  "nsfw": "unsafe",
}

# utils

def get_wallpaper_info(id):
  time.sleep(time_between_requests)
  url = wallhaven_api_url.format(id, wallhaven_api_key)
  req = requests.get(url=url)
  data = req.json()

  data = data["data"]

  tags = data["tags"]
  parsed_tags = []

  for tag in tags:
    parsed_tags.append(extract_tag(tag))

  parsed_tags.append("purity:" + tag_translation.get(data["purity"]))

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
  sfiles = []
  files = os.listdir(wallpaper_dir)
  for file in files:
    if file.startswith("wallhaven-"):
      sfiles.append(file)
  return sfiles

def print_list(l, prefix="- ", suffix=""):
  for e in l:
    print("{}{}{}".format(prefix, e, suffix))

# sides

def create_sidecar(file):
  print("Creating sidecar for " + file)
  wallpaper_id = file[10:-4]
  tags = get_wallpaper_info(wallpaper_id)
  sidecard_file_name = file + ".txt"
  write_tags(sidecard_file_name, tags)

# main

def main():
  list_of_files = scan_dir()

  print("""This script will scan every file named: wallhaven-<id>.<ext>
and use wallhaven.cc's api to get tags and purity.
then put these, separated by newlines, in a sidecar file named the same as original, but with a txt extension at the end, 
so for example: wallhaven-123456.png.txt <- the sidecar file
Please note, that to query nsfw posts, you need to specify the api key!
You can do that at the top of the file.
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