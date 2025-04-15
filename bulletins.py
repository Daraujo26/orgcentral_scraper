import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrape_course_details(driver, url, division_name):
    """
    Scrape all the courses in a course division from the provided URL.
    """
    driver.get(url)
    try:
        # Wait for the course container to load
        course_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sc_sccoursedescs"))
        )
    except TimeoutException:
        print(f"Error: Timed out waiting for course container at {url}")
        return []

    # Find all course blocks within the container
    course_blocks = course_container.find_elements(By.CLASS_NAME, "courseblock")
    courses = []

    for course in course_blocks:
        try:
            # Extract course code and title
            course_code_title = course.find_element(By.CLASS_NAME, "course_codetitle").get_attribute("innerText").strip()

            # Extract course credits
            course_credits = course.find_element(By.CLASS_NAME, "course_credits").get_attribute("innerText").strip()

            # Extract course description
            try:
                course_desc = course.find_element(By.CLASS_NAME, "courseblockdesc").get_attribute("innerText").strip()
            except Exception:
                course_desc = "N/A"

            # Combine fields into the required format
            full_title = f"{division_name} {course_code_title}"
            text = f"{division_name} {course_code_title}\n{course_credits}\n{course_desc}\n"

            # Append the flat course details
            courses.append({
                "url": url,
                "title": full_title,
                "text": text
            })
        except Exception as e:
            print(f"Error scraping course block: {e}")

    return courses


def main():
    print("Starting scrape")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://bulletins.psu.edu/university-course-descriptions/undergraduate/")
    assert "Penn State" in driver.title

    # Find all undergraduate courses A-Z
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "az_sitemap"))
    )
    undergrad_courses = elem.find_elements(By.TAG_NAME, 'ul')[1:]  # Ignore the first div that holds the "AzMenu"

    # Pre-collect all division URLs and names
    division_links = []
    for ul in undergrad_courses:
        list_items = ul.find_elements(By.TAG_NAME, 'li')
        for li in list_items:
            try:
                anchor = li.find_element(By.TAG_NAME, 'a')
                division_links.append({
                    "name": anchor.text.strip(),
                    "url": anchor.get_attribute('href')
                })
            except Exception as e:
                print(f"Error collecting division: {e}")

    print(f"Collected {len(division_links)} divisions. Starting detailed scrape...")

    all_courses = []
    for division in division_links:
        division_name = division["name"]
        division_url = division["url"]

        print(f"Scraping division: {division_name}, URL: {division_url}")

        # Scrape the courses in this division
        courses = scrape_course_details(driver, division_url, division_name)

        # Append to the overall course list
        all_courses.extend(courses)

    # Save the results to a JSON file
    with open("penn_state_courses_flat.json", "w", encoding="utf-8") as f:
        json.dump(all_courses, f, ensure_ascii=False, indent=4)

    driver.quit()
    print("Scrape complete. Results saved to 'penn_state_courses_flat.json'.")


if __name__ == '__main__':
    main()
