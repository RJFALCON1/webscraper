from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import requests
from selenium.webdriver.common.by import By
url = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'
browser = webdriver.Chrome('/Users/arjunrajdev/Downloads/chromedriver')
browser.get(url)
time.sleep(10)
headers = ['name', 'light-years_from_Earth', 'planet_mass', 'stellar_magnitude', 'discovery_date',
           'hyperlink', 'planet_type', 'planet_radius', 'orbital_radius', 'orbital_period', 'eccentricity']
planetData = []


def scrapTheData():
    for page in range(0, 2):
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        allUlTags = soup.find_all('ul', attrs={'class', 'exoplanet'})
        for eachUl in allUlTags:
            allLiTags = eachUl.find_all('li')
            tempList = []
            for index, eachLi in enumerate(allLiTags):
                if index == 0:
                    tempList.append(eachLi.find_all('a')[0].contents[0])
                else:
                    tempList.append(eachLi.contents[0])
            hyperlinkVal = allLiTags[0]
            tempList.append('https://exoplanets.nasa.gov' +
                            hyperlinkVal.find_all('a', href=True)[0]['href'])

            planetData.append(tempList)
        browser.find_element(
            By.XPATH, '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    


newPlanetData = []
scrapTheData()


def scrapMoreData(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    tempList2 = []
    allTrTags = soup.find_all('tr', attrs={'class', 'fact_row'})
    for row, eachTr in enumerate(allTrTags):
        allTdTags = eachTr.find_all('td')
        for col, eachTd in enumerate(allTdTags):
            if (row == 0 and col == 1) or (row == 1 and col == 0) or (row == 3 and col == 1):
                continue
            else:
                data = eachTd.find_all(
                    'div', attrs={'class', 'value'})[0].contents[0].get_text()
                tempList2.append(data.replace('\n',''))
    newPlanetData.append(tempList2)
print(len(planetData))
for x in planetData:
    scrapMoreData(x[5])
finalPlanetData = []
for index, value in enumerate(planetData):
    finalPlanetData.append(planetData[index]+newPlanetData[index])
with open('scrapper.csv', 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(finalPlanetData)