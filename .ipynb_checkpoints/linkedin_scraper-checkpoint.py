from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import pickle

chrome_options = Options()
chrome_options.add_argument("--headless")  # Enables headless mode
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model, required on some systems
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems



# Function to scrape profile information
def scrape_profile(url):
    driver = webdriver.Chrome(options=chrome_options)
     
    driver.get("https://www.linkedin.com")
    with open("linkedin_cookies.pkl", "rb") as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']  # Remove expiry date if present
            driver.add_cookie(cookie)
            
    driver.get(url)
    data = {'linkedin_url': url}
    
    try:
        h1_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        data = {'name': h1_element.text}
        experience_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="experience"]/..'))
        )
        companies = get_organizations(experience_element, url, driver)
        driver.get(url)
        for i, company in enumerate(companies):
            data[f'company {i+1}'] = company
        education_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="education"]/..'))
        )
        schools = get_organizations(education_element, url, driver)
        for i, school in enumerate(schools):
            data[f'school {i+1}'] = school
    except Exception as e:
        print(f"Error extracting data for profile: {url} | Error: {e}")
    driver.quit()
    return data


# Function to get experiences or education
def get_organizations(parent_element, url, driver):
    try:
        parent_element.find_element(By.XPATH, './/a[contains(@id,"see-all") and @target="_self"]').click()
        parent_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "scaffold-layout__main"))
        )
    except Exception as e:
        # If it fails, just print the error and move on
        pass
    logo_elements = parent_element.find_elements(By.XPATH, './/a[contains(@href,"company") and @target="_self"]')
    href_links = []
    for element in logo_elements:
        # Get the href attribute of each element and append it to the href_links list
        href_links.append(element.get_attribute("href"))
    href_links = list(set(href_links))
    organizations = []
    for link in href_links:
        driver.get(link)
        try:
            # Attempt to find the h1 element
            h1_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )
            organizations.append(h1_element.text)
        except Exception as e:
            # If h1 element is not found, do nothing
            pass
    # driver.get(url)
    # time.sleep(5)
    return organizations
        
