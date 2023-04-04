from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import os,pathlib

from CUKU.util import util
from CUKU.constant import CLASS_NAME
from CUKU.logger import logging


def RUN(search_term:str,images_needed:int,backend):
    class_name = CLASS_NAME
    search_term = search_term
    
    Images_needed = images_needed

    logging.info(">>starting the chrome<<")
    print(">>starting the chrome<<")
    driver = util.get_google(webdriver=webdriver,backend=backend,safesearch_off=True)
    
    try:
        logging.info(">>entering the search term<<")
        print(">>entering the search term<<")
        time.sleep(1)
        driver = util.enter_search_term(driver=driver,search_term=search_term,Keys=Keys)
    except:
        if not pathlib.Path(f"templates/{search_term}_info.html").is_file():
            print(pathlib.Path(f"templates/{search_term}_info.html").is_file())
            driver.quit()
            RUN(search_term,images_needed,backend)
            print(">>running except section from enter_search_term<<")

    try:
        print(">>finding Images Needed<<")
        logging.info(f">>finding {images_needed} images<<")
        driver,all_images = util.Finding_All_The_Images(Images_needed, driver)
    except Exception as e:
        if not pathlib.Path(f"templates/{search_term}_info.html").is_file():
            print(pathlib.Path(f"templates/{search_term}_info.html").is_file())
            driver.quit()
            print(e)
            RUN(search_term,images_needed,backend)
            print(">>running except section from finding_all_the_images<<")
    
    logging.info(">>getting the page source(html)<<")
    soup = BeautifulSoup(driver.page_source,"lxml")

    all_images = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
    all_details = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
    
    logging.info(">>creating dataframe<<")
    print(">>creating dataframe<<")
    dataframe = util.create_dataframe_new(all_details,Images_needed)

    logging.info(">>created a directory(folder to store image)<<")    
    PATH = os.path.join("Collected_Data",CLASS_NAME,search_term)
    util.make_dir(PATH) 

    logging.info(">>storing all the info and saving the image in the directory<<")
    print(">>storing_info's<<")
    dataframe = util.create_dataframe_save_images(all_images,Images_needed,dataframe,search_term,PATH)

    logging.info(">>converting the dataframe into html<<")
    print(">>creating html<<")
    pd.set_option('colheader_justify', 'center')
    dataframe.to_html(f"templates/{search_term}_info.html",escape=False,formatters=dict(Images=util.path_to_image_html))

    logging.info("SUCCESSFULL-> from CUKU :) ")
    time.sleep(2)
    print("Got Everything You needed.")
    print("*"*20)
    return True

