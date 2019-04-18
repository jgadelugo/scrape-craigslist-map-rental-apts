import requests
from csv import DictWriter
from time import sleep
import json
import time

BASE_URL1 = "https://newhaven.craigslist.org"

# Scrapes website
def scrape_apts():
    Apt_Data =[]
    count = 0
    URL = f"https://newhaven.craigslist.org/jsonsearch/apa/?search_distance=8&availabilityMode=0&sale_date=all+dates&map=1"
    apts = requests.get(f"{URL}").json()[0]
    sleep(1)
    for apt in apts:
        if "GeoCluster" in apt:
            url1 = apt["url"]
            Geo_apts = requests.get(f"{BASE_URL1}{url1}").json()[0]
            sleep(.25)
            for Geo_apt in Geo_apts:
                Apt_Data += append_Data(Geo_apt)
                count += 1
                print(count)
        else:
            Apt_Data += append_Data(apt)
            count +=1
            print(count)
        
    print(f"{count} New Haven apartment data collected.")
    return write_apts(Apt_Data)

def append_Data(apt):
    data = []
    data.append({
        "Price": get_Price(apt),
        "Bedrooms": get_Bedrooms(apt),
        "Latitude": get_Latitude(apt),
        "Longitude": get_Longitude(apt),
        "Title": get_title(apt),
        "PostedDate": get_PostedDate(apt),
        "PostingID": get_PostingID(apt),
        "URL": get_URL(apt)
    })
    return data

def write_apts(Apt_Data):
    file_name = "New_Haven_Craig_8MI"
    with open(f"{file_name}.csv", "a", encoding='utf-8') as file:
        headers = ["Price","Bedrooms","Latitude","Longitude", "Title",
                   "PostedDate", "PostingID","URL"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for apt in Apt_Data:
            csv_writer.writerow(apt)
    return print(f"apts added to {file_name}.csv.")
    
def get_Price(apt):
    try:
        Total = apt["Ask"]
    except:
        Total = 0
    return Total

def get_Bedrooms(apt):
    try:
        Bedrooms = apt["Bedrooms"]
    except:
        Bedrooms = 0
    return Bedrooms

def get_Latitude(apt):
    try:
        Latitude = apt["Latitude"]
    except:
        return "None"
    return Latitude

def get_Longitude(apt):
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


def get_PostedDate(apt):
    try:
        PostedDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(apt["PostedDate"])))
        print(PostedDate)
    except:
        return "None"
    return PostedDate


def get_PostingID(apt):
    try:
        PostingID = apt["PostingID"]
    except:
        return "None"
    return PostingID


def get_URL(apt):
    try:
        apt_url = apt["PostingURL"]
    except:
        return "None"
    return apt_url


scrape_apts()
