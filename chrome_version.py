import subprocess
import re


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
