import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = 'https://brk.ossiningufsd.org/staff-directory-v2'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)
driver.maximize_window()

search_button = driver.find_element(By.XPATH, "//a[@class='fs_style_4 fs_style_10' and @data-page-name='District Staff Directory']")
search_button.click()
time.sleep(3)


WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'fsConstituentItem')))

data = []


while True:

    time.sleep(3)
    
    # main xpath
    staff_list = driver.find_elements(By.CLASS_NAME, 'fsConstituentItem')


    for staff in staff_list:
        # Extract Name
        name = staff.find_element(By.CLASS_NAME, 'fsConstituentProfileLink').text.strip()
        

        try:
            title = staff.find_element(By.CLASS_NAME, 'fsTitles').text.strip().replace('Titles:', '').strip()
        except:
            title = 'N/A'
        

        try:
            department = staff.find_element(By.CLASS_NAME, 'fsDepartments').text.strip().replace('Departments:', '').strip()
        except:
            department = 'N/A'
        

        try:
            email_link = staff.find_element(By.CSS_SELECTOR, 'div.fsEmail a')
            email = email_link.get_attribute('href').replace('mailto:', '')
        except:
            email = 'N/A'

        # Append the data to the list
        data.append({
            'Name': name,
            'Title': title,
            'Department': department,
            'Email': email
        })
        df = pd.DataFrame(data)
        df.to_excel('staff_Task_3.xlsx', index=False)

   #pagination
    next_button = driver.find_elements(By.CLASS_NAME, 'fsNextPageLink')
    if next_button:

        if 'disabled' in next_button[0].get_attribute('class'):
            print("No more pages to scrape. Exiting.")
            break
        else:

            next_button[0].click()
            print("Moving to the next page...")
    else:
        print("No more pages to scrape. Exiting.")
        break

#excel saving

driver.quit()
print("Data saved to 'staff_Task_3.xlsx'.")
