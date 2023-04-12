import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up Selenium webdriver
driver = webdriver.Chrome()

# Initialize an empty list to store the player information
player_info_list = []

for page in range(1, 14):
    # Define the URL to scrape
    page_url = 'https://www.transfermarkt.com/bundesliga/scorerliste/wettbewerb/L1/saison_id/2022/altersklasse/alle/plus/1' + '/page/' + str(page)

    # Open the URL in the webdriver
    driver.get(page_url)

    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.items')))

    # Get the page source and parse it with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the table containing the player information
    table = soup.find('table', class_='items')
    tbody = table.find('tbody')

    # Loop through each row of the table and extract the player information
    for row in tbody.find_all(lambda tag: tag.name == 'tr' and tag.get('class') in (['odd'], ['even']))[0:]:
        # Get the columns in the row
        cols = row.find_all(lambda tag: tag.name == 'td' and tag.get('class') in (['zentriert'], ['rechts'], ['zentriert','hauptlink']))
        # Extract the player information
        inline = row.find(lambda tag: tag.name == 'table' and tag.get('class') == ['inline-table'])
        trs = inline.find_all('tr')
        name = trs[0].find('a').text
        position = trs[1].find('td').text
        club = 'for 2 clubs' if not cols[1].find('img') else cols[1].find('img').get('title')
        nationality = ', '.join([i.get('title') for i in cols[2].find_all('img')])
        age = int(cols[3].text.strip()) if not cols[3].text.strip().find('\xa0') else int(cols[3].text.strip()[0:2])
        appearances = int(cols[4].text.strip())
        goals = int(cols[7].text.strip())
        assists = int(cols[8].text.strip())	
        points = int(cols[9].text.strip())
        
        # Add the player information to the list
        player_info_list.append({
            'Name': name,
            'Position': position,
            'Nationality': nationality,
            'Age': age,
            'Club': club,
            'Appearances': appearances,
            'Assists': assists,
            'Goals': goals,
            'Points': points
        })
# Close the webdriver
driver.quit()

# Export the player information to a CSV file
with open('player_stats_bundesliga_extra.csv', 'w', encoding='utf-16', newline='') as f:
    # Create a CSV writer object with tabs as the delimiter
    writer = csv.DictWriter(f, fieldnames=player_info_list[0].keys(), delimiter='\t')
    
    # Write the header row
    writer.writeheader()
    
    # Write the player information rows
    writer.writerows(player_info_list)