<p align="center">
    This project is a GUI-based application designed for visualizing gene expression data for oncology patients. 
</p>

## 📌 About The Project

This Python application automates the retrieval, storage, and analysis of gene expression data from [Xena Browser](https://xenabrowser.net/datapages/?hub=https://tcga.xenahubs.net:443). 

The application downloads compressed .gz files containing gene expression data, extracts them to obtain TSV files, and processes them using Pandas. The extracted data is stored in MinIO, ensuring 
efficient unstructured cloud storage. Once processed, the gene expression data is merged with TCGA_clinical_survival_data.tsv that was already stored in Minio to create a comprehensive dataset.

The final dataset is then stored in MongoDB, enabling efficient querying. The results are visualized through a Tkinter-based GUI.

## 🚀 Features  
- **Automated Download & Extraction**: Fetches `.gz` files from [Xena Browser](https://xenabrowser.net/datapages/?hub=https://tcga.xenahubs.net:443) and extracts **TSV** files  
- **Data Cleaning & Transformation**: Uses **Pandas** for structured processing  
- **Secure Cloud Storage**: Stores processed files in **MinIO** for scalable object storage
- **Integrated Data Storage**: Saves processed gene expression data in **MongoDB** for efficient querying
- **GUI-Based Visualization**: Displays results interactively using **Tkinter**

## 🛠 Built With

### Languages & Frameworks
![Python](https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white) 

### Storage
![MinIO](https://img.shields.io/badge/MinIO-FF0000?style=for-the-badge&logo=minio&logoColor=white)
![MongoDB](https://img.shields.io/badge/mongodb-%2347A248.svg?style=for-the-badge&logo=mongodb&logoColor=white)


