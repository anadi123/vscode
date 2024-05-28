import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape data from a single page
def scrape_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='genTbl js-all-tables')

    data = []
    headers = []

    # Extracting headers
    for header in table.find_all('th'):
        headers.append(header.text.strip())

    # Extracting data rows
    for row in table.find_all('tr'):
        row_data = []
        for td in row.find_all('td'):
            row_data.append(td.text.strip())
        if row_data:
            data.append(row_data)

    return headers, data

# Main function to scrape data from all pages
def scrape_all_pages(base_url, num_pages):
    all_data = []
    for page in range(1, num_pages + 1):
        url = f"{base_url}&pn={page}"
        headers, data = scrape_page(url)
        all_data.extend(data)
    return headers, all_data

# URL of the page to scrape
base_url = "https://www.investing.com/stock-screener/?sp=country::14|sector::a|industry::a|equityType::a|exchange::46|eq_market_cap::100000000,18470000000000|last::300,1500|ADX::20,50|eq_beta::-2,2%3Ctech_sum_month;1"
num_pages = 10

# Scrape data from all pages
headers, all_data = scrape_all_pages(base_url, num_pages)

# Convert data to pandas DataFrame
df = pd.DataFrame(all_data, columns=headers)

# Export DataFrame to Excel
df.to_excel('stock_data.xlsx', index=False)
