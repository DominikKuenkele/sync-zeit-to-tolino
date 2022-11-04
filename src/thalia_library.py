import time
import logging

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

log = logging.getLogger(__name__)


class SynchronizationError(Exception):
    pass


class ThaliaLibrary():
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

        # close popup if appearing
        if len(self.driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id=\'undefined-popup-container\']')) > 0:
            time.sleep(1)
            ok_button = self.driver.find_element(
                By.CSS_SELECTOR, 'div[data-test-id=\'dialogButton-0\']')
            driver.execute_script('arguments[0].scrollIntoView();', ok_button)
            ok_button.click()

        # navigate to 'my books'
        self.driver.find_element(
            By.CSS_SELECTOR, 'span[data-test-id=\'library-drawer-MyBooks\']').click()
        time.sleep(1)

    def upload(self, file_path: str, e_paper_title: str) -> None:
        if e_paper_title not in self.driver.page_source:
            upload = self.driver.find_element(
                By.CSS_SELECTOR, 'input[type=\'file\']')
            log.info('starting upload...')
            upload.send_keys(file_path)

            log.info('waiting until upload done...')
            upload_status_bar = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "_ymr9b9")))
            WebDriverWait(self.driver, 200).until(
                expected_conditions.staleness_of(upload_status_bar))

            self.driver.refresh()
            log.info('waiting for e-book to be present...')
            WebDriverWait(self.driver, 10).until(
                expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'span[data-test-id="library-myBooks-titles-list-0-title"]'))
            )

            if e_paper_title not in self.driver.page_source:
                message = f'Title \'{e_paper_title}\' not found in page source'
                log.error(message)
                raise SynchronizationError(message)

            log.info('upload done.')
        else:
            log.info(
                f'e-paper \'{e_paper_title}\' already present. Skipping upload.')


class ThaliaLogin():
    LOGIN_URL = 'https://www.thalia.de/auth/oauth2/authorize?client_id=webreader&response_type=code&scope=SCOPE_BOSH&redirect_uri=https%3A%2F%2Fwebreader.mytolino.com%2Flibrary%2Findex.html%23%2Fmybooks%2Ftitles&x_buchde.skin_id=17&x_buchde.mandant_id=2'

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def get_library(self, username: str, password: str) -> ThaliaLibrary:
        self.driver.get(self.LOGIN_URL)

        self.driver.find_element(By.ID, 'j_username').send_keys(username)
        self.driver.find_element(By.ID, 'j_password').send_keys(password)
        self.driver.find_element(By.NAME, 'login').click()

        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[data-test-id=\'ftu-country-de-DE\']'))).click()
        self.driver.find_element(
            By.CSS_SELECTOR, 'div[data-test-id=\'ftu-resellerLogo-3\']').click()
        self.driver.find_element(
            By.CSS_SELECTOR, 'div[data-test-id=\'library-drawer-buttonLogin\']').click()

        return ThaliaLibrary(self.driver)
