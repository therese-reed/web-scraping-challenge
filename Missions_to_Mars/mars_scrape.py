from bs4 import BeautifulSoup
import pandas as pd
import time
from splinter import Browser
import requests
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape(): # NASA Mars News

    """
    NASA Mars News
    """

    browser = init_browser()
    # Navigate to the page
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(4)
    # Assign the HTML content of the page to a variable
    news_html = browser.html
    # Parse HTML with Beautifulsoup
    soup = BeautifulSoup(news_html,'html.parser')

    # Retrieve the latest News Title and Paragraph Text
    result = soup.find('div', class_="list_text")
    news_title = result.a.text
    news_p = result.find('div',class_="article_teaser_body").text
    
    
    """
    Mars Img
    """
    # Navigate to the page
    url_image = "https://spaceimages-mars.com/"
    browser.visit(url_image)
    browser.find_by_text(' FULL IMAGE').first.click()
   #get image url using BeautifulSoup
    html_image = browser.html
    soup = BeautifulSoup(html_image, "html.parser")
    img_url = soup.find("img", class_="fancybox-image")["src"]
    featured_image_url = url_image + img_url
 

    """
   
    Mars_data
    """
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    # Collect the tables from the page 
    tables = pd.read_html(requests.get('https://space-facts.com/mars/').text)
    #tables = pd.read_html(facts_url)

    # Retrieve the table containing facts about the planet 
    df = tables[2]
    df.columns = ["Description","Value"]
    idx_df = df.set_index("Description")
    # Export to a HTML file
    mars_df = idx_df.to_html(border="1",justify="left")
   

    """
    Mars Hemispheres
    """
    # Navigate to the page
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(1)
    # Assign the HTML content of the page to a variable
    hemisphere_html = browser.html
    # Parse HTML with Beautifulsoup
    soup = BeautifulSoup(hemisphere_html,'html.parser')

    # Collect the urls for the hemisphere images
    items = soup.find_all("div", class_="item")

    main_url = "https://astrogeology.usgs.gov"
    hemisphere_image_urls=[]
    for item in items:
        hemisphere_url = f"{main_url}{item.find('a', class_='itemLink')['href']}"
        
        # Navigate to the page
        browser.visit(hemisphere_url)
        time.sleep(1)
        # Assign the HTML content of the page to a variable
        hemisphere_html = browser.html
        # Parse HTML with Beautifulsoup
        soup = BeautifulSoup(hemisphere_html,'html.parser')
        
        img_url = soup.find('img', class_="wide-image")['src']
        title = soup.find('h2', class_="title").text
        
        hemisphere_image_urls.append({"title":title,"img_url":f"{main_url}{img_url}"})
    
    
    mars_info = {
        "news_title": news_title,
        "news_p": news_p,
        "mars_img": featured_image_url,
        "mars_fact": mars_df,
        "mars_hemisphere": hemisphere_image_urls
    }
    browser.quit()

    return mars_info
