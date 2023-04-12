from bs4 import BeautifulSoup
from selenium import webdriver
import csv

footballers, clubs, nations, appearances, positions, goals = [], [], [], [], [], []
footballer_dict = []

driver = webdriver.Chrome()

for page in range(1, 10, 1):
    page_url = 'https://www.transfermarkt.com/laliga/torschuetzenliste/wettbewerb/ES1/ajax/yw1/saison_id/2022' + '/page/' + str(page)
    driver.get(page_url)
    html_iter = driver.page_source
    soup = BeautifulSoup(html_iter,"html.parser")

    main_table = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['responsive-table'])
    
    for table in main_table: 
        # Name scraping  
        find_footballer = table.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['hauptlink'])
        for td in find_footballer:
            a = td.find_all("a")
            row = [i.text for i in a]
            footballers.append(row)
        
        # Club scraping
        find_club = table.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['zentriert'] or tag.text == 'for 2 clubs')
        for td in find_club:
            img = td.find_all(lambda tag: tag.name == 'img' and tag.get('class') != ['flaggenrahmen'])
            if img:
                row = [i.get('title') for i in img]
                clubs.append(row)
            elif td.text == 'for 2 clubs':
                clubs.append([td.text])
                
        # Position scraping
        find_position = table.find_all(lambda tag: tag.name == 'table' and tag.get('class') == ['inline-table'])
        for tb in find_position:
            td = tb.find_all(lambda tag: tag.name == 'td' and not tag.get('class'))
            row = [i.text for i in td if i.text not in ('', '\n ')]
            positions.append(row)    
            
        # Nation scraping
        find_nation = table.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['zentriert'])
        for td in find_nation:
            img = td.find_all(lambda tag: tag.name == 'img' and tag.get('class') == ['flaggenrahmen'])
            row = [i.get('title') for i in img]
            nations.append(row)

        # Appearance scraping
        find_appearance = table.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['zentriert'] and not tag.find_all('img') and tag.text != 'for 2 clubs')
        for td in find_appearance:
            a = td.find_all("a")
            row = [i.text for i in a]
            appearances.append(row)
            
        # Goals scraping
        find_goal = table.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['zentriert', 'hauptlink'])
        for td in find_goal:
            a = td.find_all("a")
            row = [i.text for i in a]
            goals.append(row)
    
# Flatten lists
flat_footballers = [item for sublist in footballers for item in sublist]
flat_clubs = [item for sublist in clubs for item in sublist]
nations_edit = [nation for nation in nations if nation != []]
flat_nations = [nation[0] + ', ' + nation[1] if len(nation) == 2 else nation[0] for nation in nations_edit]
flat_appearances = [item for sublist in appearances for item in sublist]
flat_positions = [item for sublist in positions for item in sublist]
flat_goals = [item for sublist in goals for item in sublist]

print(flat_nations)
print(flat_appearances)
print(flat_goals)

# List of footballers and their current prices
for footballer, club, nation, position, appearance, goal in zip(flat_footballers, flat_clubs, flat_nations, flat_positions, flat_appearances, flat_goals):
    footballer_dict.append({"Name" : footballer,"Club" : club, "Nation": nation, "Position": position,"Appearances": appearance, "Goals": goal})

print(footballer_dict)        
  
myFile = open('footballer_goals_laliga.csv', 'w', encoding="utf-16", newline='')
writer = csv.DictWriter(myFile, fieldnames=['Name', 'Position', 'Club', 'Nation', 'Appearances', 'Goals'], delimiter='\t')
writer.writeheader()
writer.writerows(footballer_dict)
myFile.close()