# main.py
from multiprocessing import Pool
from linkedin_scraper import scrape_profile
import pandas as pd
from selenium import webdriver
import pickle


def scrape_profiles_multiprocessing(profiles, num_processes):
    with Pool(num_processes) as pool:
        results = pool.map(scrape_profile, profiles)
    return results

if __name__ == "__main__":
    profiles = [
        "https://linkedin.com/in/aayushshah15",
        "https://linkedin.com/in/pradhit",
        "https://linkedin.com/in/petar-matejic",
        "https://linkedin.com/in/samarth-kadaba-b522491a9",
        "https://linkedin.com/in/john-h-stimac",
        "https://linkedin.com/in/adithyavellal",
        "https://linkedin.com/in/tranquilvarun",
        "https://linkedin.com/in/frances-liu-1a426057",
        "https://linkedin.com/in/marisatcohen",
        "https://linkedin.com/in/vaishant",
        "https://linkedin.com/in/josh-passell-37939a152"
    ]
    # Login and save cookies
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")
    input("login then hit enter")

    # Assuming login is done here
    # ...

    # Save cookies after login
    cookies = driver.get_cookies()
    with open("linkedin_cookies.pkl", "wb") as file:
        pickle.dump(cookies, file)

    driver.quit()

    num_processes = 4  # Adjust based on your system's capabilities
    profile_data_list = scrape_profiles_multiprocessing(profiles, num_processes)
    
    df = pd.DataFrame(profile_data_list)
    sorted_columns = df.iloc[:, 2:].sort_index(axis=1)

    # Concatenate the first two columns with the sorted columns
    df_sorted = pd.concat([df.iloc[:, :2], sorted_columns], axis=1)

    df.to_csv('yc1.csv', sep=',', index=False, encoding='utf-8')
    print(df)