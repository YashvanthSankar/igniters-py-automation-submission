import json
import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


FORM_URL = "https://forms.gle/3rGDeDSJaJupz7A48"
DELAY_MIN = 1.0  
DELAY_MAX = 2.5  
SUBMISSION_DELAY_MIN = 2.0
SUBMISSION_DELAY_MAX = 4.0


with open('config.json', encoding='utf-8') as file:
    config = json.load(file)

df = pd.read_csv('hospital_er_data.csv')

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(5)

print(f"[INFO] Starting form filling for {len(df)} patients...\n")

for index, row in df.iterrows():
    try:
        print(f"[INFO] Processing Patient ID: {row['Patient Id']}")
        driver.get(FORM_URL)
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        driver.find_element(By.XPATH, config["Patient Id"]).send_keys(str(row['Patient Id']))
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        driver.find_element(By.XPATH, config["Patient Admission Date"]).send_keys(row['Patient Admission Date'])
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        driver.find_element(By.XPATH, config["Patient First Initial"]).send_keys(row['Patient First Initial'])
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        driver.find_element(By.XPATH, config["Patient Last Name"]).send_keys(row['Patient Last Name'])
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        driver.find_element(By.XPATH, config["Patient Age"]).send_keys(str(row['Patient Age']))
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        driver.find_element(By.XPATH, config["Patient Race"]).send_keys(str(row['Patient Race']))
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        driver.find_element(By.XPATH, config["Department Referral"]).send_keys(str(row['Department Referral']))
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        driver.find_element(By.XPATH, config["Patient Waittime"]).send_keys(str(row['Patient Waittime']))
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        driver.find_element(By.XPATH, config["Additional Notes"]).send_keys(row.get('Patients CM', ''))
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        gender = row.get('Patient Gender', '').upper()
        if gender == 'M':
            driver.find_element(By.XPATH, config["Patient Gender M"]).click()
        elif gender == 'F':
            driver.find_element(By.XPATH, config["Patient Gender F"]).click()
        else driver.find_element(By.XPATH, config["Patient Gender Other"]).click()  
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))    

        satisfaction_score = int(row.get('Patient Satisfaction Score', 0))
        score_key = f"Patient Satisfaction Score {satisfaction_score}"
        if score_key in config:
            driver.find_element(By.XPATH, config[score_key]).click()
        else:
            print(f"[WARNING] Satisfaction score {satisfaction_score} not found in config.")
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

        try: 
            submit_button = driver.find_element(By.XPATH, "//span[text()='Submit']//span[text()="Submit"]/ancestor::div[@role="button"]")
            submit_button.click()
            print(f"[INFO] Submitted form for Patient ID: {row['Patient Id']}")
        except NoSuchElementException:
            print(f"[ERROR] Submit button not found for Patient ID: {row['Patient Id']}")
            continue
        time.sleep(random.uniform(SUBMISSION_DELAY_MIN, SUBMISSION_DELAY_MAX))
    except Exception as e:
        print(f"[ERROR] An error occurred while processing Patient ID: {row['Patient Id']}. Error: {e}")
        continue

driver.quit()
print("[INFO] Form filling completed.")


