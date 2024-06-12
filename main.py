import requests
import re
import subprocess
import os
import zipfile
import shutil
from config import CHROME_WEB_DRIVER_PATH


def get_chrome_version():
    """ Get the current version of Chrome installed """
    try:
        process = subprocess.Popen(
            ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, _ = process.communicate()
        chrome_version = re.search(
            r'\d+\.\d+\.\d+\.\d+', stdout.decode('utf-8')).group(0)
        return chrome_version
    except Exception as e:
        raise Exception(f"Failed to get Chrome version: {e}")


def version_tuple(v):
    """ Convert version string to a tuple of integers for comparison """
    return tuple(map(int, (v.split("."))))


def get_closest_chromedriver_version(chrome_version, versions_info):
    """ Get the closest matching ChromeDriver version """
    chrome_version_parsed = version_tuple(chrome_version)
    closest_version = None
    smallest_diff = None

    for version_info in versions_info['versions']:
        curr_version = version_tuple(version_info['version'])
        diff = abs(
            sum(a - b for a, b in zip(chrome_version_parsed, curr_version)))
        if smallest_diff is None or diff < smallest_diff:
            smallest_diff = diff
            closest_version = version_info

    return closest_version


def get_chromedriver_download_url(chrome_version):
    """ Get the download URL for the corresponding ChromeDriver version """
    try:
        base_url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
        response = requests.get(base_url)
        response.raise_for_status()
        versions_info = response.json()

        # Check for exact match first
        for version_info in versions_info['versions']:
            if version_info['version'] == chrome_version:
                for download_info in version_info['downloads']['chromedriver']:
                    if download_info['platform'] == 'mac-arm64':
                        return download_info['url']

        # If no exact match, find the closest match
        closest_version_info = get_closest_chromedriver_version(
            chrome_version, versions_info)
        if closest_version_info:
            for download_info in closest_version_info['downloads']['chromedriver']:
                if download_info['platform'] == 'mac-arm64':
                    return download_info['url']

        raise Exception(
            f"No matching ChromeDriver version found for Chrome version {chrome_version}")
    except Exception as e:
        raise Exception(f"Could not fetch the ChromeDriver download URL: {e}")


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


def main():
    try:
        driver_path = CHROME_WEB_DRIVER_PATH
        if not driver_path:
            raise Exception(
                "Chrome Web Driver path not specified in the configuration file.")

        chrome_version = get_chrome_version()
        print(f"Chrome version: {chrome_version}")

        chromedriver_url = get_chromedriver_download_url(chrome_version)
        print(f"ChromeDriver download URL: {chromedriver_url}")

        zip_path = download_chromedriver(chromedriver_url)
        extract_and_replace(zip_path, driver_path)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
