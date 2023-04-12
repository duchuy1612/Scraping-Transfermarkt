from bs4 import BeautifulSoup
from selenium import webdriver
import csv

footballers, clubs, nations, ages, prices, positions = [], [], [], [], [], []
footballer_dict = []

driver = webdriver.Chrome()

for page in range(1, 23, 1):
    page_url = 'https://www.transfermarkt.com/premier-league/marktwertaenderungen/wettbewerb/GB1/pos//detailpos/0/verein_id/0/land_id/0/plus/1' + '/page/' + str(page)
    driver.get(page_url)
    html_iter = driver.page_source
    soup = BeautifulSoup(html_iter,"html.parser")

    # Name scraping
    find_footballer = soup.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['hauptlink'])
    for td in find_footballer:
        a = td.find_all("a")
        row = [i.text for i in a]
        footballers.append(row)
    
    # Club scraping
    find_club = soup.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['zentriert'])
    for td in find_club:
        a = td.find_all("a")
        row = [i.get('title') for i in a]
        clubs.append(row) 
    
    # Nation scraping
    find_nation = soup.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['zentriert'])
    for td in find_nation:
        img = td.find_all(lambda tag: tag.name == 'img' and tag.get('class') == ['flaggenrahmen'])
        row = [i.get('title') for i in img]
        nations.append(row)

    # Age scraping
    find_age = soup.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['zentriert'] and not tag.find_all('img'))
    ages.append([i.text for i in find_age])
    
    # Position scraping
    find_position = soup.find_all(lambda tag: tag.name == 'table' and tag.get('class') == ['inline-table'])
    for table in find_position:
        td = table.find_all(lambda tag: tag.name == 'td' and not tag.get('class'))
        row = [i.text for i in td if i.text not in ('', '\n ')]
        positions.append(row)

    # Value scraping
    find_price = soup.find_all(lambda tag: tag.name == 'td' and (tag.get('class') == ['rechts','hauptlink'] or tag.get('class') == ['rechts','hauptlink','mwHoechstwertKarriere']))
    prices.append([i.text.replace("\xa0\xa0", "") for i in find_price])


# Flatten lists
flat_footballers = [item for sublist in footballers for item in sublist]
flat_clubs = [item for sublist in clubs for item in sublist]
nations_edit = [nation for nation in nations if nation != []]
flat_nations = [nation[0] + ', ' + nation[1] if len(nation) == 2 else nation[0] for nation in nations_edit]
flat_ages = [item for sublist in ages for item in sublist]
flat_positions = [item for sublist in positions for item in sublist]
flat_prices = [item for sublist in prices for item in sublist]


# List of footballers and their current prices
for footballer, position, club, nation, age, price in zip(flat_footballers, flat_positions, flat_clubs, flat_nations, flat_ages, flat_prices):
    footballer_dict.append({"Name" : footballer, "Position" : position, "Club" : club,"Nation": nation,"Age": age, "Current Value" : price})

myFile = open('footballer_info.csv', 'w', encoding="utf-16", newline='')
writer = csv.DictWriter(myFile, fieldnames=['Name', 'Position', 'Club', 'Nation', 'Age', 'Current Value'], delimiter='\t')
writer.writeheader()
writer.writerows(footballer_dict)
myFile.close()

