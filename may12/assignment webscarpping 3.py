#!/usr/bin/env python
# coding: utf-8

# In[23]:


import requests
from bs4 import BeautifulSoup
#Question 1
def search_amazon(product_name):
    url = f"https://www.amazon.in/s?k={product_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    products = []

    for result in soup.find_all("div", {"data-component-type": "s-search-result"}):
        title_tag = result.find("span", {"class": "a-size-medium a-color-base a-text-normal"})
        link_tag = result.find("a", {"class": "a-link-normal a-text-normal"})

        if title_tag and link_tag:
            title = title_tag.text.strip()
            link = "https://www.amazon.in" + link_tag["href"]
            products.append({"title": title, "link": link})

    return products

product_name = input("Enter a product name: ")
products = search_amazon(product_name)
for product in products:
    print(f"Title: {product['title']}, Link: {product['link']}")


# In[20]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
#question 2
def scrape_amazon(product_name):
    products = []
    for page in range(1, 4):  # scrape first 3 pages
        url = f"https://www.amazon.in/s?k={product_name}&page={page}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        for result in soup.find_all("div", {"data-component-type": "s-search-result"}):
            product_url = "https://www.amazon.in" + result.find("a", {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style"})["href"]
            product_page_response = requests.get(product_url, headers=headers)
            product_page_soup = BeautifulSoup(product_page_response.content, "html.parser")
            brand_name = product_page_soup.find("a", {"id": "bylineInfo"}).text.strip() if product_page_soup.find("a", {"id": "bylineInfo"}) else "-"
            product_name = product_page_soup.find("span", {"id": "productTitle"}).text.strip() if product_page_soup.find("span", {"id": "productTitle"}) else "-"
            price = product_page_soup.find("span", {"id": "priceblock_ourprice"}).text.strip() if product_page_soup.find("span", {"id": "priceblock_ourprice"}) else "-"
            return_exchange = product_page_soup.find("span", {"class": "a-size-base a-color-base"}).text.strip() if product_page_soup.find("span", {"class": "a-size-base a-color-base"}) else "-"
            expected_delivery = product_page_soup.find("span", {"id": "delivery-message"}).text.strip() if product_page_soup.find("span", {"id": "delivery-message"}) else "-"
            availability = product_page_soup.find("span", {"id": "availability"}).text.strip() if product_page_soup.find("span", {"id": "availability"}) else "-"
            products.append({
                "Brand Name": brand_name,
                "Name of the Product": product_name,
                "Price": price,
                "Return/Exchange": return_exchange,
                "Expected Delivery": expected_delivery,
                "Availability": availability,
                "Product URL": product_url
            })
    return products

product_name = input("Enter a product name: ")
products = scrape_amazon(product_name)
df = pd.DataFrame(products)
df.to_csv(f"D:\flip\assignment webscrap june20th\''{product_name}.csv", index=False)
print(f"Data saved to {product_name}.csv")


# In[2]:


import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import urllib.request
import shutil

# Set up Chrome options--Question3
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# Set up Chrome driver
driver = webdriver.Chrome(options=options)

# Set up search terms
search_terms = ["fruits", "cars", "Machine Learning", "Guitar", "Cakes"]

# Set up image count
image_count = 10

# Create a directory for each search term
for term in search_terms:
    os.makedirs(term, exist_ok=True)

# Function to fetch image URLs
def fetch_image_urls(term):
    driver.get("https://images.google.com/")
    search_box = driver.find_element_by_name("q")
    search_box.send_keys(term)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    image_urls = []
    while len(image_urls) < image_count:
        thumbnails = driver.find_elements_by_css_selector("img.rg_i")
        for thumbnail in thumbnails:
            thumbnail.click()
            time.sleep(1)
            actual_image = driver.find_element_by_css_selector("img.n3VNCb")
            image_url = actual_image.get_attribute("src")
            if image_url:
                image_urls.append(image_url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    return image_urls

# Function to download images
def download_images(term, image_urls):
    for i, url in enumerate(image_urls):
        filename = f"{term}/{i+1}.jpg"
        urllib.request.urlretrieve(url, filename)
        print(f"Downloaded {filename}")

# Fetch and download images for each search term
for term in search_terms:
    image_urls = fetch_image_urls(term)
    download_images(term, image_urls)

# Close Chrome driver
driver.quit()


# In[6]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
#Question4
def scrape_flipkart(smartphone_name):
    url = f"https://www.flipkart.com/search?q={smartphone_name}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    products = []
    for result in soup.find_all("div", {"class": "_2kHMtA"}):
        product_url = "https://www.flipkart.com" + result.find("a", {"class": "_1fQZEK"})["href"]
        product_page_response = requests.get(product_url, headers=headers)
        product_page_soup = BeautifulSoup(product_page_response.content, "html.parser")
        brand_name = product_page_soup.find("span", {"class": "_2J4LW6"}).text.strip() if product_page_soup.find("span", {"class": "_2J4LW6"}) else "-"
        smartphone_name = product_page_soup.find("span", {"class": "_35KyD6"}).text.strip() if product_page_soup.find("span", {"class": "_35KyD6"}) else "-"
        colour = product_page_soup.find("div", {"class": "_3FxgXg"}).text.strip() if product_page_soup.find("div", {"class": "_3FxgXg"}) else "-"
        specs = product_page_soup.find_all("li", {"class": "_2ascJb"})
        ram = "-"
        storage = "-"
        primary_camera = "-"
        secondary_camera = "-"
        display_size = "-"
        battery_capacity = "-"
        for spec in specs:
            if "RAM" in spec.text:
                ram = spec.text.split(":")[1].strip()
            elif "Storage" in spec.text:
                storage = spec.text.split(":")[1].strip()
            elif "Primary Camera" in spec.text:
                primary_camera = spec.text.split(":")[1].strip()
            elif "Secondary Camera" in spec.text:
                secondary_camera = spec.text.split(":")[1].strip()
            elif "Display Size" in spec.text:
                display_size = spec.text.split(":")[1].strip()
            elif "Battery Capacity" in spec.text:
                battery_capacity = spec.text.split(":")[1].strip()
        price = product_page_soup.find("div", {"class": "_1vC4OE _2rQ-NK"}).text.strip() if product_page_soup.find("div", {"class": "_1vC4OE _2rQ-NK"}) else "-"
        products.append({
            "Brand Name": brand_name,
            "Smartphone Name": smartphone_name,
            "Colour": colour,
            "RAM": ram,
            "Storage(ROM)": storage,
            "Primary Camera": primary_camera,
            "Secondary Camera": secondary_camera,
            "Display Size": display_size,
            "Battery Capacity": battery_capacity,
            "Price": price,
            "Product URL": product_url
        })
    return products

smartphone_name = input("Enter a smartphone name: ")
products = scrape_flipkart(smartphone_name)
df = pd.DataFrame(products)
df.to_csv(f"{smartphone_name}.csv", index=False)
print(f"Data saved to {smartphone_name}.csv")


# In[7]:


pip install requests


# In[9]:


import requests
#question 5
def get_geospatial_coordinates(city, api_key):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": city,
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        print(f"Error fetching data: {data['status']}")
        return None, None

# Replace 'YOUR_API_KEY' with your actual Google Maps Geocoding API key
api_key = "YOUR_API_KEY"
city = input("Enter a city: ")
latitude, longitude = get_geospatial_coordinates(city, api_key)

if latitude and longitude:
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Could not retrieve geospatial coordinates.")


# In[10]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
#question 6
def scrape_gaming_laptops():
    url = "https://www.digit.in/laptops/best-gaming-laptops-in-india.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    laptops = soup.find_all("div", {"class": "listing-item"})
    data = []
    for laptop in laptops:
        brand_name = laptop.find("h2", {"class": "title"}).text.strip()
        product_name = laptop.find("h3", {"class": "subtitle"}).text.strip()
        price = laptop.find("span", {"class": "price"}).text.strip()
        availability = laptop.find("span", {"class": "availability"}).text.strip()
        product_url = laptop.find("a", {"class": "listing-link"})["href"]
        specs = laptop.find("ul", {"class": "specs"}).find_all("li")
        specs_dict = {}
        for spec in specs:
            key, value = spec.text.strip().split(": ")
            specs_dict[key] = value
        data.append({
            "Brand Name": brand_name,
            "Product Name": product_name,
            "Price": price,
            "Availability": availability,
            "Product URL": product_url,
            "Processor": specs_dict.get("Processor", "-"),
            "Graphics Card": specs_dict.get("Graphics Card", "-"),
            "RAM": specs_dict.get("RAM", "-"),
            "Storage": specs_dict.get("Storage", "-"),
            "Display": specs_dict.get("Display", "-"),
            "Refresh Rate": specs_dict.get("Refresh Rate", "-")
        })
    df = pd.DataFrame(data)
    df.to_csv("gaming_laptops.csv", index=False)

scrape_gaming_laptops()


# In[18]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
#Question 7
def scrape_forbes_billionaires():
    url = 'https://www.forbes.com/billionaires/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Locate the table containing the billionaire data
    table = soup.find('div', {'class': 'table-container'})
    rows = table.find_all('div', {'class': 'table-row'})

    data = []
    for row in rows[1:]:  # Skipping the header row
        rank = row.find('div', {'class': 'Table_rank__X4MKf'}).get_text(strip=True)
        name = row.find('div', {'class': 'Table_personName__Bus2E'}).get_text(strip=True)
        net_worth = row.find('div', {'class': 'Table_finalWorth__UZA6k'}).get_text(strip=True)
        age = row.find('div', {'class': 'age'}).get_text(strip=True)
        citizenship = row.find('div', {'class': 'countryOfCitizenship'}).get_text(strip=True)
        source = row.find('div', {'class': 'source'}).get_text(strip=True)
        industry = row.find('div', {'class': 'category'}).get_text(strip=True)
        
        data.append({
            'Rank': rank,
            'Name': name,
            'Net worth': net_worth,
            'Age': age,
            'Citizenship': citizenship,
            'Source': source,
            'Industry': industry
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df

# Scrape and display the data
billionaires_df = scrape_forbes_billionaires()
print(billionaires_df)

# Optionally, save to a CSV file
billionaires_df.to_csv('D:\flip\assignment webscrap june20th\forbes_billionaires.csv', index=False)


# In[12]:


pip install google-api-python-client


# In[13]:


pip install requests beautifulsoup4 pandas


# In[15]:


from googleapiclient.discovery import build

api_key = 'YOUR_API_KEY'
#question 8
def video_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_response = youtube.commentThreads().list(
        part='snippet,replies',
        videoId=video_id
    ).execute()

    comments = []
    while video_response:
        for item in video_response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            reply_count = item['snippet']['totalReplyCount']
            if reply_count > 0:
                for reply in item['replies']['comments']:
                    reply = reply['snippet']['textDisplay']
                    comments.append({'Comment': comment, 'Reply': reply, 'Upvote': item['snippet']['topLevelComment']['snippet']['likeCount'], 'Time': item['snippet']['topLevelComment']['snippet']['publishedAt']})
            else:
                comments.append({'Comment': comment, 'Reply': '-', 'Upvote': item['snippet']['topLevelComment']['snippet']['likeCount'], 'Time': item['snippet']['topLevelComment']['snippet']['publishedAt']})

        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                pageToken=video_response['nextPageToken']
            ).execute()
        else:
            break

    df = pd.DataFrame(comments)
    df.to_csv('youtube_comments.csv', index=False)

video_id = 'ENTER_VIDEO_ID'
video_comments(video_id)


# In[11]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
#Question 9
def scrape_hostels():
    url = "https://www.hostelworld.com/hostels/London"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    hostels = soup.find_all('div', {'data-testid': 'property-card'})
    hostels_data = []

    for hostel in hostels:
        name_element = hostel.find('div', {'data-testid': 'title'})
        name = name_element.text.strip()

        distance_element = hostel.find('span', {'data-testid': 'distance'})
        distance = distance_element.text.strip()

        ratings_element = hostel.find('div', {'class': 'rating'})
        ratings = ratings_element.text.strip()

        reviews_element = hostel.find('span', {'data-testid': 'eviews'})
        reviews = reviews_element.text.strip()

        privates_price_element = hostel.find('span', {'data-testid': 'privates-price'})
        privates_price = privates_price_element.text.strip()

        dorms_price_element = hostel.find('span', {'data-testid': 'dorms-price'})
        dorms_price = dorms_price_element.text.strip()

        facilities_element = hostel.find('div', {'data-testid': 'facilities'})
        facilities = facilities_element.text.strip()

        property_description_element = hostel.find('div', {'data-testid': 'property-description'})
        property_description = property_description_element.text.strip()

        hostels_data.append({
            'Name': name,
            'Distance from City Centre': distance,
            'Ratings': ratings,
            'Total Reviews': reviews,
            'Privates from Price': privates_price,
            'Dorms from Price': dorms_price,
            'Facilities': facilities,
            'Property Description': property_description
        })

    df = pd.DataFrame(hostels_data)
    df.to_csv('hostels_london.csv', index=False)

scrape_hostels()


# In[ ]:




