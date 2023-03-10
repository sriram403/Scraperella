from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import os 
import requests
import urllib
import pandas as pd

from CUKU.util import util
from CUKU.constant import CLASS_NAME,PATH
from CUKU.logger import logging

def RUN(search_term,images_needed):
    class_name = CLASS_NAME
    
    search_term = search_term
    
    Images_needed = images_needed

    logging.info(">>starting the chrome<<")
    driver = util.get_google(webdriver=webdriver)
    logging.info(">>entering the search term<<")
    driver = util.enter_search_term(driver=driver,search_term=search_term,Keys=Keys)

    driver.find_element("xpath","//*[@id='hdtb-msb']/div[1]/div/div[2]/a").click()
    logging.info(f">>finding {images_needed} images<<")
    driver,all_images = util.Finding_All_The_Images(Images_needed, driver)
    
    logging.info(">>getting the page source(html)<<")
    soup = BeautifulSoup(driver.page_source,"lxml")

    all_images = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
    all_details = soup.find_all("div",class_="isv-r PNCib MSM1fd BUooTd")
    
    logging.info(">>creating dataframe<<")
    dataframe = util.create_dataframe_new(all_details,Images_needed)

    logging.info(">>created a directory(folder to store image)<<")    
    path = PATH

    util.make_dir() 

    logging.info(">>storing all the info and saving the image in the directory<<")
    dataframe = util.create_dataframe_save_images(all_images,Images_needed,dataframe,search_term)

    logging.info(">>converting the dataframe into html<<")
    pd.set_option('colheader_justify', 'center')

    dataframe.to_html(f"{search_term}_info.html",escape=False,formatters=dict(Images=util.path_to_image_html))
    
    logging.info("SUCCESSFULL-> from cuku (づ￣ 3￣)づ ")
    time.sleep(5)
    print("Finished")


