import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime


# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


# Function to scrape for weather in Cost Rica
def scrape():

    # Initialize browser
    browser = init_browser()
    weather = {}
    # Visit the Costa Rica climate site
    url = "https://visitcostarica.herokuapp.com/"
    browser.visit(url)
    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # Find today's forecast
    weather["forecast"] = soup.find("p").get_text()
    # Get the max temp
    #weather["max_temp"] = soup.find("span", class_="result-price").get_text()
    # Print the min temp
    #weather["min_temp"] = soup.find("span", class_="result-hood").get_text()
    # Get current time stamp
    weather["time"] = datetime.datetime.utcnow()

    # Return results
    return mars


