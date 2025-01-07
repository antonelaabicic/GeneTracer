from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from urllib.parse import urljoin

def initialize_driver(driver_path):
    driver = webdriver.Chrome(service=Service(driver_path))
    return driver

def get_cohort_links(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='cohort']")))
    cohort_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='cohort']")
    return [elem.get_attribute('href') for elem in cohort_elements]

def get_tcga_link(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
        link_element = driver.find_element(By.XPATH, "//a[contains(text(), 'IlluminaHiSeq pancan normalized')]")
        return link_element.get_attribute("href")
    except Exception:
        return None

def click_gz_link(driver):
    try:
        gz_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href$='.gz']")))
        gz_link.click()
        sleep(3)
    except Exception as e:
        pass