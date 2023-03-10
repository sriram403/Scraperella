from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

from CUKU.util import util
from CUKU.constant import CLASS_NAME
from CUKU.logger import logging

def RUN(search_term:str,images_needed:int,backend):
    class_name = CLASS_NAME
    
    search_term = search_term
    
    Images_needed = images_needed

    logging.info(">>starting the chrome<<")
    print(">>starting the chrome<<")
    driver = util.get_google(webdriver=webdriver,backend=backend)
    
    logging.info(">>entering the search term<<")
    print(">>entering the search term<<")
    time.sleep(2)
    driver = util.enter_search_term(driver=driver,search_term=search_term,Keys=Keys)

    logging.info(f">>finding {images_needed} images<<")
    driver,all_images = util.Finding_All_The_Images(Images_needed, driver)
    
    logging.info(">>getting the page source(html)<<")
    soup = BeautifulSoup(driver.page_source,"lxml")

    all_images = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
    all_details = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
    
    logging.info(">>creating dataframe<<")
    print(">>creating dataframe<<")
    dataframe = util.create_dataframe_new(all_details,Images_needed)

    logging.info(">>created a directory(folder to store image)<<")    

    PATH = os.path.join(CLASS_NAME,search_term)
    util.make_dir(PATH) 

    logging.info(">>storing all the info and saving the image in the directory<<")
    print(">>storing_info's<<")
    dataframe = util.create_dataframe_save_images(all_images,Images_needed,dataframe,search_term,PATH)

    logging.info(">>converting the dataframe into html<<")
    print(">>creating html<<")
    pd.set_option('colheader_justify', 'center')

    dataframe.to_html(f"{search_term}_info.html",escape=False,formatters=dict(Images=util.path_to_image_html))
    
    logging.info("SUCCESSFULL-> from CUKU :) ")
    time.sleep(5)
    print("Got Everything You needed.")


