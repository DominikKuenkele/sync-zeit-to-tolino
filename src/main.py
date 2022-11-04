import os
import time
import logging
import zipfile

from lxml import etree

from src.webdriver import get_webdriver, DOWNLOAD_PATH
from src.zeit_epaper import ZeitEPaper
from src.thalia_library import ThaliaLogin


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class MissingEnvironmentVariable(Exception):
    pass

def is_file_downloaded(file_path: str, timeout=60) -> bool:
    end_time = time.time() + timeout
    while not os.path.exists(file_path):
        time.sleep(1)
        if time.time() > end_time:
            return False

    if os.path.exists(file_path):
        return True

def get_e_paper_title(epaper_file: str) -> str:
    def xpath(element: etree._Element, path: str) -> etree._Element | etree._ElementUnicodeResult:
        return element.xpath(
            path,
            namespaces={
                "n": "urn:oasis:names:tc:opendocument:xmlns:container",
                "pkg": "http://www.idpf.org/2007/opf",
                "dc": "http://purl.org/dc/elements/1.1/",
            },
        )[0] 

    # prepare to read from the .epub file
    zip_content = zipfile.ZipFile(epaper_file)

    # find the contents metafile
    cfname = xpath(
        etree.fromstring(zip_content.read("META-INF/container.xml")),
        "n:rootfiles/n:rootfile/@full-path",
    )

    # grab the metadata block from the contents metafile
    metadata = xpath(etree.fromstring(zip_content.read(cfname)), "/pkg:package/pkg:metadata")

    # repackage the data
    return xpath(metadata, f"dc:title/text()")


if __name__ == '__main__':
    try:
        log.info('Reading environment variables...')
        zeit_user = os.environ['ZEIT_USER']
        zeit_password = os.environ['ZEIT_PASSWORD']
        thalia_user = os.environ['THALIA_USER']
        thalia_password = os.environ['THALIA_PASSWORD']
    except KeyError as e:
        log.error(f'Failed reading the environment variable {e.args[0]}')
        raise MissingEnvironmentVariable(f'The environment variable \'{e.args[0]}\' is missing. Ensure to export it.') from None

    try:
        webdriver = get_webdriver(headless=True)
        
        log.info('logging into ZEIT...')
        zeit_epaper = ZeitEPaper(webdriver).get_current_issue(zeit_user, zeit_password)
        log.info('downloading current ZEIT e-paper issue...')
        file_name = zeit_epaper.download_file()
        

        file_path = os.path.join(DOWNLOAD_PATH, file_name)
        if is_file_downloaded(file_path):
            e_paper_title = get_e_paper_title(file_path)

            log.info('logging into Tolino Webreader with Thalia...')
            thalia_library = ThaliaLogin(webdriver).get_library(thalia_user, thalia_password)
            log.info('uploading ZEIT e-paper to tolino cloud...')
            thalia_library.upload(file_path, e_paper_title)
            log.info('done.')
        else:
            log.error('download of current ZEIT e-paper issue failed.')
    except:
        log.error('Failed.', exc_info=True)
    finally:
        webdriver.quit()

