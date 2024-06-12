import requests


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

        # Check for compatible versions
        compatible_version = None
        for version_info in versions_info['versions']:
            if version_info['version'].startswith(chrome_version.split('.')[0]):
                compatible_version = version_info
                break

        if compatible_version:
            for download_info in compatible_version['downloads']['chromedriver']:
                if download_info['platform'] == 'mac-arm64':
                    return download_info['url']

        # If no exact match or compatible version, find the closest match
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
