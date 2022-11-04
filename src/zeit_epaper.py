from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

class ZeitIssue():
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def download_file(self) -> str:
        link_elem = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.LINK_TEXT, 'EPUB FÜR E-READER LADEN')))

        file_name = link_elem.get_attribute('href').split('/')[-1]
        link_elem.click()
        return file_name


class ZeitEPaper():
    LOGIN_URL = 'https://epaper.zeit.de/abo/diezeit/'

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def get_current_issue(self, username: str, password: str) -> ZeitIssue :
        self.driver.get(self.LOGIN_URL)

        self.driver.find_element(By.NAME, 'email').send_keys(username)
        self.driver.find_element(By.NAME, 'pass').send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, 'input[type=\'submit\']').click()

        self.driver.find_element(By.LINK_TEXT, 'ZUR AKTUELLEN AUSGABE').click()
        return ZeitIssue(self.driver)
