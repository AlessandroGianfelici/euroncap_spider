# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os
from datetime import datetime
import time 
from functions import parse_car

def file_folder_exists(path: str):
    """
    Return True if a file or folder exists.

    :param path: the full path to be checked
    :type path: str
    """
    try:
        os.stat(path)
        return True
    except:
        return False

def select_or_create(path: str):
    """
    Check if a folder exists. If it doesn't, it create the folder.

    :param path: path to be selected
    :type path: str
    """
    if not file_folder_exists(path):
        os.makedirs(path)
    return path


class MySpider(CrawlSpider):
    name = 'gspider'
    allowed_domains = ['euroncap.com']
    start_urls = [r'https://www.euroncap.com/en/']
    rules = (# Extract and follow all links!
        Rule(LinkExtractor(), callback='parse_item', follow=True), )
               
    def parse_item(self, response):
        if "en/results" in response.url:
            outpath = select_or_create("data")
            parsed_car = parse_car(response.body)
            filename = f"{parsed_car['Car Name'][0].replace(' ', '_')}.csv"
            if len(parsed_car)>0:
                parsed_car.to_csv(os.path.join(outpath, filename), index=0)
        self.log('crawling'.format(response.url))
