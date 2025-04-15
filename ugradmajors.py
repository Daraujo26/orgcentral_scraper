import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementNotInteractableException,
    NoSuchElementException,
    ElementClickInterceptedException,
)

def scrape_majors_on_page(driver, base_url):
    """
    Scrape all the majors on the current page.
    """
    try:
        majors_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "theme-cache-c87vln"))
        )
    except TimeoutException:
        print("Error: Timed out waiting for majors container")
        return []

    major_cards = majors_container.find_elements(By.CLASS_NAME, "theme-cache-11rhcct")
    print(f"Found {len(major_cards)} major cards.")
    majors = []

    for i, card in enumerate(major_cards):
        retry_count = 3
        while retry_count > 0:
            try:
                # Scroll to the element
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                time.sleep(0.5)  # Allow time for scroll stabilization

                WebDriverWait(driver, 3).until(EC.visibility_of(card))
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable(card)).click()

                details_container = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "theme-cache-1qh5309"))
                )

                description_elements = details_container.find_elements(By.TAG_NAME, "p")
                descriptions = "\n".join(
                    [desc.get_attribute("innerText").strip() for desc in description_elements]
                )

                try:
                    title_element = details_container.find_element(By.TAG_NAME, "h2")
                    title = title_element.get_attribute("innerText").strip()
                except NoSuchElementException:
                    title = f"Major {i} (Title not found)"

                majors.append({
                    "title": title,
                    "description": descriptions,
                    "url": base_url  # Add the URL
                })

                close_button = details_container.find_element(By.CLASS_NAME, "theme-cache-1tackaf")
                driver.execute_script("arguments[0].click();", close_button)

                WebDriverWait(driver, 2).until(EC.invisibility_of_element(details_container))
                print(f"Successfully scraped: {title}")

                break  # Exit retry loop on success
            except (TimeoutException, ElementNotInteractableException, ElementClickInterceptedException) as e:
                retry_count -= 1
                print(f"Error processing card {i}: {e}. Retrying ({3 - retry_count}/3)...")
                driver.execute_script("window.scrollBy(0, -100);")  # Scroll slightly up to avoid overlap
                time.sleep(1)  # Delay before retrying
            except Exception as e:
                print(f"Unhandled error processing card {i}: {e}")
                break

    return majors

def scrape_all_pages(driver, url):
    """
    Scrape majors across all pages.
    """
    driver.get(url)
    all_majors = []

    while True:
        majors_on_page = scrape_majors_on_page(driver, url)
        all_majors.extend(majors_on_page)

        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//li[@aria-label='Go to next page']"))
            )
            if next_button.get_attribute("aria-disabled") == "true":
                print("Reached the last page.")
                break

            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)  # Allow time for the next page to load
        except TimeoutException:
            print("Next page button not found or last page reached.")
            break

    return all_majors

def main():
    print("Starting scrape")
    options = Options()
    options.headless = False
    driver = webdriver.Firefox(options=options)

    try:
        base_url = "https://www.psu.edu/academics/undergraduate/majors"
        driver.get(base_url)
        assert "Penn State" in driver.title

        all_majors = scrape_all_pages(driver, base_url)

        with open("majors.json", "w", encoding="utf-8") as f:
            json.dump(all_majors, f, ensure_ascii=False, indent=4)
    finally:
        driver.quit()

    print("Scrape complete. Results saved to 'majors.json'.")

if __name__ == '__main__':
    main()
