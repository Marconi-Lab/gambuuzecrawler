#!/bin/sh
PATH="$PATH":/snap/bin/gsutil
BOTO_CONFIG="/home/ben_wycliff/.boto"
HOME=/home/ben_wycliff
DATE=$(date +"20""%y_%m_%d")
DATE2=2021_08_18

/snap/bin/gsutil cp -r /home/ben_wycliff/scrape/gambuuzecrawler/data/gambuuze_$DATE.csv gs://mldatastorage/gambuuze_auto_scraping
/snap/bin/gsutil cp -r /home/ben_wycliff/scrape/gambuuzecrawler/data/gambuuze_$DATE\_long.csv gs://mldatastorage/gambuuze_auto_scraping
