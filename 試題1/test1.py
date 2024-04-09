from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import time
import ddddocr
from PIL import Image
import io
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging

class AddressFetcher:

    def __init__(self,url) -> None:
        self.logger = self.setup_logger()
        self.chrome_options = Options()
        service = Service(executable_path=ChromeDriverManager().install())
        self.chrome_options.add_argument("--headless")  
        self.chrome_options.add_argument("--disable-gpu") 
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(service=service, options=self.chrome_options)
        self.ocr = ddddocr.DdddOcr()
        self.url = url
        
    
    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger
    
    def open_website(self):
        self.browser.get(self.url)

    def select_location_and_date(self):
        # Click the button
        element = self.browser.find_element(By.XPATH,"/html/body/div[1]/div[4]/div/div/form/div[1]/fieldset/div/div[1]/button")
        element.click()
        time.sleep(1)
        # Click on the map for Taoyuan
        area_element = self.browser.find_element(By.XPATH,'//*[@id="mapForm"]/div/fieldset/div[3]/map/area[2]')
        area_element.click()
        time.sleep(1)
        # Select Taoyuan city
        areacode_dropdown = self.browser.find_element(By.XPATH,'//*[@id="areaCode"]')
        areacode_select = Select(areacode_dropdown)
        areacode_select.select_by_value("68000010")
        time.sleep(1)
        # Set start date (民國年)
        self.browser.execute_script("document.getElementById('sDate').removeAttribute('readonly')")
        date_input = self.browser.find_element(By.ID,'sDate')
        date_input.clear()  
        date_input.send_keys("111-01-01")#因為固定從這時間開始，如果要特別計算的話再改
        time.sleep(1)
        # Set end date (民國年)
        now_date = datetime.now()
        self.browser.execute_script("document.getElementById('eDate').removeAttribute('readonly')")
        date_input = self.browser.find_element(By.ID,'eDate')
        date_input.clear()  
        date_input.send_keys(f"{now_date.year-1911}-{now_date.month:02d}-{now_date.day:02d}")

    def fetch_addresses(self):
        while True:
            # If no captcha error popup appears, continue with captcha recognition and input
            captcha_image = self.browser.find_element(By.XPATH,'//*[@id="captchaImage_captchaKey"]')
            captcha_image_binary = captcha_image.screenshot_as_png
            image = Image.open(io.BytesIO(captcha_image_binary))
            result = self.ocr.classification(image)
            self.logger.info(f"current catcha : {result}")
            time.sleep(2)
            # Input captcha
            captcha_input = self.browser.find_element(By.XPATH,'//*[@id="captchaInput_captchaKey"]')
            captcha_input.clear()  
            captcha_input.send_keys(result)
            time.sleep(2)
            # Click search
            search_button = self.browser.find_element(By.XPATH,'//*[@id="goSearch"]')
            search_button.click()
            time.sleep(3)
            try:
                #有跳出錯誤框的話代表驗證碼錯誤，要點擊"確定"按鈕，並且重試
                error_captcha_button = self.browser.find_element(By.CSS_SELECTOR,"body > div.swal2-container.swal2-center.swal2-fade.swal2-shown > div > div.swal2-actions > button.swal2-confirm.swal2-styled")
                self.logger.info("Captcha error, clicking 'Confirm' button, retrying...")
                error_captcha_button.click()
                continue
            except NoSuchElementException:
                self.logger.info("Captcha succeeded.")
                break

    def fetch_addresses_from_all_pages(self):
        while True:
            try:
                time.sleep(1)
                next_page_button = self.browser.find_element(By.XPATH,'//*[@id="next_result-pager"]/span')
                page_source = self.browser.page_source
                self.logger.info("Start writing CSV file")
                self.process_table(page=page_source,csv_name="address.csv")
                self.logger.info("End writing CSV file")
                next_page_button.click()
            except ElementClickInterceptedException:
                self.logger.info("Reached the last page.")
                break

    def process_table(self,page,csv_name):

        tables = pd.read_html(page)
        df = tables[1][1:]
        df[0] = df[0].astype(int)
        self.logger.info("current data: \n",df)
        df.to_csv(csv_name, mode='a', header=False, index=False)

    def close_browser(self):
        self.browser.quit()

if __name__ == "__main__":
    target_url = "https://www.ris.gov.tw/info-doorplate/app/doorplate/main?retrievalPath=%2Fdoorplate%2F"
    fetcher = AddressFetcher(target_url)
    fetcher.open_website()
    fetcher.select_location_and_date()
    fetcher.fetch_addresses()
    fetcher.fetch_addresses_from_all_pages()
    fetcher.close_browser()
         
        
        