from math import e
import os
from time import sleep
import scraping.selenium_setup as Scraper
import file_managment.file_operations as FileManager
import file_managment.path_config as PathConfig
from services.data_processor import merge_gene_and_clinical_data
from services.minio_service import list_files_in_bucket
from services.mongo_service import check_data_exists, insert_data_to_mongo, fetch_data_from_mongo
from data_visualizer import visualize_data

BUCKET_NAME = "antonela-aabicic-p2"
COMBINED_FILE_NAME = "combined_gene_clinical_data.tsv"
CLINICAL_FILE_NAME = "TCGA_clinical_survival_data.tsv"

def process_and_visualize_data():
    insert_data_to_mongo(BUCKET_NAME, COMBINED_FILE_NAME)
    data = fetch_data_from_mongo()
    visualize_data(data)

def main():
    driver = None
    try:
        if check_data_exists():
            print("Data already exists in MongoDB. Fetching data and visualizing.")
            data = fetch_data_from_mongo()
            visualize_data(data)
            return

        files_in_minio = list_files_in_bucket(BUCKET_NAME)
        if COMBINED_FILE_NAME in files_in_minio:
            print(f"Combined file '{COMBINED_FILE_NAME}' already exists in Minio.")
            process_and_visualize_data()
            return
        
        if len(files_in_minio) < 37:
            driver_path, gz_folder, unzipped_folder = PathConfig.setup_paths()
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
                FileManager.process_gz_files(gz_folder, unzipped_folder)
        else:
            print("All 37 files are already present in MinIO. Skipping download.")

        merge_gene_and_clinical_data(CLINICAL_FILE_NAME, BUCKET_NAME)
        process_and_visualize_data()

    except Exception as e:
        raise Exception(f"Error: {e}")
    finally:
        if driver is not None:
            driver.quit()

if __name__ == "__main__":
    main()







