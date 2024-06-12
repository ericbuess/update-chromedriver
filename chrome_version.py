import subprocess
import re
import platform
from config import CHROME_BINARY_PATH


def get_chrome_version():
    """ Get the current version of Chrome installed """
    try:
        system = platform.system()
        if system == 'Darwin':  # macOS
            command = [CHROME_BINARY_PATH['mac'], '--version']
        elif system == 'Linux':  # Linux
            command = [CHROME_BINARY_PATH['linux'], '--version']
        elif system == 'Windows':  # Windows
            command = [CHROME_BINARY_PATH['windows'], '--version']
        else:
            raise Exception(f"Unsupported operating system: {system}")

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, _ = process.communicate()
        chrome_version = re.search(
            r'\d+\.\d+\.\d+\.\d+', stdout.decode('utf-8')).group(0)
        return chrome_version
    except Exception as e:
        raise Exception(f"Failed to get Chrome version: {e}")
