import requests

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
        diff = abs(sum(a - b for a, b in zip(chrome_version_parsed, curr_version)))
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
        closest_version_info = get_closest_chromedriver_version(chrome_version, versions_info)
        if closest_version_info:
            for download_info in closest_version_info['downloads']['chromedriver']:
                if download_info['platform'] == 'mac-arm64':
                    return download_info['url']

        raise Exception(f"No matching ChromeDriver version found for Chrome version {chrome_version}")
    except Exception as e:
        raise Exception(f"Could not fetch the ChromeDriver download URL: {e}")
