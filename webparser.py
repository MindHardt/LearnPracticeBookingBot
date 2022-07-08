import datetime
from abc import abstractmethod
from datetime import date
from functools import total_ordering
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
#from tqdm import tqdm
from tqdm.contrib.telegram import tqdm, trange
import json

#https://hotel.tutu.ru/
#20 records_per_page
#lenta

class Parser:
    base_url: str
    max_records: int
    records_per_page: int
    headers2 = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'}
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

    @abstractmethod
    def parse(self, dest: str, checkin: str, checkout: str, hotels_quantity: int, chat_id, token):
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
            soup = BeautifulSoup(requests.get(url_to_parse,headers=self.headers).content, 'html.controller')

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
        hotel_soup = BeautifulSoup(requests.get(url,headers=self.headers).content, 'html.controller')
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

    def parse(self, destination: str, checkin: datetime.datetime, checkout: datetime.datetime, hotels_quantity: int, chat_id, token):

        hotel_search_url = self.__generate_url(destination, checkin, checkout)
        hotel_urls = self.__get_hotel_urls(hotel_search_url, hotels_quantity)

        pool = Pool(processes=4)

        all_data = []
        for result in tqdm(pool.imap(func=self.__get_hotel_data, iterable=hotel_urls), token=f'{token}', chat_id=f'{chat_id}', total=len(hotel_urls), unit='hotel'):
            all_data.append(result)

        return all_data


class YandexParser(Parser):
    base_url = 'https://travel.yandex.ru/hotels/'
    max_records = 25
    records_per_page = 25

    def num_to_month(self, num):
        return {
                1: 'Январь',
                2: 'Февраль',
                3: 'Март',
                4: 'Апрель',
                5: 'Май',
                6: 'Июнь',
                7: 'Июль',
                8: 'Август',
                9: 'Сентябрь', 
                10: 'Октябрь',
                11: 'Ноябрь',
                12: 'Декабрь'
        }[num]

    def __generate_url(self, dest: str, checkin: date, checkout: date):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(options=option)
        driver.get(self.base_url)
        driver.maximize_window()

        city_input = driver.find_element(By.XPATH, "//input[@class='w_eHd input_center']")
        city_input.clear()
        city_input.send_keys(dest)
        time.sleep(1)
        elem = driver.find_element(By.XPATH, "//div[@class='rC02U _PIrG sfzRD w5F6Y P0ZeS']")
        elem.click()
        time.sleep(1)

        #load calendar
        months_list = driver.find_elements(By.XPATH, "//div[@class='monthsList']//div")
        months_list[-1].click()
        #looking for correct month index
        checkin_month_index = 0 #февраль - 7
        for i in range(0, 12):
            if(months_list[i].text.__contains__(self.num_to_month(checkin.month))):
                checkin_month_index = i
                break
        checkout_month_index = checkin_month_index + checkout.month - checkin.month
        time.sleep(1)

        month_counter = -1

        for day in driver.find_elements(By.XPATH, "//div[@class='mYiO8']/div/span"):
            if(day.text == "1"):
                month_counter = month_counter + 1
            if(month_counter == checkin_month_index and day.text == checkin.day.__str__()):
                day.click()
            if(month_counter == checkout_month_index and day.text == checkout.day.__str__()):
                day.click()
                break


        submit_button = driver.find_element(By.XPATH, "//button[@class='vHqxX z8gtM']")
        submit_button.click()

        time.sleep(2)
        base_url = driver.current_url
        driver.quit()

        return base_url

    def __get_hotel_urls(self, url_to_parse: str, hotels_quantity: int = 10):
        #empty url list
        hotel_urls = []
        #счетчик отелей
        item_counter = 0
        #отступ для url
        for i in range(0, self.max_records, self.records_per_page):   #переход по страницам
            url_to_parse = re.sub('navigationToken=\d+', 'navigationToken=' + i.__str__(), url_to_parse)
            url_to_parse = re.sub('-\d+-newsearch', f'-{round(i / 25) + 1}-newsearch', url_to_parse)
                
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            driver = webdriver.Chrome(options=option)
            driver.get(url_to_parse)
            driver.maximize_window()
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()

            for item in soup.find_all('div', 'ATR04'): #going through hotel records
                #extract url
                hotel_url = 'https://travel.yandex.ru' + item.find('a', 'Link Link_theme_normal Link_view_default STEEy Y_QIb Link_lego vW74J').get('href')
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
    def __get_hotel_data(self, url):
            hotel_soup = BeautifulSoup(requests.get(url,headers=self.headers).content, 'html.parser')
            #name //*[@id="hp_hotel_name"]/text() 
            try:
                name = hotel_soup.find('div', '_SN_o').get_text()
            except AttributeError:
                name = 'Noname'
            #url is url
            #rate
            try:
                rate = hotel_soup.find('span', 'Akpkj vE8yn').get_text()
            except AttributeError:
                rate = 'Unknown'
            #stars
            try:
                stars = (round(float(hotel_soup.find('div', 'FlrxR _DRHd kWZoP').get_text().replace(',','.')))).__str__()
            except AttributeError:
                stars = ''
            #address
            try:
                address = hotel_soup.find('span', 'address Y7xGC').get_text().replace('\n', '')
            except AttributeError:
                address = 'Unknown'
            #latitude
            #longitude
            try:
                imgsrc = ''
                images = hotel_soup.find_all('img')
                for img in images:
                    if img.has_attr('src'):
                        if img['src'].__contains__('static-maps.yandex.ru'):
                            imgsrc = img['src']
                for str in imgsrc.split('&'):
                    if(str.__contains__('ll=')):
                        coords = str.removeprefix('ll=').split('%2C')
            except AttributeError:
                coords = ['0', '0']
            latitude = float(coords[1])
            longitude = float(coords[0])

            try:
            #tags
                tags = []
                for tag in hotel_soup.find_all('div', 'diui0 avQrE h865h'):
                    tags.append(tag.find('span', 'G7iZ5').get_text().replace('\n', ''))
                
                for tag in hotel_soup.find_all('li', 'cKijb'):
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
                
    def __str_to_date(self, str_date: str, separator = '.'):
            args = str_date.split(separator)
            return date(int(args[2]), int(args[1]), int(args[0]))

    def parse(self, dest: str, checkin: str, checkout: str, hotels_quantity: int, chat_id, token):
        checkin_d = self.__str_to_date(checkin)
        checkout_d = self.__str_to_date(checkout)
        hotel_search_url = self.__generate_url(dest, checkin_d, checkout_d)
        hotel_urls = self.__get_hotel_urls(hotel_search_url, hotels_quantity)

        pool = Pool(processes=4)

        all_data = []
        for result in tqdm(pool.imap(func=self.__get_hotel_data, iterable=hotel_urls), token=f'{token}', chat_id=f'{chat_id}', total=len(hotel_urls), unit='hotel'):
            all_data.append(result)