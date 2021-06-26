#!/usr/bin/env python
# coding: utf-8
# # 10.3.3 Scrape Maars Data: The News
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import time

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Scrape Mars news
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #slide_elem.find('div', class_= 'content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p
    
  
# # 10.3.4 Scrape Mars Data: Featured Image
# ### JPL Space Images Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None, None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url
    
# # 10.3.5 Scrape Mars Data: Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def mars_hemispheres(browser):
    # Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    link_soup = soup(html, 'html.parser')

    # Create a list to hold the images and titles.
    image_urls = []
    results = link_soup.find_all('div', class_ = 'item')
    for result in results:
        # Retreive image urls
        link = result.find('a', class_='itemLink product-item')['href']
        # Create image url by appending to the base url
        image_url = f'https://marshemispheres.com/{link}'
        image_urls.append(image_url)
    
    # Create a list to hold the images and titles.Step 2
    hemisphere_image_urls = []

    # Looping to get img urls
    for url in image_urls:
        hemispheres = {}
        # Visit the url using browser
        browser.visit(url)

        # Click on toggle open button
        button = browser.find_by_id("wide-image-toggle")
        button.click()

        # Time lapse
        time.sleep(1)

        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')

        # Retrieve the titles for each hemisphere.
        title = img_soup.find('h2', class_= "title").text
        # Adding to dictionary
        hemispheres["title"]= title

        # Retreiving the rel image url
        rel_img = img_soup.find('img',class_= "wide-image").get('src')

        # The image url
        img_url = f'https://marshemispheres.com/{rel_img}'
        # adding to dictionary
        hemispheres["img_url"]= img_url

        # Appending dictionary to the empty list
        hemisphere_image_urls.append(hemispheres)

        # Going back to the browser
        browser.back()

    return hemisphere_image_urls

#if __name__ == "__main__":

    # If running as script, print scraped data
    #print(scrape_all())   

mars = scrape_all()
for x,y in mars.items():
    print(x,y)






