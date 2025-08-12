#!/bin/env python3
import os

wallpaper_dir = "../../media"

# utils

def scan_dir():
  files = os.listdir(wallpaper_dir)
  for file in files:
    if not file.lower().startswith("konachan."):
      files.remove(file)
  return files

def print_list(l, prefix="- ", suffix=""):
  for e in l:
    print("{}{}{}".format(prefix, e, suffix))

# sides

def rename(file):
  file_old = file.split(' ')
  file_id = file_old[2]
  extension = file.split(".")[2]

  new_name = f"konachan_{file_id}.{extension}"

  os.rename(wallpaper_dir + "/" + file, wallpaper_dir + "/" + new_name)
  print("Renamed: " + new_name)

# main

def main():
  list_of_files = scan_dir()

  print("""This script will rename every file downloaded from konachan.* <- any domain, safe or explicit
  from the pattern(example): Konachan.net - 123456 tag1 tag2 tag3.jpg
  it will produce: konachan_123456.jpg
  This makes it easier to pull info about the post using my other script: auto_sidecard-kc.py
        """)

  print("These files will be processed: ")
  print_list(list_of_files)

  for _, file in enumerate(list_of_files):
    rename(file)

if __name__ == "__main__":
  main()