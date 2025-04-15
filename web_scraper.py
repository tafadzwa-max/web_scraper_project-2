import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime
import schedule
import time

# Setup Logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

BASE_URL = "https://vacancymail.co.zw"
JOBS_URL = f"{BASE_URL}/jobs/"

def fetch_job_cards():
    try:
        response = requests.get(JOBS_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        job_cards = soup.find_all('div', class_='job-listing-details')

        if not job_cards:
            logging.warning("⚠ No job cards found. Check if class name has changed.")
            print("⚠ No job cards found. Check if class name has changed.")
            return []

        return job_cards

    except Exception as e:
        logging.error(f"Error fetching job cards: {e}")
        print(f"Error fetching job cards: {e}")
        return []

def scrape_job_details(card):
    try:
        title = card.find('h3', class_='job-listing-title')
        title = title.get_text(strip=True) if title else None

        company = card.find('h4', class_='job-listing-company')
        company = company.get_text(strip=True) if company else None

        description = card.find('p', class_='job-listing-text')
        description = description.get_text(strip=True) if description else None

        location_tag = card.find('i', class_='icon-material-outline-location-on')
        location = location_tag.find_parent('li').get_text(strip=True).replace('location_on', '').strip() if location_tag else None

        expiry_tag = card.find('i', class_='icon-material-outline-access-time')
        expiry = expiry_tag.find_parent('li').get_text(strip=True).replace('access_time', '').strip() if expiry_tag else None

        return {
            "Job Title": title,
            "Company": company,
            "Location": location,
            "Expiry Date": expiry,
            "Description": description,
            "Scraped At": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    except Exception as e:
        logging.error(f"Error parsing job card: {e}")
        print(f"Error parsing job card: {e}")
        return None

def clean_data(data):
    df = pd.DataFrame(data)
    df.drop_duplicates(subset=["Job Title", "Company"], inplace=True)
    return df

def scrape_and_save():
    print(" Script is running...")
    logging.info("Starting scrape job")

    job_cards = fetch_job_cards()
    job_data = []

    for card in job_cards:
        job = scrape_job_details(card)
        if job:
            job_data.append(job)

    if job_data:
        df = clean_data(job_data)

        if not os.path.exists("scraped_data.csv"):
            df.to_csv("scraped_data.csv", index=False)
        else:
            existing_df = pd.read_csv("scraped_data.csv")
            combined = pd.concat([existing_df, df], ignore_index=True)
            combined.drop_duplicates(subset=["Job Title", "Company"], inplace=True)
            combined.to_csv("scraped_data.csv", index=False)

        logging.info(f" Scraped and saved {len(df)} job(s).")
        print(f" Scraped and saved {len(df)} job(s).")
    else:
        logging.warning(" No job data scraped.")
        print("No job data scraped.")

def run_scheduled_scraping():
    schedule.every().day.at("09:00").do(scrape_and_save)
    logging.info("Scheduled job scraper started.")
    print(" Scheduler started: Scraping every 24 hours.")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    scrape_and_save()
    run_scheduled_scraping()  # Uncomment to enable scheduling