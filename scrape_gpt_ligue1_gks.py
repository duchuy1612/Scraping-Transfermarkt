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


for page in range(1, 3):
    # Define the URL to scrape
    page_url = 'https://www.transfermarkt.com/ligue-1/weisseWeste/wettbewerb/FR1/saison_id/2022/plus/1' + '/page/' + str(page)

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
        name = trs[0].find(lambda tag: tag.name =='a' and tag.get('href') != '#').text
        position = 'Goalkeeper'
        club = trs[1].find('td').text
        nationality = ', '.join([i.get('title') for i in cols[1].find_all('img')])
        matches = int(cols[2].text.strip())
        clean_sheets = int(cols[3].text.strip())
        goal_conceded = int(cols[4].text.strip()) if cols[4].text.strip() != '-' else 0
        minutes_played = cols[5].text.strip().replace('.', '')
        minutes_played = int(minutes_played.replace("'", ''))
        minutes_per_goal_against = int(cols[6].text.strip()) if cols[6].text.strip() != '-' else 0
        percentage = float(cols[7].text.strip().replace('%', '')) if cols[7].text.strip() != '%' else 0.0

        # Add the player information to the list
        player_info_list.append({
            'Name': name,
            'Position': position,
            'Nationality': nationality,
            'Club': club,
            'Appearances': matches,
            'Clean Sheets': clean_sheets,
            'Goal Conceded': goal_conceded,
            'Minutes Played': minutes_played,
            'Minutes Per Goal Against': minutes_per_goal_against,
            'Percentage': percentage,
        })
# Close the webdriver
driver.quit()

# Export the player information to a CSV file
with open('player_stats_ligue1_gks.csv', 'w', encoding='utf-16', newline='') as f:
    # Create a CSV writer object with tabs as the delimiter
    writer = csv.DictWriter(f, fieldnames=player_info_list[0].keys(), delimiter='\t')
    
    # Write the header row
    writer.writeheader()
    
    # Write the player information rows
    writer.writerows(player_info_list)
