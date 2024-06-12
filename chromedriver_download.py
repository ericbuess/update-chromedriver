import os
import requests
import zipfile
import shutil


def download_chromedriver(url):
    """ Download the ChromeDriver from the specified URL """
    try:
        zip_path = os.path.join(os.getcwd(), 'chromedriver.zip')
        response = requests.get(url, stream=True)
        with open(zip_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print(f"Downloaded ChromeDriver from: {url}")
        return zip_path
    except Exception as e:
        raise Exception(f"Failed to download ChromeDriver: {e}")


def extract_and_replace(zip_path, driver_path):
    """ Extract the downloaded zip file and replace the existing ChromeDriver """
    try:
        temp_extract_path = os.path.join(os.getcwd(), 'temp_chromedriver')
        os.makedirs(temp_extract_path, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_path)

        # Find the extracted chromedriver file
        for root, _, files in os.walk(temp_extract_path):
            if 'chromedriver' in files:
                extracted_driver_path = os.path.join(root, 'chromedriver')
                break
        else:
            raise Exception(
                f"Extracted ChromeDriver not found in {temp_extract_path}")

        if os.path.exists(driver_path):
            os.remove(driver_path)

        shutil.move(extracted_driver_path, driver_path)
        # Ensure the new driver has execute permissions
        os.chmod(driver_path, 0o755)
        shutil.rmtree(temp_extract_path)
        os.remove(zip_path)
        print(f"Extracted and replaced ChromeDriver at: {driver_path}")
    except Exception as e:
        raise Exception(f"Failed to extract and replace ChromeDriver: {e}")
