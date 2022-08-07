from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import sqlite3
import os
from time import sleep

con = sqlite3.connect(os.path.dirname(
            os.path.abspath(__file__)) + "/db.db")
cur = con.cursor()
cur.executescript(open(os.path.dirname(os.path.abspath(__file__)) + '/dump.sql').read())
con.commit()
con.close()

con = sqlite3.connect(os.path.dirname(
            os.path.abspath(__file__)) + "/db.db")
cur = con.cursor()
driver = webdriver.Firefox()
for i in range(8):
    driver.get(f"https://www.susu.ru/ru/about/official/plans?field_year_begin_value=All&field_department_filter_value_1=All&page={i}")
    sleep(0.6)
    main = driver.find_element(By.CLASS_NAME, 'view-content')
    spisk = main.find_elements(By.TAG_NAME, 'li')
    links = ((j.find_element(By.TAG_NAME, 'a'), (j.find_elements(By.TAG_NAME, 'div')[-1].text if len(j.find_elements(By.TAG_NAME, 'div'))>=2 else '')) for j in spisk)
    for a, b in links:
        try:
            sleep(0.3)
            driver2 = webdriver.Firefox()
            cur.execute("""INSERT INTO Directions(name) VALUES (?)""", (a.text+' '+b,))
            cur.execute("""SELECT id FROM Directions WHERE name = (?)""", (a.text+' '+b,))
            id_dir = int(cur.fetchone()[0])
            driver2.get("https://www.susu.ru" + a.get_attribute('href') if 'susu' not in a.get_attribute('href') else a.get_attribute('href'))
            sleep(0.6)
            page = driver2.find_element(By.TAG_NAME,'tbody')
            for rows in page.find_elements(By.TAG_NAME, 'tr'):
                row = rows.find_elements(By.TAG_NAME, 'td')
                name, semm, hours = row[0].text, ', '.join(row[1].text.strip().split(';\n')), int(row[3].text)*36
                cur.execute("""INSERT INTO Disciplines VALUES (?,?,?,?)""", (name, semm, id_dir, hours))
            driver2.close()
        except:
            driver2.close()
            continue

con.commit()
con.close()
driver.close()