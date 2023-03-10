from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import os 
import requests
import urllib

class_name = "My favourite"
search_term = "Billie Elish"
Images_needed = 200

# #To run without browser opening
# op = webdriver.ChromeOptions()
# op.add_argument('headless')
# driver = webdriver.Chrome(options=op)
# driver.get("https://google.com")

#to open browser while running (we can visualize)
driver = webdriver.Chrome()
driver.get("https://google.com")

# box = driver.find_element("xpath",'//*[@id="APjFqb"]')
box = driver.find_element("xpath","/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
box.send_keys(search_term)
box.send_keys(Keys.ENTER)

try: 
    driver.find_element("xpath","//*[@id='hdtb-msb']/div[1]/div/div[2]/a").click()
except:
    driver.find_element("xpath",'//*[@id="cnt"]/div[5]/div/div/div/div[1]/div/a[2]').click()

starting_length = driver.execute_script("return document.body.scrollHeight")
finished_length = starting_length+1
Find_Images = True
while (starting_length != finished_length) & (Find_Images):
    starting_length = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    soup = BeautifulSoup(driver.page_source,"lxml")
    all_images = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
    try:
        all_images = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
        if len(all_images) <= Images_needed:
            time.sleep(5)
            finished_length = driver.execute_script("return document.body.scrollHeight")
        else:
            all_images = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
            Find_Images = False
    except Exception as e:
        print(f"the exception occured as: {e}")
print("finished_scrolling")

all_details = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
if len(all_details) == 0 :
    driver.find_element("xpath",'//*[@id="hdtb-msb"]/div[1]/div/div[3]/a').click()
    starting_length = driver.execute_script("return document.body.scrollHeight")
    finished_length = starting_length+1
    Find_Images = True
    while (starting_length != finished_length) & (Find_Images):
        starting_length = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        soup = BeautifulSoup(driver.page_source,"lxml")
        all_images = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
        try:
            all_images = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
            if len(all_images) <= Images_needed:
                time.sleep(5)
                finished_length = driver.execute_script("return document.body.scrollHeight")
            else:
                all_images = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
                Find_Images = False
        except Exception as e:
            print(f"the exception occured as: {e}")
    print("finished_scrolling")    
    all_details=soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")

soup = BeautifulSoup(driver.page_source,"lxml")

all_images = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")

import pandas as pd
index = int(len(all_images))

dataframe = pd.DataFrame(columns=["Blog_Link","Title","Source_Name"])

all_details=soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")

for detail in all_details[:Images_needed]:
    link_and_title = detail.find("a",class_="VFACy kGQAp sMi44c d0NI4c lNHeqe WGvvNb")
    link = link_and_title.get("href")
    title = link_and_title.get("title")
    source = link_and_title.find("div",class_="dmeZbb").text
    dataframe = pd.concat([dataframe,pd.DataFrame({dataframe.columns[0]:[link],dataframe.columns[1]:[title],
                                                    dataframe.columns[2]:[source]})],ignore_index=True)

path = os.path.join(os.getcwd(),f"{class_name}")
os.makedirs(path,exist_ok=True)  

dataframe["Images"] = None
for i,image_link in enumerate(all_images[:Images_needed]):
    imageurl = image_link.find("img",class_="rg_i Q4LuWd").get("src")
    alt_image_url = image_link.find("img",class_="rg_i Q4LuWd").get("data-src")
    try:
        dataframe.iloc[i,-1] = imageurl if imageurl != None else None
        urllib.request.urlretrieve(imageurl,f"{path}/{search_term}_image_{i}.jpg")
    except Exception as e:
        dataframe.iloc[i,-1] = alt_image_url if alt_image_url != None else None
        urllib.request.urlretrieve(alt_image_url,f"{path}/{search_term}image_{i}.jpg")
        pass

def path_to_image_html(path):
    return '<img src ="'+ path + '" width="120" >'

pd.set_option('colheader_justify', 'center')

dataframe.to_html(f"{search_term}_data.html",escape=False,formatters=dict(Images=path_to_image_html))

time.sleep(5)
print("Finished")

