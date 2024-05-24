#!/usr/bin/env python
# coding: utf-8

# In[12]:


pip install requests beautifulsoup4 pandas


# In[13]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# Question 1: IMDb Top 100 Indian movies
url = 'https://www.imdb.com/list/ls056092300/'

# Send a GET request to fetch the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize lists to store movie data
names = []
ratings = []
years = []

# Find all movie list items
movies = soup.find_all('div', class_='sc-b189961a-0 hBZnfJ')

for movie in movies:
    # Extract movie name
    name = movie.find('h3', class_='ipc-title__text').a.text
    names.append(name)
    
    # Extract movie rating
    rating = movie.find('span', class_='ipc-icon ipc-icon--star-inline').text
    ratings.append(rating)
    
    # Extract movie year
    year = movie.find('span', class_='lister-item-year text-muted unbold').text
    years.append(year)

# Create a DataFrame
df = pd.DataFrame({
    'Name': names,
    'Rating': ratings,
    'Year of Release': years
})

# Display the DataFrame
print(df)

# Optionally, save the DataFrame to a CSV file
# df.to_csv('top_100_indian_movies.csv', index=False)


# In[11]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# Question 2: scrape details of all the posts

# If accessing directly, use:
url='https://www.patreon.com/coreyms'
response = requests.get(url)

# Save the HTML content to a local file
with open('coreyms_patreon.html', 'w', encoding='utf-8') as file:
    file.write(response.text)

soup = BeautifulSoup(response.content, 'html.parser')


# If HTML content is saved locally:
with open('coreyms_patreon.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Initialize lists to store post data
headings = []
dates = []
contents = []
likes = []
youtube_links = []

# Find all posts
posts = soup.find_all('div', class_='post-class')  # Adjust the class based on actual HTML structure

for post in posts:
    # Extract heading
    heading = post.find('h2', class_='post-title-class').text.strip()  # Adjust the class
    headings.append(heading)
    
    # Extract date
    date = post.find('span', class_='post-date-class').text.strip()  # Adjust the class
    dates.append(date)
    
    # Extract content
    content = post.find('div', class_='post-content-class').text.strip()  # Adjust the class
    contents.append(content)
    
    # Extract likes
    like = post.find('span', class_='post-likes-class').text.strip()  # Adjust the class
    likes.append(like)
    
    # Extract YouTube link if present
    youtube_link_tag = post.find('a', href=True)
    youtube_link = youtube_link_tag['href'] if youtube_link_tag and 'youtube.com' in youtube_link_tag['href'] else None
    youtube_links.append(youtube_link)

# Create a DataFrame
df = pd.DataFrame({
    'Heading': headings,
    'Date': dates,
    'Content': contents,
    'Likes': likes,
    'YouTube Link': youtube_links
})

# Display the DataFrame
print(df)

# Optionally, save the DataFrame to a CSV file
#df.to_csv('coreyms_patreon_posts.csv', index=False)


# In[16]:


pip install selenium beautifulsoup4 pandas


# In[1]:


pip install requests beautifulsoup4


# In[2]:


import requests
from bs4 import BeautifulSoup

# Question 3: Function to fetch house details
def fetch_house_details(locality):
    url = f"https://www.nobroker.in/property/sale/{locality.lower().replace(' ', '-')}_bangalore"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    houses = []

    # Find all house listings on the page
    for listing in soup.find_all('div', class_='card'):
        try:
            title = listing.find('h2', class_='heading-6').text.strip()
            location = listing.find('div', class_='nb__2CMjv').text.strip()
            area = listing.find('div', class_='nb__3oNyC').text.strip()
            price = listing.find('div', class_='nb__1Nyyv').text.strip()
            emi = listing.find('div', class_='nb__sqaQl').text.strip()
            
            house = {
                'Title': title,
                'Location': location,
                'Area': area,
                'Price': price,
                'EMI': emi
            }
            houses.append(house)
        except AttributeError:
            continue

    return houses

# Localities to scrape
localities = ["Indira Nagar", "Jayanagar", "Rajaji Nagar"]

# Fetch details for each locality
all_houses = []
for locality in localities:
    print(f"Fetching details for {locality}...")
    houses = fetch_house_details(locality)
    all_houses.extend(houses)

# Print all house details
for house in all_houses:
    print(house)


# In[3]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# Quesrion 4: URL of the Bewakoof Bestseller page
url = 'https://www.bewakoof.com/bestseller?sort=popular'

# Send a GET request to fetch the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize lists to store product data
product_names = []
prices = []
image_urls = []

# Find the product details
products = soup.find_all('div', class_='productCardBox', limit=10)

for product in products:
    # Extract product name
    product_name = product.find('h3').text
    product_names.append(product_name)
    
    # Extract product price
    price = product.find('div', class_='discountedPriceText').text
    prices.append(price)
    
    # Extract product image URL
    image_url = product.find('img', class_='productImgTag')['src']
    image_urls.append(image_url)

# Create a DataFrame
df = pd.DataFrame({
    'Product Name': product_names,
    'Price': prices,
    'Image URL': image_urls
})

# Display the DataFrame
print(df)

# Optionally, save the DataFrame to a CSV file
df.to_csv('bewakoof_bestsellers.csv', index=False)


# In[4]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the CNBC World News page
url = 'https://www.cnbc.com/world/?region=world'

# Send a GET request to fetch the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize lists to store news data
headings = []
dates = []
news_links = []

# Question 5: Find the news articles (adjust the tags and classes based on actual HTML structure)
articles = soup.find_all('div', class_='Card-standardBreakerCard')

for article in articles:
    # Extract headline
    heading = article.find('a', class_='Card-title').text.strip() if article.find('a', class_='Card-title') else 'N/A'
    headings.append(heading)
    
    # Extract date
    date = article.find('time', class_='Card-time')['datetime'] if article.find('time', class_='Card-time') else 'N/A'
    dates.append(date)
    
    # Extract news link
    news_link = article.find('a', class_='Card-title')['href'] if article.find('a', class_='Card-title') else 'N/A'
    news_links.append(news_link)

# Create a DataFrame
df = pd.DataFrame({
    'Heading': headings,
    'Date': dates,
    'News Link': news_links
})

# Display the DataFrame
print(df)

# Optionally, save the DataFrame to a CSV file
df.to_csv('cnbc_world_news.csv', index=False)


# In[14]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# Question 6: URL of the page to scrape
url = 'https://www.keaipublishing.com/en/journals/artificial-intelligence-in-agriculture/most-downloaded-articles/'

# Send a GET request to fetch the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize lists to store paper data
titles = []
dates = []
authors = []

# Find the paper details (adjust the tags and classes based on actual HTML structure)
articles = soup.find_all('div', class_='pod-listing')

for article in articles:
    # Extract paper title
    title = article.find('h2', class_='pod-listing-header').text.strip() if article.find('h2', class_='pod-listing-header') else 'N/A'
    titles.append(title)
    
    # Extract date
    date = article.find('span', class_='pod-listing-date').text.strip() if article.find('span', class_='pod-listing-date') else 'N/A'
    dates.append(date)
    
    # Extract author
    author = article.find('span', class_='pod-listing-authors').text.strip() if article.find('span', class_='pod-listing-authors') else 'N/A'
    authors.append(author)

# Create a DataFrame
df = pd.DataFrame({
    'Paper Title': titles,
    'Date': dates,
    'Author': authors
})

# Display the DataFrame
print(df)

# Optionally, save the DataFrame to a CSV file
df.to_csv('most_downloaded_articles.csv', index=False)


# In[ ]:




