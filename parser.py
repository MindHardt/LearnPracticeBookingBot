from datetime import date
import time
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import date
import re
from multiprocessing.dummy import Pool
from tqdm import tqdm
import json

#https://hotel.tutu.ru/
#20 records_per_page
#lenta

headers2 = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'}
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

class Parser:
    base_url: str
    max_records: int
    records_per_page: int

    def parse(dest: str, checkin: date, checkout: date, hotels_quantity: int):
        pass

    

class BookingParser(Parser): 
    base_url = 'https://www.booking.com/searchresults.ru.html'
    max_records = 100
    records_per_page = 25

    #генерирует ссылку для букинга
    def __generate_url(self, dest: str, checkin: date, checkout: date):
        new_url = self.base_url + "?" + urlencode(
            {
                "ss": dest,
                "checkin_year": checkin.year,
                "checkin_month": checkin.month,
                "checkin_monthday": checkin.day,
                "checkout_year": checkout.year,
                "checkout_month": checkout.month,
                "checkout_monthday": checkout.day,
                "no_rooms": 1,
                "offset": 0
            }
        )
        return new_url

    #список ссылок на отели
    def __get_hotel_urls(self, url_to_parse: str, hotels_quantity: int = 10): #for booking
        #empty url list
        hotel_urls = []
        #счетчик отелей
        item_counter = 0
        #отступ для url
        for i in range(0, self.max_records, self.records_per_page):   #переход по страницам
            #изменяю url на другую страницу
            url_to_parse = re.sub('offset=\d+', 'offset=' + i.__str__(), url_to_parse)
            #soup страницы с отелями
            soup = BeautifulSoup(requests.get(url_to_parse,headers=headers).content, 'html.parser')

            for item in soup.find_all('div', 'd20f4628d0'): #going through hotel records/переход по блокам отелей
                #extract url
                hotel_url = item.find('a', 'e13098a59f').get('href') #hotel url
                #add to list
                hotel_urls.append(hotel_url)
                #increment counter
                item_counter += 1
                #stop if enougth
                if(item_counter == hotels_quantity):
                    break
            if(item_counter == hotels_quantity):
                break
        return hotel_urls

    #извлекает данные об отеле по ссылке
    def __get_hotel_data(self, url):   #booking
        hotel_soup = BeautifulSoup(requests.get(url,headers=headers).content, 'html.parser')
        #name //*[@id="hp_hotel_name"]/text() 
        try:
            name = hotel_soup.find('h2', id='hp_hotel_name').get_text().replace('\n', '').removeprefix('Отель')
        except AttributeError:
            name = 'Noname'
        #url is url
        #rate
        try:
            rate = hotel_soup.find('span', 'prco-valign-middle-helper').get_text().replace('\n', '')
        except AttributeError:
            rate = 'Unknown'
        #stars
        try:
            stars = (round(float(hotel_soup.find('div', 'b5cd09854e d10a6220b4').get_text().replace(',','.')) / 2)).__str__() #hotel rating
        except AttributeError:
            stars = ''
        #address
        try:
            address = hotel_soup.find('span', 'hp_address_subtitle js-hp_address_subtitle jq_tooltip').get_text().replace('\n', '')
        except AttributeError:
            address = 'Unknown'
        #latitude
        #longitude
        try:
            coords = hotel_soup.find('a', id='hotel_address').get('data-atlas-latlng').split(',') #hotel address
        except AttributeError:
            coords = ['0', '0']
        latitude = float(coords[0])
        longitude = float(coords[1])
        try:
            soup_tags = hotel_soup.find_all('div', 'important_facility')
        
        #tags
            tags = []
            for tag in soup_tags:
                tags.append(tag.get_text().replace('\n', ''))
        except AttributeError:
            tags = ['Unknown']

        hotel_data = {
            'name': name,
            'url': url,
            'rate': rate,
            'stars': stars,
            'address': address,
            'latitude': latitude,
            'longitude': longitude,
            'tags': tags
        }
        return hotel_data

    def __get_all_hotel_data(self, urls, thread_number = 4):
        pool = Pool(processes=thread_number)

        all_data = []
        for result in tqdm(pool.imap(func=self.__get_hotel_data, iterable=urls), total=len(urls)):
            all_data.append(result)
        return all_data

    def parse(self, dest: str, checkin: date, checkout: date, hotels_quantity: int):
        hotel_search_url = self.__generate_url(dest, checkin, checkout)
        hotel_urls = self.__get_hotel_urls(hotel_search_url, hotels_quantity)
        all_data = self.__get_all_hotel_data(hotel_urls, 4)
        return all_data

class YandexParser(Parser):
    base_url = 'https://travel.yandex.ru/hotels/'
    max_records = 50
    records_per_page = 25

"""
Parsers = [BookingParser(), YandexParser()]

city = "Стабмбул"
checkin = date(2022, 9, 10)   #YYYY-MM-DD
checkout = date(2022, 9, 11)

hotels_data = Parsers[0].parse(city, checkin, checkout, 50)

with open("data\\temp.json", "w", encoding='utf-8') as final:
    json.dump(hotels_data, final, ensure_ascii=False, indent=2)
"""