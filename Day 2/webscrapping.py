from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import codecs
import re
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

# Function to fetch page source
def fetch_page_source(url):
    driver.get(url)
    wait.until(EC.url_to_be(url))
    return driver.page_source if driver.current_url == url else None

# Get the first URL
val = input("Enter a URL: ")
page_source = fetch_page_source(val)

# Get the second URL
val = input("Enter a valid URL: ").strip()
page_source = fetch_page_source(val)

if page_source:
    soup = BeautifulSoup(page_source, "html.parser")
else:
    print("❌ No valid page source retrieved.")


# Ensure page source is valid
if page_source:
    soup = BeautifulSoup(page_source, "html.parser")

    # Keyword search
    keyword = input("Enter a keyword to find in the article: ")
    matches = re.findall(keyword, soup.get_text(), re.IGNORECASE)
    len_match = len(matches)
    title = soup.title.text if soup.title else "No Title Found"

    # Save results to a file
    with codecs.open("article_scraping.txt", "a+", encoding="utf-8") as file:
        file.write(title + "\n")
        file.write("The following are all instances of your keyword:\n")
        for count, match in enumerate(matches, start=1):
            file.write(f"{count}. {match}\n")
        file.write(f"There were {len_match} matches found for the keyword.\n")

# Close browser
driver.quit()