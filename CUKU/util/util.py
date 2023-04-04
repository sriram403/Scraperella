import time
from bs4 import BeautifulSoup
from CUKU.constant import CHROME_DRIVER_LOC,FORMAT,COLUMN_1,COLUMN_2,COLUMN_3,COLUMN_4
import urllib
import os
import pandas as pd
from CUKU.logger import logging

def path_to_image_html(path):
    return '<img src ="'+ path + '" width="120" >'

def Finding_All_The_Images(Images_needed, driver):
    driver.find_element("xpath","//*[@id='hdtb-msb']/div[1]/div/div[2]/a").click()
    soup = BeautifulSoup(driver.page_source,"lxml")
    all_details = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
    logging.info(f">>checking the all details length which is ->: {len(all_details)}")
    if len(all_details) != 0:
        print("got the image tab")
        logging.info("got the image tab right away") 
        starting_length = driver.execute_script("return document.body.scrollHeight")
        finished_length = starting_length + 1
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
                return driver,all_images
            except Exception as e:
                print(f"the exception occured as: {e}")
        print("finished_scrolling")
        return driver,all_images
    else:
        logging.info("didn't get the image so checking the near tab")
        print(">>changing into next tab to check for images<<")
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
        return driver,all_images
    
def get_google(webdriver,backend):
    if backend == True:
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_LOC,options=op)
        driver.get("https://google.com")

    else:
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_LOC)
        driver.get("https://google.com")
    return driver

def enter_search_term(driver,search_term,Keys):
    try:
        time.sleep(1)
        box = driver.find_element("xpath","/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
    except:
        box = driver.find_element("xpath",'//*[@id="APjFqb"]')
    box.send_keys(search_term)
    box.send_keys(Keys.ENTER)
    return driver

def make_dir(PATH):
    os.makedirs(PATH,exist_ok=True) 

def create_dataframe_save_images(all_images,Images_needed,dataframe,search_term,PATH):
    for i,image_link in enumerate(all_images[:Images_needed]):
        imageurl = image_link.find("img",class_="rg_i Q4LuWd").get("src")
        alt_image_url = image_link.find("img",class_="rg_i Q4LuWd").get("data-src")
        try:
            dataframe.iloc[i,-1] = imageurl if imageurl != None else None
            urllib.request.urlretrieve(imageurl,f"{PATH}/{search_term}_image_{i}.{FORMAT}")
        except Exception as e:
            dataframe.iloc[i,-1] = alt_image_url if alt_image_url != None else None
            urllib.request.urlretrieve(alt_image_url,f"{PATH}/{search_term}image_{i}.{FORMAT}")
    return dataframe

def create_dataframe_new(all_details,Images_needed):
    dataframe = pd.DataFrame(columns=[COLUMN_1,COLUMN_2,COLUMN_3,COLUMN_4])
    dataframe[COLUMN_4] = None

    for detail in all_details[:Images_needed]:
        link_and_title = detail.find("a",class_="VFACy kGQAp sMi44c d0NI4c lNHeqe WGvvNb")
        link = link_and_title.get("href")
        title = link_and_title.get("title")
        source = link_and_title.find("div",class_="dmeZbb").text
        dataframe = pd.concat([dataframe,pd.DataFrame({dataframe.columns[0]:[link],dataframe.columns[1]:[title],
                                                    dataframe.columns[2]:[source]})],ignore_index=True)
    return dataframe


