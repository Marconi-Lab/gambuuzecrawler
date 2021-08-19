#!/bin/sh

TIME=$(date +"20""%y-%m-%d""T00:00:00.000Z")
DATE=$(date +"20""%y_%m_%d")
echo $TIME
echo $DATE

echo {\"date\": {\"\$gte\": {\"\$date\": \"$TIME\"}}} > ./query.json

mongoexport --db=gambuuze --collection=lines --fields=text --type=csv --queryFile=./query.json --out=./data/gambuuze_$DATE.csv
mongoexport --db=gambuuze --collection=linesLong --fields=text --type=csv --queryFile=./query.json --out=./data/gambuuze_$DATE"_long.csv"

