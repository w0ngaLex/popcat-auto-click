# -*- mode: python; coding: utf-8 -*-

import multiprocessing as mp
from functools import partial
from selenium import webdriver
import threading
import time
import os
import json

chromedriver = "./chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
div = '//*[@id="app"]'
delay = 0.055
drives = 5
mute = True

def job(num, chrome_options, delay):
    time.sleep(num)
    driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
    driver.set_window_size(500, 400)
    driver.set_window_position(350*(num%5)-10, 250*(num//5), windowHandle='current')
    driver.get('https://popcat.click/')
    js = "var event = new KeyboardEvent('keydown',{key:'g',ctrlKey:true});setInterval(function(){document.dispatchEvent(event);},"+str(delay * 1000)+");"
    driver.execute_script(js)
    while(True):
        time.sleep(99999)

def multicore(chrome_options, delay, drives):
    pool = mp.Pool()
    res = pool.map(partial(job, chrome_options=chrome_options, delay=delay), range(drives))
    pool.close()
    pool.join()
    
def main():
    global chrome_options, chromedriver, delay, drives
    print("Start.")
    if os.path.isfile('setting.json'):
        file = open('setting.json')
        setting = json.load(file)
        if 'chromedriver' in setting:
            chromedriver = setting['chromedriver']
        if 'delay' in setting:
            delay = setting['delay']
        if 'drives' in setting:
            drives = setting['drives']
        if 'mute' in setting:
            mute = setting['mute']
    if mute:
        chrome_options.add_argument("--mute-audio")
    if os.path.isfile(chromedriver):
        multicore(chrome_options, delay, drives)
    else:
        print("Can not found: ", chromedriver)
        input("Press any key to continue")
    

if __name__=='__main__':
    multiprocessing.freeze_support()
    main()
    input("Press any key to continue")
