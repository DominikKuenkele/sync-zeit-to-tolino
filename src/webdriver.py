import tempfile

from selenium.webdriver import Chrome, ChromeOptions


DOWNLOAD_PATH = tempfile.gettempdir()
# maybe updated, when headless driver denied by Thalia
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) '\
             'AppleWebKit/537.36 (KHTML, like Gecko) '\
             'Chrome/107.0.0.0 '\
             'Safari/537.36'


def get_webdriver(headless=True) -> Chrome:
    prefs = {}
    prefs["download.default_directory"] = DOWNLOAD_PATH

    chrome_options = ChromeOptions()
    chrome_options.add_argument('--window-size=1920,1080')
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument(f'user-agent={USER_AGENT}')
    chrome_options.add_experimental_option("prefs", prefs)

    driver = Chrome(options=chrome_options)
    driver.implicitly_wait(5)

    return driver
