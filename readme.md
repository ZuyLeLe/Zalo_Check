# Zalo Phone Number Checker
This application uses the **ZaloAPI** to check whether phone numbers are registered on Zalo, based on user-provided login credentials. The application features a graphical user interface (GUI) built with **Tkinter**, allowing users to input login information, select a file containing phone numbers, and export the results.
## Features
- **ZaloAPI Integration**: Login using Zalo credentials (cookies, IMEI, phone, password).
- **File Processing**: Check multiple phone numbers for Zalo registration via a CSV or Excel file.
- **Progress Tracking**: Real-time progress updates displayed in the GUI during file processing.
- **Auto-fill Login Details**: Saves IMEI and cookies for easy future logins.
- **Error Handling & Retry Logic**: Handles rate limits and retries failed requests with exponential backoff.
- **Pre-built Executable**: No need to install Python—just download and run the `.exe`.
> [!WARNING]  
> This is a log in session based API so it will require your Zalo account number and password.
## Download & Installation
### Option 1: Download the Pre-built `.exe` (Recommended)
1. Download the latest release of the **Zalo Phone Number Checker** from the [Releases](https://github.com/yourusername/zalo-checker/releases) page.
2. Run the `.exe` directly—no installation required.
3. Follow the usage steps below.
### Option 2: Run from Source
If you prefer to run the project from the source code, follow these steps:
1. Clone the repository:
     ```bash
     git clone https://github.com/yourusername/zalo-checker.git
     cd zalo-checker
2. Install required libraries:
    ```bash
    pip install -r requirements.txt   
3. Run the application:
    ```bash
    python main.py
## How to get IMEI and Cookies?
### Download Extension
- [Click Here](https://drive.google.com/file/d/18_-8ruYOVa89JkHdr3muGj3kGWxwt6mc/view?usp=drive_link) to download the extension support getting IMEI & Cookies more conveniently.
### Extension Usage Tutorial
1. Enable the extension downloaded above.
2. Go to [https://chat.zalo.me](https://chat.zalo.me), Sign in to your account.
3. After successfully logging in, go back to extension and get IMEI, Cookies.
> [!TIP]
If you have opened the website ``chat.zalo.me`` but the extension does not have IMEI & Cookies, please click ``Refresh Page``.
## Usage
  1. Login:
      * Enter your Zalo session cookies (in JSON format) and IMEI. If saved from a previous session, they will be auto-filled as long as you are still log in the browser.
      * If you have log out then there will be a new cookies to you need to get the new IMEI, Cookies again.
      * Proceed to the next screen by clicking "Next".
  2. Phone Number Check:
      * Enter your Zalo account phone number and password.
      * The app will attempt to log in and proceed to file selection upon success.
  3. File Selection and Processing:
      * Upload a CSV or Excel file that contains a column titled Phone.
      * The app will check the Zalo registration status of each phone number and save the results in a new file (CSV or Excel).
      * During processing, a real-time log of each phone check will appear in the progress box.
## File Format
The input file should be in CSV or Excel format and must contain a column named ``Phone``. Example:
| Phone            |
|------------------|
| 0987654321       |
| 0123456789       |
| 0901234567       |

The output file will add a column called IsZalo, indicating the Zalo registration status:

|Phone	|IsZalo|
|--------|-------|
|0987654321	|User name |
|0123456789|	Unknown|
|1|Not a phone number|
## Error Handling
  * If any phone number cannot be checked, the app will retry the request up to 5 times with an exponential backoff. Failed numbers will be marked as 'Timeout' or 'Error'.
  * Any invalid login details or file issues will be shown in an error dialog.
    
## Credits
This project utilizes the [ZaloAPI](https://github.com/Its-VrxxDev/zlapi) developed by [Its-VrxxDev](https://github.com/Its-VrxxDev). 
Special thanks to the original author for providing the ZaloAPI used in this project.
## Contributing
Feel free to fork this repository and submit pull requests. Please ensure that code is properly formatted and follows Pythonic conventions (e.g., PEP 8).
## License
This project is licensed under the MIT License - see the LICENSE file for details.