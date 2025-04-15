import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from utils.getLink import getLink

def main():
    print("Starting scrape")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://orgcentral.psu.edu/organizations")
    assert "Penn State" in driver.title

    # Collapse load more button
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

    organizations = []
    for i, link in enumerate(links):
        print(f'Opening link {str(i+1)}')
        data = getLink(driver, link)  # Pass driver to getLink
        if data:  # Ensure the scraper didn't return empty data
            title, bio, contact, addtl, _, link_url = data
            combined_text = f"{bio}\n\n{contact}\n\n{addtl}"
            organizations.append({
                "title": title,
                "text": combined_text,
                "url": link_url
            })

    # Write JSON to file
    with open('orgcentral.json', 'w') as file:
        json.dump(organizations, file, indent=4)

    print("Done")
    assert "No results found." not in driver.page_source
    driver.close()

if __name__ == '__main__':
    main()
