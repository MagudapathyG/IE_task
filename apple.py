import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()

try:

    url = "https://www.apple.com/in/leadership/"
    driver.get(url)


    wait = WebDriverWait(driver, 10)
    profile_list_items = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".profile-list-item"))
    )

    profiles = []
    for item in profile_list_items:
        name = item.find_element(By.CSS_SELECTOR, ".profile-name").text
        try:

            designation = item.find_element(By.CSS_SELECTOR, ".typography-profile-title").text.replace("\n", " ")

            profiles.append({"Name": name, "Designation": designation})
            
        except Exception:
            designation = "N/A"  


    for profile in profiles:
        print(profile)

    df = pd.DataFrame(profiles)

    output_path = "apple_leadership_task_1.xlsx"
    df.to_excel(output_path, index=False)
    print(f"Data saved to {output_path}")

finally:

    driver.quit()