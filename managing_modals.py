import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
import os

def close_modal(driver):
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept all') or \
                                            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept all cookies') or \
                                            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept cookies') or \
                                            contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]")))

        accept_button.click()
        print("Cookie popup handled: Cookies accepted.")
        # Wait a brief moment for the DOM to settle
        WebDriverWait(driver, 5).until(EC.invisibility_of_element(accept_button))
    except (TimeoutException, NoSuchElementException):
        try:
            print("No cookie popup detected or 'Accept' button not found. Looking for a link instead ...")

            accept_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept all') or \
                                                contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept all cookies') or \
                                                contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept cookies') or \
                                                contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]")))
            accept_link.click()
            print('accept link found!')
            # Wait a brief moment for the DOM to settle
            WebDriverWait(driver, 5).until(EC.invisibility_of_element(accept_link))                
        except (TimeoutException, NoSuchElementException):
            print('No Accept link found. Assuming page loaded with job URLs')

def wait_for_page_load(timeout=10):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

def find_all_links(driver, url, i):
    wait_for_page_load()
    all_links_attributes = []
    a_tags = driver.find_elements(By.TAG_NAME, 'a')

    for a in a_tags:
        attributes = driver.execute_script(
            '''
            let items = {}; 
            for (let attr of arguments[0].attributes) {
                items[attr.name] = attr.value;
            } 
            return items;
            ''',
            a
        )

        updated_attributes = {'url_id': i+1, 'url': url}
        updated_attributes.update(attributes)
        all_links_attributes.append(updated_attributes)
            
    # Print attributes (optional for debugging)
    for attr in all_links_attributes:
        print(attr)

    # Write attributes to file
    with open('output.txt', 'a') as f:
        # Convert attributes to a JSON string for readability
        json.dump(all_links_attributes, f, indent=2)
    
    return all_links_attributes

def find_all_input_fields():
    input_field_tags = driver.find_elements(By.TAG_NAME, 'input')
    
    input_fields = [(i.get_attribute('type')) for i in input_field_tags]
    print(input_fields)
    
    return input_fields    

def clear_cookies_for_sites(driver, websites):
    for website in websites:
        # Open the website
        driver.get(website)
        
        # Clear all cookies for the current website
        driver.delete_all_cookies()
        
        print(f"Cleared cookies for {website}")            

def setup_selenium():
    options = Options()

    # adding arguments
    options.add_arguments("--disable-gpu")

def print_all_cookies(driver):
    # Get all cookies
    cookies_list = driver.get_cookies()

    # Print cookies
    for cookie in cookies_list:
        print(cookie)

if __name__ == "__main__":
    os.system('cls')

    with open('urls.txt') as f:
        urls = f.readlines()

    driver = webdriver.Chrome()

    for i in range(len(urls)):
        url = urls[i]
        print(f"\nURL {i + 1}: {url}")
        driver.get(url)
        # print_all_cookies(driver)
        close_modal(driver)
        find_all_links(driver, url, i)


    # clear_cookies_for_sites(driver, urls)
    driver.quit()