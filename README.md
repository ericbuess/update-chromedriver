# ChromeDriver Updater

This project automatically updates the ChromeDriver to match the installed Chrome browser version. It downloads the appropriate ChromeDriver version, extracts it, and places it in the specified path. This is useful for tools like Selenium that require a ChromeDriver version compatible with the version of Chrome installed on your system which can change when you update your Chrome browser.

## Features

- Automatically detects the installed Chrome version.
- Downloads the closest matching ChromeDriver version.
- Extracts the ChromeDriver and replaces the old one.
- Handles permissions and cleanup of temporary files.

## Setup Examples

### Using Python Virtual Environment

1. **Create a virtual environment:**

   ```sh
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

### Using Conda

1. **Create a Conda environment:**

   ```sh
   conda create --name updatechrome python=3.23
   ```

2. **Activate the Conda environment:**

   ```sh
   conda activate updatechrome
   ```

### Install Dependencies

1. **Install the required packages:**

   ```sh
   pip install requests packaging
   ```

## Configuration

Update the `config.py` file with the path where you want to store the ChromeDriver. Here are some default examples:

```python
# config.py
# Specify the path where you store the ChromeDriver
# Examples:
# Windows: "C:\\path\\to\\chromedriver"
# macOS/Linux: "/usr/local/bin/chromedriver"
CHROME_WEB_DRIVER_PATH = "/your/path/to/chromedriver"
```

## Usage

1. **Run the script:**

   ```sh
   python main.py
   ```

2. **If you encounter permission issues (e.g., when writing to protected directories), run the script with `sudo` on macOS/Linux:**

   ```sh
   sudo python main.py
   ```

**Note:** Make sure to update `config.py` with the correct path to your ChromeDriver.

## What This Project Does

This project detects the installed Chrome version, downloads the corresponding ChromeDriver version, extracts it, and replaces the existing ChromeDriver. It also ensures proper permissions and cleans up temporary files.

## Troubleshooting

- **Permission Issues:**

  - On macOS/Linux, you might need to run the script with `sudo` if you encounter permission issues when writing to protected directories.

- **Missing Dependencies:**

  - Ensure all dependencies are installed by running:
    ```sh
    pip install -r requirements.txt
    ```

- **Chrome Version Detection:**
  - If the script fails to detect the Chrome version, ensure Chrome is installed in the default path or update the script to point to the correct Chrome executable.

## Contributing

Contributions are welcome! Please submit a pull request with detailed descriptions of your changes.

## License

This project is licensed under The Unlicense. See the [LICENSE](LICENSE) file for details.
