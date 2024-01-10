import requests
from bs4 import BeautifulSoup
import csv
import schedule
import time
import datetime

import re

def extract_numbers(text):
    numbers = re.findall(r'\d+\.\d+|\d+', text)
    if numbers:
        return float(numbers[0])
    else:
        return None

def mining():
    now = datetime.datetime.now()
    formatted_now = now.strftime("%d/%m/%Y %H:%M:%S")
    date = formatted_now

    url1 =  "https://www.iqair.com/th/thailand/bangkok/pathum-wan/pathumwan-district"
    url2 = "https://www.iqair.com/th/thailand/bangkok/pathum-wan/lumpini-park-pathumwan-district"
    url3 = "https://www.iqair.com/th/thailand/bangkok/the-royal-bangkok-sports-club"
    url4 = "https://www.iqair.com/th/thailand/nakhon-pathom/water-reservoir"
    url5 = "https://www.iqair.com/th/indonesia/south-sumatra/palembang/palembang-bukit-kecil"
    list_url = [url1,url2,url3,url4,url5]
    for url in list_url:
        req = requests.get(url)
        soup = BeautifulSoup(req.text,"html.parser")

        pm2_5 = soup.find("span",{"mattooltipposition":"below"}).text
        data = soup.find("div",{"class":"weather__detail"})
        data1 = data.find_all("td")
        data_record =[date,datetime.datetime.now().day,datetime.datetime.now().hour]
        for i in [3,7,5,9]:
            data_i = data.find_all("td")[i].text
            data_i = extract_numbers(data_i)
            data_record.append(data_i)
        data_record.append(pm2_5)
        
        for i in range(5):
            if list_url.index(url) == i:
                with open(file_csv[i],"a",newline="",encoding="utf-8")as f:
                    fw = csv.writer(f)
                    fw.writerow(data_record)
                    print(f"{data_record} stroed in {file_csv[i]}  ")
    print()

head =["Time","day","hour","Temperature(°C)","Wind Speed(km/hr.)","Moisture(%)","Pressure(millibars)","PM_2.5(µg/m^3)"]
file_csv = ["data_district.csv","data_lumpini.csv","data_rbs.csv","data_nk.csv","data_indo.csv"]

for file in file_csv:
    with open(file,"w",newline="",encoding="utf-8") as f:
        fw = csv.writer(f)
        fw.writerow(head)
    print(f"{file} created ")


def define_time():
    hour = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 0]
    if datetime.datetime.now().hour in range(24):
        if datetime.datetime.now().minute == 0:
            mining()

mining()
schedule.every(1).minutes.do(mining)

while True:
    schedule.run_pending()
    time.sleep(1)
