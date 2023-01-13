import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import urllib.request



class opony:
    def wlaczenie_strony(self):
        s = Service('C:\webdriver\chromedriver.exe')
        self.browser = webdriver.Chrome(service=s)
        self.browser.get('https://b2b.j-m-k.pl/index.php/home/loginForm')
        login = self.browser.find_element("name", 'user_login[username]')
        login.send_keys('888')  # 
        time.sleep(0.1)
        haslo = self.browser.find_element("name", 'user_login[password]')
        haslo.send_keys('888')  #
        haslo.send_keys(Keys.ENTER)
        self.browser.implicitly_wait(4)
        self.pozycje = self.browser.find_element(By.XPATH, '//a[@href="/index.php/cennik/100"]')
        self.pozycje.click()
        self.browser.implicitly_wait(4)
        #select_element = browser.find_element(By.ID, 'quantity-filter2')
        #select = Select(select_element)
        # select.select_by_value('more_four')
        time.sleep(3)


    doCsv = list()
    def przejscie(self, x):
        self.browser.get(f'https://b2b.j-m-k.pl/index.php/cennik/strona/{x}')
        time.sleep(4)
        self.nazwy = self.browser.find_elements(By.XPATH, '//span[@class="item-title"]')
        print(len(self.nazwy))

    def pobieranie_danych(self, i):
        print("DDDD", i)
        self.nazwy[i].click()
        self.browser.implicitly_wait(4)
        ##nazwa
        #print("nazwa",self.nazwy[i].text)
        self.linia = self.browser.find_elements(By.XPATH, '//tr[@route="@product"]')
        #print(self.linia[i].text)
        self.podzielona_linia = (str(self.linia[i].text)).split()
        print(self.podzielona_linia)
        print("ilość",self.podzielona_linia[-5],self.podzielona_linia[-4],self.podzielona_linia[-3])
        time.sleep(3)
        ## tutaj dodać czekanie
        try:
            self.opis = self.browser.find_elements(By.XPATH, '//div[@class="desc-box"]')
            print("pisy", len(self.opis))
            #print(self.opis[i].text)
            self.opis_podzielony = self.opis[i].text
        except IndexError:
        #    time.sleep(20)
        #    self.opis = self.browser.find_elements(By.XPATH, '//div[@class="desc-box"]')
        #    print("pisy", len(self.opis))
        #    # print(self.opis[i].text)
        #    self.opis_podzielony = self.opis[i].text
            try:
                self.opis = self.browser.find_elements(By.XPATH, '//div[@class="desc-box"]')
                print("pisy", len(self.opis))
                # print(self.opis[i].text)
                self.opis_podzielony = self.opis[i].text
            except:
                self.browser.refresh()
                self.nazwy[i].click()
                self.browser.implicitly_wait(4)
                time.sleep(10)
                self.opis = self.browser.find_elements(By.XPATH, '//div[@class="desc-box"]')
                print("pisy", len(self.opis))
                # print(self.opis[i].text)
                self.opis_podzielony = self.opis[i].text

        self.opis_podzielony = self.opis_podzielony.split('\n')
        self.opis_podzielony = ' '.join(self.opis_podzielony)
        ##opis
        print("opis",self.opis_podzielony)
        ##cena center red price_netto
        self.cena = self.browser.find_elements(By.XPATH, '//td[@class="center red price_netto"]')
        print("cena",self.cena[i].text)
        ##nowa nazwa
        self.nazwa = self.browser.find_elements(By.XPATH, '//span[@class="item-title"]')[i].text
        print("nazwa",self.nazwa)
        self.do_pliku = self.nazwa + "&" + self.cena[i].text + "&" + self.opis_podzielony + "&" + self.podzielona_linia[-5] + "&" + self.podzielona_linia[-4] + "&" +self.podzielona_linia[-3]
        print("wszystko", self.do_pliku)
        with open('noweopony.csv', 'a') as file:
            fi = csv.writer(file)
            fi.writerow(self.do_pliku)







objekt = opony()
objekt.wlaczenie_strony()



for x in range(40,41):#pierwsza liczba to liczba strony
    objekt.przejscie(x)

    for i in range(0, 100):
        objekt.pobieranie_danych(i)
