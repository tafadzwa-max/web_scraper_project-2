# Zimbabwe Job Scraper (vacancymail.co.zw)

This Python script scrapes job listings from [vacancymail.co.zw](https://vacancymail.co.zw) and saves the data into a CSV file. It’s designed for automation, with scheduled scraping and logging support to help track job updates daily.

## Project Structure

. ├── logs/ │ └── scraper.log # Log file with runtime details ├── scraped_data.csv # Output file with scraped job data ├── scraper.py # Main script file └── README.md # Project documentation

##  Features

- Scrapes job title, company, location, expiry date, and description
- Cleans and deduplicates data before saving
- Saves output to `scraped_data.csv`
- Logs activity and errors to `logs/scraper.log`
- Option for scheduled daily scraping using the `schedule` module

##  Requirements

Install the dependencies using:

```bash
pip install -r requirements.txt
Dependencies:

requests

beautifulsoup4

pandas

schedule

To create your own requirements.txt:

requests
beautifulsoup4
pandas
schedule
 Usage
Run Once (Immediate Scrape):

python scraper.py
Enable Daily Automation:
Uncomment this line in the scraper.py file:

#run_scheduled_scraping()  # Uncomment to enable scheduling
Then run the script:

python scraper.py
The script will scrape jobs daily at 09:00 AM and run continuously in the background.

🗃️ Output Example
scraped_data.csv includes:


Job Title	Company	Location	Expiry Date	Description	Scraped At
Data Analyst	ZimTech	Harare	2025-04-30	Seeking data analyst with experience	2025-04-15 09:00:00
🛡️ Logging
All logs are saved in the logs/ folder:

logs/scraper.log
Sample log output:

2025-04-15 09:00:00 - INFO - Starting scrape job
2025-04-15 09:00:03 - INFO - Scraped and saved 12 job(s).

Notes
If the scraper doesn't return any jobs, inspect scraper.log and confirm the HTML structure hasn't changed.

Make sure your internet is active and stable during scraping.

Don’t forget to run the script again if you close it while scheduling is active.

 To-Do / Improvements
Add email alerts for new job posts

Export data to Excel or JSON

Build a basic dashboard to visualize scraped data

Dockerize the project for easier deployment

👨🏽‍💻 Author
Built with ❤️ by Tafadzwa.
Feel free to connect and contribute.

