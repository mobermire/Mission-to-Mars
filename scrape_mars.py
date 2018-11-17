from flask import Flask, render_template
import pymongo
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests


# # NASA Mars News
# 
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# URL of page to be scraped
url = 'https://mars.nasa.gov/news/'

# Retrieve page with the requests module
response = requests.get(url)

# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, 'html.parser')


news_title = soup.find("div", class_='content_title').text
news_p = soup.find("div", class_='rollover_description_inner').text
print(news_title)
print(news_p)


# # JPL Mars Space Images - Featured Image

# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign
# the url string to a variable called featured_image_url.
from splinter import Browser


executable_path = {'executable_path' : 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
base_url = "https://www.jpl.nasa.gov/"
browser.visit(url)

browser.click_link_by_partial_text('FULL IMAGE')


html_image = browser.html
soup = bs(html_image, "html.parser")
img_url = soup.find("img", class_="fancybox-image")["src"]
featured_img_url = base_url + img_url
print(featured_img_url)


# # Mars Weather


#Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from 
# the page. Save the tweet text for the weather report as a variable called mars_weather

url_weather = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_weather)

weather_data = browser.html
soup = bs(weather_data, "html.parser")
mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(mars_weather)


# # Mars Facts


# Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet 
# including Diameter, Mass, etc.  Use Pandas to convert the data to a HTML table string.

facts_url = "https://space-facts.com/mars/"
table = pd.read_html(facts_url)
table = table[0]

html_table = table.to_html()
html_table = html_table.replace("\n", "")
html_table


# # Mars Hemispheres

# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.

# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.

# Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the
# hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.

# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one 
# dictionary for each hemisphere.

hemi_url  = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
hemi_list = []

# Setting up splinter
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True)
browser.visit(hemi_url)


for i in range (4):
    images = browser.find_by_tag('h3')
    images[i].click()
    html = browser.html
    soup = bs(html, 'html.parser')
    partial = soup.find("img", class_="wide-image")["src"]
    img_title = soup.find("h2",class_="title").text
    img_url = 'https://astrogeology.usgs.gov'+ partial
    dictionary={"title":img_title,"img_url":img_url}
    hemi_list.append(dictionary)
    browser.back()

hemi_list

