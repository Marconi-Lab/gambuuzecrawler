# Getting Started

## Prerequisites
The following must be installed on your PC.
- Python 3.6
- MongoDB (preferably v4.4)

## Project Setup
Follow the instructions below to setup the project for use.

1. Create a virutal environment.
   - Ubuntu
   ```python3.6 -m venv <path/to/virtual/environment>```
   - Windows
   ```python -m venv <path/to/virtual/environment```
2. Clone the project
   ```git clone https://github.com/Marconi-Lab/gambuuzecrawler.git```
3. Install requirments in virtual enviroment
   ```pip install -r requirements.txt```
4. Create a .env file in the root directory of the project. Populate it with the following variables:
  ```DATABASE_URL="<mongodb database URL>"  ```
  ```TARGET_URL="<URL for site to be crawled>"```

## Project execution
#### 1. Run the app.py file to begin crawling the site.
   ```python app.py```
   This will extract all the text from the site and store it in a database (gambuuze in mongoDB) in collections _lines_ and _linesLong_; _linesLong_ stores all lines longer than 14 words. Duplicate texts are not stored.
#### 2. Export CSV files.
  The bash shell script _generate\_csv.sh_ exports 2 CSV files (for long and short lines) for texts created on the current day directly from the mongoDB database using _mongoexport_. The exported files are stored in a _data_ directory in the root of the project.

  ```./path/to/generate_csv.sh```
  NB. This is currently implemented for Linux only
#### 3. BackUp
The bash shell script _gsutil.sh_ uploads the CSV files generated on the current day into the google cloud bucket _mldatastorge_ in a folder _gambuuze_auto_scraping_
gsutil must be installed on your system for this to work.
```./path/to/gsutil.sh```
NB. This is currently implemented for Linux only