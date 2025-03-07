import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

# Set the root download directory for LEGAL FRAMEWORK
download_dir = '/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/LEGAL FRAMEWORK/'

chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    "download.prompt_for_download": False,  # Turn off download prompt
    "download.directory_upgrade": True,  # Allow directory upgrade
    "plugins.always_open_pdf_externally": True,  # Open PDFs externally, not in-browser
})

# Set up the WebDriver
driver = webdriver.Chrome(options=chrome_options)

def create_folder(folder_name):
    """Create a folder for saving PDFs if it doesn't exist."""
    folder_path = os.path.join(download_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def set_download_directory(folder_path):
    """Dynamically set the Chrome download directory using Chrome DevTools Protocol (CDP)."""
    driver.execute_cdp_cmd("Page.setDownloadBehavior", {
        "behavior": "allow",
        "downloadPath": folder_path
    })

def download_pdfs(base_url, folder_name, total_pages):
    """Download all PDFs for a specific section and save them in a folder."""
    folder_path = create_folder(folder_name)  # Create the folder
    set_download_directory(folder_path)  # Set the dynamic download path
    driver.set_script_timeout(60)
    page = 1
    while page <= total_pages:
        page_url = f"{base_url}?page={page}"
        driver.get(page_url)
        print(f"Accessing {page_url}")

        # Wait for elements to load
        time.sleep(3)

        # Find all PDF download links
        links = driver.find_elements(By.XPATH, "//a[contains(@onclick, 'newwindow')]")
        if not links:
            break  # Exit if no more PDFs are found

        for link in links:
            try:
                # Execute the JavaScript function to open the new window with the PDF
                pdf_js = link.get_attribute('onclick')
                driver.execute_script(pdf_js)
                print(f"Downloading PDF for {folder_name}...")
                time.sleep(2)  # Wait to ensure the download starts
            except Exception as e:
                print(f"Error downloading PDF: {e}")
                continue  # Skip any failed download

        page += 1

    print(f"Finished downloading PDFs for {folder_name}.")

def process_all_legal_framework():
    """Process all dropdown options dynamically."""
    categories = {
        "ACT": "https://ibbi.gov.in/legal-framework/act",
        "RULES": "https://ibbi.gov.in/legal-framework/rules",
        "REGULATIONS": "https://ibbi.gov.in//legal-framework/updated",
        "CIRCULARS": "https://ibbi.gov.in/legal-framework/circulars",
        "NOTIFICATIONS": "https://ibbi.gov.in/legal-framework/notifications",
        "FACILITATION": "https://ibbi.gov.in/legal-framework/facilitation",
        "GUIDELINES": "https://ibbi.gov.in/legal-framework/guidelines",
        "BY OTHER AUTHORITIES": "https://ibbi.gov.in//legal-framework/other-authorities"
    }

    
    pages_per_category = {
        "ACT": 4,
        "RULES": 4,
        "REGULATIONS": 11,
        "CIRCULARS": 9,
        "NOTIFICATIONS": 8,
        "FACILITATION": 10,
        "GUIDELINES": 5,
        "BY OTHER AUTHORITIES": 5,
    }

    for category, url in categories.items():
        print(f"Processing: {category}")
        total_pages = pages_per_category.get(category, 1)  # Default to 1 page if not specified
        download_pdfs(url, category, total_pages)

try:
    process_all_legal_framework()
finally:
    driver.quit()
    print("Closed the browser.")
