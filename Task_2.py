import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()


url = "http://www.amityvilleschools.org/staff/Default.aspx?school=172"


driver.get(url)
time.sleep(3) 
driver.maximize_window() 


staff_directory = {}


school_name = driver.find_element(By.CLASS_NAME, 'staffSchoolName').text.strip()



departments = driver.find_elements(By.CLASS_NAME, 'staffDepartment')
for department in departments:
    dept_name = department.find_element(By.CLASS_NAME, 'staffDepartmentHeader').text.strip()
    staff_directory[dept_name] = []

    groups = department.find_elements(By.CLASS_NAME, 'staffGroup')
    for group in groups:
        group_name = group.find_element(By.CLASS_NAME, 'staffGroupHeader').text.strip()
        members = group.find_elements(By.CLASS_NAME, 'staffMember')
        for member in members:
            name = member.find_element(By.CLASS_NAME, 'staffMemberLink').text.strip()

            try:
                description = member.find_element(By.CLASS_NAME, 'staffMemberDescription').text.strip()
            except:
                description = "No description"

            staff_directory[dept_name].append({
                'group': group_name,
                'name': name,
                'description': description
            })

# for dept, members in staff_directory.items():
#     print(f"\nDepartment: {dept}")
#     for member in members:
#         print(f"  Group: {member['group']}")
#         print(f"  Name: {member['name']}")
#         print(f"  Description: {member['description']}")

data = []
for dept, members in staff_directory.items():
    for member in members:
        data.append({
            'Name': member['name'],
            'Department': dept,
            'Group': member['group'],
            'Description': member['description']
        })

df = pd.DataFrame(data)
df.to_excel("amityvilleschools_Task_2.xlsx", index=False)

driver.quit()
