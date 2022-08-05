from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
driver = webdriver.Firefox()
arr = {}
driver.get("https://www.susu.ru/ru/plan/090301-2020-40-informatika-i-vychislitelnaya-tehnika-31658")
sleep(3)
page = driver.find_element(By.TAG_NAME,'tbody')
mx_len = 0
for i in page.find_elements(By.TAG_NAME, 'tr'):
    row = i.find_elements(By.TAG_NAME, 'td')
    if row[3].text != '0':
        arr[row[0].text] = (', '.join(row[1].text.strip().split(';\n')), str(int(row[3].text)*36)+'ч')
        mx_len = max(len(row[0].text), mx_len)

driver.close()
for i in arr:
    print(i + ' '*(mx_len - len(i) + 5) + '|' + ' '*5 + (' '*(5-len(arr[i][0])+5)+'|'+' '*5).join(arr[i]))