from math import e
import os
from time import sleep
import scraping.selenium_setup as Scraper
import file_managment.file_operations as FileManager
import file_managment.path_config as PathConfig


def main():
    try:
        driver_path, gz_folder, unzipped_folder, processed_folder = PathConfig.setup_paths()
        driver = Scraper.initialize_driver(driver_path)
        driver.get("https://xenabrowser.net/datapages/?hub=https://tcga.xenahubs.net:443")
        sleep(3)

        cohort_links = Scraper.get_cohort_links(driver)
        for cohort_link in cohort_links:
            driver.get(cohort_link)
            sleep(5)

            tcga_link = Scraper.get_tcga_link(driver)
            if tcga_link:
                driver.get(tcga_link)
                Scraper.click_gz_link(driver)
                sleep(5)
            else:
                pass

            FileManager.wait_for_all_downloads()
            FileManager.process_gz_files(gz_folder, unzipped_folder, processed_folder)

    except Exception as e:
        raise Exception(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()







