# scraping-utils

#### tl;dr This is a set of tools to get tags of images from various sites

### Compatibility
- wallhaven.cc
- konachan.net/com*

**the script for konachan, makes request for the .com version - since it does not restrict explicit, and someone may need it.*

### Tools
> wallhaven/auto_sidecar-wh.py
- Requires: Python(tested with 3.13.3) and requests library.
 - Optionally requires putting an api key, if wish to access nsfw.
 - Uses wallhaven.cc api to get tags and purity, and then create a sidecard for every file in specified directory.
> konachan/auto_rename-kc.py
 - Requires: Python(tested with 3.13.3)
 - Renames files downloaded from konachan for use with auto_sidecar-kc.py
> konachan/auto_sidecar-kc.py
 - Requires: Python(tested with 3.13.3) and library beautifulsoup4
 - Uses BeautifulSoup to scrape konachan.com for tags and purity, and then create a sidecard for every file in specified directory.
 - Unfortunately, I could not find a way to get single post data using konachan's api. sry if there is a way and i'm dumb.

## Directory
Adjust the variable, `wallpaper_dir` to your needs.  
By default, it assumes you have cloned/unzipped this repo, and are running scripts from their original positions, with a directory called `media` being present next to this repo directory.  
So ***tl;dr***, it assumes this.
- `/media/` - media folder
- `/scraping-utils/` - this repo
- `/scraping-utils/wallhaven/auto_sidecar-wh.py` <- running this file from it's original position

## Timeout and Rate Limiting
Sidecar creators have 3 parameters that will space out requests so that you won't get rate limited.  
- `time_between_requests` controls sleep time before every request
- `timeout_time` specifies sleep time for when we do a timeout
- `timeout_request_count` specifies, every which request do we wait n seconds, so we don't get rate limited. (n being `timeout_time`).

For `wallhaven.cc`, it is stated that you can do 45 request per minute, so do that.  
I could not find such info for `konachan`, so I made it 12 requests ever 1s and then a 15s pause

## Background (boringg)
I love collecting data, segregating them, tagging them, measuring sizes, etc.  
And also I love hoarding. (okay that might be the same thing hehe)  

What's more, wallpapers and pfps have meanings for me, they are tied to certain timelines of my life.  
So, I like to keep sh*tton of them and sometimes swap.  

But there has been a problem, a big one - I have too many :<
That pushed me into organizing them, not based on folder structures - but on tags.
There is this project called [hydrus network](https://hydrusnetwork.github.io/hydrus/index.html), that helps you organize all your media into one big database, which you can search by tags. (and I need a db for my screenshots too.)

There is a function in hydrus to import a set of tags when importing files.
That is, by using something called *sidecar* files. (iirc it's late)
When you have a media file, let's say  `waterfall.jpg`, 
you can create a file `waterfall.jpg.txt`,  
that will contain a set of tags, for example `waterfall` `scenery` `landscape`, all separated by newlines.  
When choosing the import option, you can tell hydrus to get the sidecars, and it will add the tags alongside media.