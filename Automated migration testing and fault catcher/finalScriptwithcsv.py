# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 22:53:15 2019

@author: vijay
"""

import csv
from selenium import webdriver
import time
from PIL import Image as img

#def to read csv and extract source and destination urls
def readcsv():
    with open('datasets/urls.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        global source
        global destination
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t Source url: {row[0]} and Destination url: {row[1]}.')
                source[line_count] = row[0]
                destination[line_count] = row[1]
                line_count += 1
        print(f'Processed {line_count} lines.')
    
    
#def for getting urls screenshots and comapring for difference
#for source urls to get screenshots
def runurls(source, destination):
    with webdriver.Firefox() as driver:
        for linksource in source:
            sourcedata = {'output': 'Screenshots/source'+str(linksource)+'.png',
                       'width': 2200,
                       'height': 1800}
            
            #linkWithProtocol = 'https://' + str(link)
            slink = source[linksource]
            # set the window size for desktop
            driver.maximize_window()
            driver.get(slink)
            time.sleep(2)
            firefox_elem = driver.find_element_by_tag_name('body')
            firefox_elem.screenshot(sourcedata['output'])
            #print(desktop['output'])
       
        
        for linkdestin in destination:
            destidata = {'output': 'Screenshots/destination'+str(linkdestin)+'.png',
                       'width': 2200,
                       'height': 1800}
            
            #linkWithProtocol = 'https://' + str(link)
            dlink = destination[linkdestin]
            # set the window size for desktop
            driver.maximize_window()
            driver.get(dlink)
            time.sleep(2)
            firefox_elem = driver.find_element_by_tag_name('body')
            firefox_elem.screenshot(destidata['output'])
            #print(desktop['output'])
            
            
#def to compare images to calculate differnce
def caldiff(source):
    for image in source:
        i1 = img.open("Screenshots/source"+str(image)+".png")
        i2 = img.open("Screenshots/destination"+str(image)+".png")
        assert i1.mode == i2.mode, "Different kinds of images."
        assert i1.size == i2.size, "Different sizes."
         
        pairs = zip(i1.getdata(), i2.getdata())
        if len(i1.getbands()) == 1:
            # for gray-scale jpegs
            dif = sum(abs(p1-p2) for p1,p2 in pairs)
        else:
            dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
         
        ncomponents = i1.size[0] * i1.size[1] * 3
        print("Difference (percentage) for page"+str(image)+":", (dif / 255.0 * 100) / ncomponents)
            
            
#call to functions
readcsv()
runurls(source, destination)
caldiff(source)
