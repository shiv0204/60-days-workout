from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--lang=en-US")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 30)  # Increased timeout to 30 seconds

# Function to fetch page source
def fetch_page_source(url):
    try:
        print(f"🌐 Fetching URL: {url}")
        driver.get(url)
        
        # Wait for the movie list to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list-summary-item")))
        
        print("✅ Page loaded successfully.")
        return driver.page_source
    except TimeoutException:
        print("❌ Page load timed out. The page might be taking too long to load.")
        # Take a screenshot for debugging
        driver.save_screenshot("debug_screenshot.png")
        print("📸 Screenshot saved as 'debug_screenshot.png'.")
    except WebDriverException as e:
        print(f"❌ Error fetching page source: {e}")
    return None

# URL for IMDb's Top 250 Movies
url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
page_source = fetch_page_source(url)

if page_source:
    soup = BeautifulSoup(page_source, "html.parser")
    
    # Find all movie entries
    movie_list = soup.find_all("li", class_="ipc-metadata-list-summary-item")
    
    # Extract movie titles and ratings
    movies = []
    for movie in movie_list:
        # Extract title
        title_element = movie.find("h3", class_="ipc-title__text")
        title = title_element.get_text(strip=True) if title_element else "N/A"
        
        # Extract rating
        rating_element = movie.find("span", class_="ipc-rating-star--imdb")
        rating = rating_element.get_text(strip=True).split()[0] if rating_element else "N/A"
        
        movies.append({"Title": title, "Rating": rating})
    
    # Save to a CSV file
    df = pd.DataFrame(movies)
    df.to_csv("top_250_movies.csv", index=False)
    print("✅ Data saved to 'top_250_movies.csv'.")
else:
    print("❌ No valid page source retrieved.")

# Close browser
driver.quit()