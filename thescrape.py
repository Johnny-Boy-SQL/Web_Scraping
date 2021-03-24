# %%
import pandas as pd
from splinter import browser
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import time
from urllib.parse import urlsplit
from pprint import pprint


# %%
# run chrome driver
def init_browser():
    executable_path = {'executable_path': "C:\Drivers\chromedriver\chromedriver.exe"}
    return browser = Browser("chrome", **executable_path, headless=False)


# %%
def scrape_info():
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)


    # %%
    html = browser.html
    soup = bs(html,"html.parser")


    # %%
    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    print(f"Title: {news_title}")
    print(f"Para: {news_p}")


    # %%
    # load up the url
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')


    # %%
    stuff=soup.find('img',class_='headerimage fade-in')
    stuff


    featured = "image/featured/mars3.jpg/"
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    featured_url = url + featured


    # %%
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    tables


    # %%
    mars_df=tables[2]
    mars_df.columns=["description", "value"]
    mars_df.set_index("description",inplace=True)
    mars_df


    # %%
    mars_html_table=mars_df.to_html()
    mars_html_table.replace('\n','')


    # %%
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')


    # %%
    all_hemi=soup.find("div",class_='collapsible results')
    pprint(all_hemi)


    # %%
    all_hemi1=soup.find("div",class_='collapsible results')
    print(all_hemi1.prettify())


    # %%
    hemisphere1=all_hemi1.find_all('a')


    # %%
    hemisphere_image_urls = []
    for hemi in hemisphere1:
        if hemi.h3:
            title=hemi.h3.text
            link=hemi["href"]
            main_url="https://astrogeology.usgs.gov/"
            forward_url=main_url+link
            browser.visit(forward_url)
            html = browser.html
            soup = bs(html, 'html.parser')
            hemi2=soup.find("div",class_= "downloads")
            image=hemi2.ul.a["href"]
            hemi_dict={}
            hemi_dict["title"]=title
            hemi_dict["img_url"]=image
            hemisphere_image_urls.append(hemi_dict)
            browser.back()


    # %%
mars_py_dict={
        "mars_news_title": news_title,
        "mars_news_paragraph": news_p,
        "featured_mars_image": featured_url,
        "mars_facts": mars_html_table,
        "mars_hemisphers": hemisphere_image_urls
   }
browser.quit()

return mars_py_dict