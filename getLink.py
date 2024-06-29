from selenium import webdriver
from selenium.webdriver.common.by import By

def getLink(link: str):
    driver = webdriver.Firefox()
    driver.get(link)
    assert "Penn State" in driver.title

    try:
        title = driver.find_element(By.XPATH, "//h1[1]").text
    except:
        title = ''
    try:
        bio = driver.find_element(By.XPATH, "//div[@class='bodyText-large userSupplied']").text
    except:
        bio = ''
    try:
        contact = driver.find_element(By.XPATH, "//div[@id='react-app']/div/div[@role='main']/div[1]/div[1]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]").text
    except:
        contact = ''
    try:
        addtl = driver.find_element(By.XPATH, "//div[@id='react-app']/div/div[@role='main']/div[1]/div[1]/div[1]/div[2]/div/div[5]/div[1]/div[2]/div[1]").text
    except:
        addtl = ''
    try:
        officers = driver.find_element(By.XPATH, "//div[@id='react-app']/div[1]/div[1]/div[1]/div[5]/div[1]/div[1]/div[2]/div[1]")
        officers_list = [text for text in officers.text.split('\n') if len(text) > 1]
        officers = []
        for i in range(0, len(officers_list)-1, 2):
            officers.append(f"{officers_list[i]}-{officers_list[i+1]}")
        officers = ", ".join(officers)
    except:
        officers = ''

    # scraper takes the letter in the officers profile pic so you have to filter it out
    driver.quit()
    return [title, bio, contact, addtl, officers, link]