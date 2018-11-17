from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from selenium import webdriver


# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


# Function to scrape for Mars information
def scrape():
    browser = init_browser()

    mars = {}
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    
    # Retrieve the parent divs for all articles
    results = soup.find('li', class_="slide")

    news_title = results.find('div', class_='content_title').text
    #print(news_title)

    news_body = results.find('div', class_='article_teaser_body').text
    #print(news_body)
    #append the article title and body text to the dictionary
    mars["title"] = news_title
    mars["body"] = news_body

    #Find the featured image from the JPL webiste
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find('div', class_='img')
    #print(image)

    #Get the url for the image and append to the JPL website path
    img_url = image.find('img')['src']
    featured_image_url = 'https://www.jpl.nasa.gov'+img_url
    #print(featured_image_url)

    #Append the featured image url to the mars dictionary
    mars["feat_img"] = featured_image_url

    #visit the Mars weather twitter website and scrape the latest weather
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find('p', class_='TweetTextSize').text
    #print(mars_weather)

    #append the weather text to the dictionary
    mars["weather"] = mars_weather

    #Find the four Mars hemisphere images
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #get a list of the text of the four images
    image_list = soup.find_all('h3')
    hemisphere_image_urls = []

    #loop through the list of links and get the image urls
    for title in image_list:
        #print(title.text)
        browser.visit(url5)
        browser.click_link_by_partial_text(title.text)
        html2 = browser.html
        soup = BeautifulSoup(html2, 'html.parser')
        find_image = soup.find('div', class_='downloads')
        image_url = find_image.find('a')['href']
        #print(image_url)

        #append the title and image url to a dictionary and append to the list of images
        image_dict = {"title": title.text, "url": image_url}
        hemisphere_image_urls.append(image_dict)    
        mars["hemi_img"] = hemisphere_image_urls

    # Return results
    return mars


