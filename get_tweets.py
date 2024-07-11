from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Initialize the WebDriver (make sure you have the correct path to the WebDriver executable)
# Initialize the WebDriver service
service = Service(ChromeDriverManager().install())

# Configure Chrome options (if needed)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Function to scrape tweets


def get_tweets(query, max_tweets):
    driver.get(f'https://twitter.com/search?q={query}&src=typed_query')
    time.sleep(2)  # Let the page load

    tweets = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(tweets) < max_tweets:
        tweet_elements = driver.find_elements(
            By.XPATH, '//article[@data-testid="tweet"]')

        for tweet_element in tweet_elements:
            try:
                username = tweet_element.find_element(
                    By.XPATH, './/span[contains(text(), "@")]').text
                content = tweet_element.find_element(
                    By.XPATH, './/div[2]/div[2]/div[1]').text
                date = tweet_element.find_element(
                    By.XPATH, './/time').get_attribute('datetime')
                likes = tweet_element.find_element(
                    By.XPATH, './/div[@data-testid="like"]').text
                retweets = tweet_element.find_element(
                    By.XPATH, './/div[@data-testid="retweet"]').text

                tweet_details = {
                    "username": username,
                    "created_at": date,
                    "content": content,
                    "likes": likes,
                    "retweets": retweets
                }

                if tweet_details not in tweets:
                    tweets.append(tweet_details)

                if len(tweets) >= max_tweets:
                    break
            except Exception as e:
                continue

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    return tweets


# Fetch tweets
query = "e-levy"
max_tweets = 10
tweets = get_tweets(query, max_tweets)

# Create DataFrame and save to CSV
df = pd.DataFrame(tweets)
df.to_csv('./Data/Raw/tweets.csv', index=False)
print(df)

# Close the WebDriver
driver.quit()
