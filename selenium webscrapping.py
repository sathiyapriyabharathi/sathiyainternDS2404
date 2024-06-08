#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install selenium')


# In[4]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Question 1: 
driver = webdriver.Chrome()

# Step 1: Go to the Naukri website
driver.get("https://www.naukri.com/")

# Step 2: Enter “Data Scientist” in “Skill, Designations, and Companies” field and search
search_field = driver.find_element(By.ID, "suggestor-input")
search_field.send_keys("Data Scientist")
search_field.send_keys(Keys.RETURN)

# Step 3: Apply the location filter for “Delhi/NCR”
time.sleep(5)  # wait for the page to load
location_filter = driver.find_element(By.XPATH, "//span[text()='Delhi / NCR']")
location_filter.click()

# Step 4: Apply the salary filter for “3-6” lakhs
time.sleep(5)  # wait for the page to load
salary_filter = driver.find_element(By.XPATH, "//span[text()='3-6 Lakhs']")
salary_filter.click()

# Step 5: Scrape the data for the first 10 job results
time.sleep(5)  # wait for the page to load
jobs = []
for i in range(1, 11):
    try:
        job_title = driver.find_element(By.XPATH, f"(//a[@class='title fw500 ellipsis'])[position()={i}]").text
        job_location = driver.find_element(By.XPATH, f"(//li[@class='fleft grey-text br2 placeHolderLi location']/span)[position()={i}]").text
        company_name = driver.find_element(By.XPATH, f"(//a[@class='subTitle ellipsis fleft'])[position()={i}]").text
        experience_required = driver.find_element(By.XPATH, f"(//li[@class='fleft grey-text br2 placeHolderLi experience']/span)[position()={i}]").text
        jobs.append([job_title, job_location, company_name, experience_required])
    except Exception as e:
        print(f"Error occurred for job index {i}: {e}")

# Step 6: Create a dataframe of the scraped data
columns = ["Job Title", "Location", "Company Name", "Experience Required"]
df = pd.DataFrame(jobs, columns=columns)

# Save or print the dataframe
print(df)

# Close the driver
driver.quit()


# In[3]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Question 2:
driver = webdriver.Chrome()

# Step 1: Go to the Shine website
driver.get("https://www.shine.com/")

# Step 2: Enter “Data Scientist” in “Job title, Skills” field and enter “Bangalore” in “enter the location” field
time.sleep(5)  # Wait for the page to load
job_title_field = driver.find_element(By.ID, "id_q")
job_title_field.send_keys("Data Scientist")

location_field = driver.find_element(By.ID, "id_loc")
location_field.send_keys("Bangalore")

# Step 3: Click the search button
search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search Jobs')]")
search_button.click()

# Step 4: Scrape the data for the first 10 job results
time.sleep(5)  # Wait for the results to load
jobs = []
for i in range(1, 11):
    try:
        job_title = driver.find_element(By.XPATH, f"(//div[@class='w-90']/div/h2/a)[{i}]").text
        job_location = driver.find_element(By.XPATH, f"(//div[@class='w-90']/div/div[@class='result-info__location'])[{i}]").text
        company_name = driver.find_element(By.XPATH, f"(//div[@class='w-90']/div/div[@class='result-info__left-content']/div[@class='result-info__org'])[{i}]").text
        experience_required = driver.find_element(By.XPATH, f"(//div[@class='w-90']/div/div[@class='result-info__exp'])[{i}]").text
        jobs.append([job_title, job_location, company_name, experience_required])
    except Exception as e:
        print(f"Error occurred for job index {i}: {e}")

# Step 5: Create a dataframe of the scraped data
columns = ["Job Title", "Location", "Company Name", "Experience Required"]
df = pd.DataFrame(jobs, columns=columns)

# Print the dataframe
print(df)

# Close the driver
driver.quit()


# In[4]:


get_ipython().system('pip install selenium pandas')


# In[5]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Question 3:
driver = webdriver.Chrome()

# Step 1: Go to the Flipkart iPhone 11 reviews page
driver.get("https://www.flipkart.com/apple-iphone-11-black-64-gb/product-reviews/itm4e5041ba101fd?pid=MOBFWQ6BXGJCEYNY&lid=LSTMOBFWQ6BXGJCEYNYZXSHRJ&marketplace=FLIPKART")

# Function to scrape one page of reviews
def scrape_page():
    reviews = []
    review_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'col _2wzgFH')]")
    for review_element in review_elements:
        try:
            rating = review_element.find_element(By.XPATH, ".//div[@class='_3LWZlK _1BLPMq']").text
            review_summary = review_element.find_element(By.XPATH, ".//p[@class='_2-N8zT']").text
            full_review = review_element.find_element(By.XPATH, ".//div[@class='t-ZTKy']").text
            reviews.append([rating, review_summary, full_review])
        except Exception as e:
            print(f"Error occurred: {e}")
    return reviews

# Step 2: Scrape the data for the first 100 reviews
all_reviews = []
page = 1
while len(all_reviews) < 100:
    print(f"Scraping page {page}")
    all_reviews.extend(scrape_page())
    if len(all_reviews) >= 100:
        break
    try:
        next_button = driver.find_element(By.XPATH, "//a[contains(@class, '_1LKTO3') and text()='Next']")
        next_button.click()
        time.sleep(5)  # Wait for the next page to load
        page += 1
    except Exception as e:
        print(f"No more pages found: {e}")
        break

# Limit to 100 reviews
all_reviews = all_reviews[:100]

# Step 3: Create a dataframe of the scraped data
columns = ["Rating", "Review Summary", "Full Review"]
df = pd.DataFrame(all_reviews, columns=columns)

# Print the dataframe
print(df)

# Close the driver
driver.quit()

# Optionally, save the dataframe to a CSV file
df.to_csv("flipkart_iphone11_reviews.csv", index=False)


# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Question 4:
driver = webdriver.Chrome()

# Step 1: Go to the Flipkart website
driver.get("https://www.flipkart.com/")

# Close the login popup if it appears
try:
    close_login_popup = driver.find_element(By.XPATH, "//button[contains(text(), '✕')]")
    close_login_popup.click()
except Exception as e:
    print("Login popup did not appear.")

# Step 2: Enter “sneakers” in the search field and click the search button
search_field = driver.find_element(By.NAME, "q")
search_field.send_keys("sneakers")
search_field.send_keys(Keys.RETURN)

# Function to scrape one page of sneaker results
def scrape_page():
    sneakers = []
    product_elements = driver.find_elements(By.XPATH, "//div[@class='_2B099V']")
    for product_element in product_elements:
        try:
            brand = product_element.find_element(By.XPATH, ".//div[@class='_2WkVRV']").text
            description = product_element.find_element(By.XPATH, ".//a[@class='IRpwTa']").text
            price = product_element.find_element(By.XPATH, ".//div[@class='_30jeq3']").text
            sneakers.append([brand, description, price])
        except Exception as e:
            print(f"Error occurred: {e}")
    return sneakers

# Step 3: Scrape the data for the first 100 sneakers
all_sneakers = []
page = 1
while len(all_sneakers) < 100:
    print(f"Scraping page {page}")
    all_sneakers.extend(scrape_page())
    if len(all_sneakers) >= 100:
        break
    try:
        next_button = driver.find_element(By.XPATH, "//a[contains(@class, '_1LKTO3') and text()='Next']")
        next_button.click()
        time.sleep(5)  # Wait for the next page to load
        page += 1
    except Exception as e:
        print(f"No more pages found: {e}")
        break

# Limit to 100 sneakers
all_sneakers = all_sneakers[:100]

# Step 4: Create a dataframe of the scraped data
columns = ["Brand", "Product Description", "Price"]
df = pd.DataFrame(all_sneakers, columns=columns)

# Print the dataframe
print(df)

# Close the driver
driver.quit()

# Optionally, save the dataframe to a CSV file
df.to_csv("flipkart_sneakers.csv", index=False)


# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Question 5:
driver = webdriver.Chrome()

# Step 1: Go to the Amazon website
driver.get("https://www.amazon.in/")

# Step 2: Enter “Laptop” in the search field and click the search icon
search_field = driver.find_element(By.ID, "twotabsearchtextbox")
search_field.send_keys("Laptop")
search_field.send_keys(Keys.RETURN)

# Step 3: Set CPU Type filter to “Intel Core i7”
time.sleep(5)  # Wait for the page to load
cpu_filter = driver.find_element(By.XPATH, "//span[text()='Intel Core i7']")
cpu_filter.click()

# Function to scrape one page of laptop results
def scrape_page():
    laptops = []
    product_elements = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
    for product_element in product_elements:
        try:
            title = product_element.find_element(By.XPATH, ".//h2/a/span").text
            ratings = product_element.find_element(By.XPATH, ".//span[@class='a-icon-alt']").text
            price_whole = product_element.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
            price_fraction = product_element.find_element(By.XPATH, ".//span[@class='a-price-fraction']").text
            price = price_whole + price_fraction
            laptops.append([title, ratings, price])
        except Exception as e:
            print(f"Error occurred: {e}")
    return laptops

# Step 4: Scrape the data for the first 10 laptops
all_laptops = []
page = 1
while len(all_laptops) < 10:
    print(f"Scraping page {page}")
    all_laptops.extend(scrape_page())
    if len(all_laptops) >= 10:
        break
    try:
        next_button = driver.find_element(By.XPATH, "//a[contains(@class, 's-pagination-next')]")
        next_button.click()
        time.sleep(5)  # Wait for the next page to load
        page += 1
    except Exception as e:
        print(f"No more pages found: {e}")
        break

# Limit to 10 laptops
all_laptops = all_laptops[:10]

# Step 5: Create a dataframe of the scraped data
columns = ["Title", "Ratings", "Price"]
df = pd.DataFrame(all_laptops, columns=columns)

# Print the dataframe
print(df)

# Close the driver
driver.quit()

# Optionally, save the dataframe to a CSV file
df.to_csv("amazon_laptops.csv", index=False)


# In[6]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Question 6:
driver = webdriver.Chrome()

# Step 1: Go to the AZ Quotes website
driver.get("https://www.azquotes.com/")

# Step 2: Click on "Top Quotes"
time.sleep(5)  # Wait for the page to load
top_quotes_link = driver.find_element(By.LINK_TEXT, "Top Quotes")
top_quotes_link.click()

# Function to scrape one page of quotes
def scrape_page():
    quotes = []
    quote_elements = driver.find_elements(By.XPATH, "//div[@class='wrap-block']/div[@class='quote']")
    for quote_element in quote_elements:
        try:
            quote_text = quote_element.find_element(By.CLASS_NAME, "title").text
            author = quote_element.find_element(By.CLASS_NAME, "author").text
            type_of_quote = quote_element.find_element(By.CLASS_NAME, "tags").text
            quotes.append([quote_text, author, type_of_quote])
        except Exception as e:
            print(f"Error occurred: {e}")
    return quotes

# Step 3: Scrape the data for the top 1000 quotes
all_quotes = []
page = 1
while len(all_quotes) < 1000:
    print(f"Scraping page {page}")
    all_quotes.extend(scrape_page())
    if len(all_quotes) >= 1000:
        break
    try:
        next_button = driver.find_element(By.LINK_TEXT, "Next")
        next_button.click()
        time.sleep(5)  # Wait for the next page to load
        page += 1
    except Exception as e:
        print(f"No more pages found or error occurred: {e}")
        break

# Limit to 1000 quotes
all_quotes = all_quotes[:1000]

# Step 4: Create a dataframe of the scraped data
columns = ["Quote", "Author", "Type of Quotes"]
df = pd.DataFrame(all_quotes, columns=columns)

# Print the dataframe
print(df)

# Close the driver
driver.quit()

# Optionally, save the dataframe to a CSV file
df.to_csv("top_1000_quotes.csv", index=False)


# In[ ]:




