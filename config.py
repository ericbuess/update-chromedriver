import platform

system = platform.system()

# Specify the path where you want to store the ChromeDriver
CHROME_WEB_DRIVER_PATH = "/usr/local/bin/chromedriver" if system != 'Windows' else "C:\\path\\to\\chromedriver.exe"

# Specify the path to the Chrome binary for each operating system
CHROME_BINARY_PATH = {
    'mac': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    'linux': '/usr/bin/google-chrome',
    'windows': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
}
