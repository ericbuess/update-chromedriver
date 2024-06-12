from config import CHROME_WEB_DRIVER_PATH
from chrome_version import get_chrome_version
from chromedriver_version import get_chromedriver_download_url
from chromedriver_download import download_chromedriver, extract_and_replace


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
