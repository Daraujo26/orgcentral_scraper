import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

from getLink import getLink

def main():
    print("Starting scrape")
    driver = webdriver.Firefox()
    driver.get("https://orgcentral.psu.edu/organizations")
    assert "Penn State" in driver.title

    # collapse load more button
    print("Collapsing load button")
    load_more = driver.find_element(By.XPATH, "//button[@type='button']") 
    while load_more:
        try:
            load_more.click()
        except:
            load_more = False
            print("Done collapsing, getting links")
        
    elem = driver.find_element(By.ID, "org-search-results")
    tags = elem.find_elements(By.TAG_NAME, 'a')
    links = [tag.get_attribute('href') for tag in tags]

    with open('orgcentral.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ['title', 'bio', 'contact', 'addtl', 'officers', 'link']
        writer.writerow(field)
        for i, link in enumerate(links):
            print(f'Opening link {str(i+1)}')
            writer.writerow(getLink(link))

    print("Done")
    assert "No results found." not in driver.page_source
    driver.close()

if __name__ == '__main__':
    main()