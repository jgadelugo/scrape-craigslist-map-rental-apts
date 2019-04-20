import requests
import sqlite3
from csv import DictWriter
from time import sleep
import json
import time

BASE_URL1 = "https://newhaven.craigslist.org"

# Scrapes website
def scrape_apts():
    apt_data =[]
    count = 0
    URL = f"https://newhaven.craigslist.org/jsonsearch/apa/?search_distance=8&availabilityMode=0&sale_date=all+dates&map=1"
    apts = requests.get(f"{URL}").json()[0]
    sleep(1)
    for apt in apts:
        if "GeoCluster" in apt:
            url1 = apt["url"]
            geo_apts = requests.get(f"{BASE_URL1}{url1}").json()[0]
            sleep(.25)
            for geo_apt in geo_apts:
                data = (get_posting_id(geo_apt), get_title(geo_apt), get_bedrooms(geo_apt), get_price(
                    geo_apt), get_posted_date(geo_apt), get_latitude(geo_apt), get_longitude(geo_apt), get_url(geo_apt))
                apt_data.append(data)
                count += 1
                print(count)
        else:
            data = (get_posting_id(apt), get_title(apt), get_bedrooms(apt), get_price(
                apt), get_posted_date(apt), get_latitude(apt), get_longitude(apt), get_url(apt))
            apt_data.append(data)
            count +=1
            print(count)
    print(f"{count} New Haven apartment data collected.")
    return save_apts(apt_data)


def append_data(apt):
    data = []
    data.append({
        "PostingID": get_posting_id(apt),
        "Title": get_title(apt),
        "Bedrooms": get_bedrooms(apt),
        "Price": get_price(apt),
        "PostedDate": get_posted_date(apt),
        "Latitude": get_latitude(apt),
        "Longitude": get_longitude(apt),
        "URL": get_url(apt)
    })
    return data
# Creates apts.db -> creates apts table -> inserts values ; if table is already created comment out CREATE TABLE
def save_apts(all_apts):
    connection = sqlite3.connect("NewHaven_8_Miles.db")
    c = connection.cursor()
    #Table already created
    #c.execute(''' CREATE TABLE apts
    #    (ID INTEGER, Title TEXT, BRS INTEGER , Price REAL, PostedDate SMALLDATETIME, Latitude INTEGER, Longitude INTEGER, URL TEXT)''')
    c.executemany("INSERT INTO apts VALUES (?,?,?,?,?,?,?,?)", all_apts)
    connection.commit()
    connection.close()

def write_apts(apt_data):
    file_name = "New_Haven_Craig_8MI"
    with open(f"{file_name}.csv", "a", encoding='utf-8') as file:
        headers = ["Price","Bedrooms","Latitude","Longitude", "Title",
                   "PostedDate", "PostingID","URL"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for apt in apt_data:
            csv_writer.writerow(apt)
    return print(f"apts added to {file_name}.csv.")
    
def get_price(apt):
    try:
        Total = apt["Ask"]
    except:
        Total = 0
    return Total

def get_bedrooms(apt):
    try:
        Bedrooms = apt["Bedrooms"]
    except:
        Bedrooms = 0
    return Bedrooms

def get_latitude(apt):
    try:
        Latitude = apt["Latitude"]
    except:
        return "None"
    return Latitude

def get_longitude(apt):
    try:
        Longitude = apt["Longitude"]
    except:
        return "None"
    return Longitude

def get_title(apt):
    try:
        title = apt["PostingTitle"]
    except:
        return "None"
    return title


def get_posted_date(apt):
    try:
        PostedDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(apt["PostedDate"])))
    except:
        return "None"
    return PostedDate


def get_posting_id(apt):
    try:
        PostingID = apt["PostingID"]
    except:
        return "None"
    return PostingID


def get_url(apt):
    try:
        apt_url = apt["PostingURL"]
    except:
        return "None"
    return apt_url


scrape_apts()
