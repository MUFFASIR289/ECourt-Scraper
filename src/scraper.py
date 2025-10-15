"""
Core web scraping functionality for eCourts
This file contains the main ECourtsScraper class
"""
import time
import requests
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

from config import *
from models import CaseDetails, CaseListing, SearchResult, CauseList
from utils import setup_logger, get_date_string, validate_cnr

class ECourtsScraper:
    """
    Main scraper class for eCourts portal
    """
    def __init__(self, headless: bool = True):
        self.logger = setup_logger()
        self.logger.info("Initializing eCourts Scraper...")
        self.headless = headless
        self.driver = None
        self.session = requests.Session()
        self._setup_browser()
        self.logger.info("✓ Scraper initialized successfully")
    
    def _setup_browser(self):
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service

        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
        chrome_options.add_argument(f"user-agent={USER_AGENT}")

        if DISABLE_IMAGES:
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)

        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(IMPLICIT_WAIT)
            self.logger.info("✓ Browser initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize browser: {e}")
            raise
    
    def search_by_cnr(self, cnr: str, check_listing: bool = True) -> SearchResult:
        self.logger.info(f"Searching for case with CNR: {cnr}")
        is_valid, message = validate_cnr(cnr)
        if not is_valid:
            self.logger.error(f"Invalid CNR: {message}")
            return SearchResult(
                success=False,
                message=message,
                error="Invalid CNR"
            )
        try:
            self.driver.get(CASE_STATUS_URL)
            self.logger.info("✓ Loaded case status page")
            time.sleep(2)
            try:
                cnr_radio = self.driver.find_element(By.ID, "radCNR")
                cnr_radio.click()
                self.logger.info("✓ Selected CNR search option")
                time.sleep(1)
                cnr_input = self.driver.find_element(By.ID, "cnr_number")
                cnr_input.clear()
                cnr_input.send_keys(cnr)
                self.logger.info("✓ Entered CNR number")

                self.logger.warning("⚠ CAPTCHA detected - Manual intervention required")
                self.logger.info("Please solve the CAPTCHA in the browser window...")
                self.logger.info("The script will continue after you submit the form")
                input("Press Enter after you've solved the CAPTCHA and clicked 'Go'...")

                WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                    EC.presence_of_element_located((By.TAG_NAME, "table"))
                )
                self.logger.info("✓ Results page loaded")
                case_details = self._parse_case_details()
                if case_details:
                    self.logger.info("✓ Case found successfully")
                    listing_info = None
                    is_listed = False
                    if check_listing:
                        self.logger.info("Checking case listing status...")
                        is_listed, listing_info = self._check_case_listing(case_details)
                    return SearchResult(
                        success=True,
                        message="Case found successfully",
                        case_details=case_details,
                        is_listed=is_listed,
                        listing_info=listing_info
                    )
                else:
                    return SearchResult(
                        success=False,
                        message="Case not found",
                        error="No case data found for this CNR"
                    )
            except NoSuchElementException as e:
                self.logger.error(f"Element not found: {e}")
                return SearchResult(
                    success=False,
                    message="Failed to locate search elements",
                    error=str(e)
                )   
        except TimeoutException:
            self.logger.error("Request timed out")
            return SearchResult(
                success=False,
                message="Request timed out",
                error="The server took too long to respond"
            )
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return SearchResult(
                success=False,
                message="An unexpected error occurred",
                error=str(e)
            )
    
    def _parse_case_details(self) -> Optional[CaseDetails]:
        try:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            case = CaseDetails()
            tables = soup.find_all('table')
            if not tables:
                self.logger.warning("No tables found on page")
                return None
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        label = cells[0].get_text(strip=True).lower()
                        value = cells[1].get_text(strip=True)
                        if 'case' in label and 'number' in label:
                            case.case_number = value
                        elif 'case' in label and 'type' in label:
                            case.case_type = value
                        elif 'year' in label:
                            case.case_year = value
                        elif 'petitioner' in label or 'plaintiff' in label:
                            case.petitioner = value
                        elif 'respondent' in label or 'defendant' in label:
                            case.respondent = value
                        elif 'court' in label and 'name' in label:
                            case.court_name = value
                        elif 'filing' in label and 'date' in label:
                            case.filing_date = value
                        elif 'registration' in label and 'date' in label:
                            case.registration_date = value
                        elif 'status' in label:
                            case.status = value
                        elif 'judge' in label:
                            case.judge_name = value
                        elif 'next' in label and ('hearing' in label or 'date' in label):
                            case.next_hearing_date = value
            return case if case.case_number else None
        except Exception as e:
            self.logger.error(f"Error parsing case details: {e}")
            return None

    def _check_case_listing(self, case_details: CaseDetails) -> tuple[bool, Optional[CaseListing]]:
        try:
            today = get_date_string(0, "ecourts")
            listing = self._check_cause_list_for_date(today, case_details)
            if listing:
                self.logger.info(f"✓ Case is listed TODAY")
                return True, listing
            tomorrow = get_date_string(1, "ecourts")
            listing = self._check_cause_list_for_date(tomorrow, case_details)
            if listing:
                self.logger.info(f"✓ Case is listed TOMORROW")
                return True, listing
            self.logger.info("Case is not listed today or tomorrow")
            return False, None
        except Exception as e:
            self.logger.error(f"Error checking case listing: {e}")
            return False, None

    def _check_cause_list_for_date(self, date: str, case_details: CaseDetails) -> Optional[CaseListing]:
        self.logger.warning("Cause list checking not fully implemented - requires manual adaptation")
        return None

    def download_cause_list(self, date: Optional[str] = None) -> Optional[CauseList]:
        if date is None:
            date = get_date_string(0, "ecourts")
        self.logger.info(f"Downloading cause list for {date}")
        try:
            self.driver.get(CAUSE_LIST_URL)
            time.sleep(2)
            self.logger.warning("Cause list download not fully implemented")
            return None
        except Exception as e:
            self.logger.error(f"Error downloading cause list: {e}")
            return None

    def close(self):
        if self.driver:
            self.driver.quit()
            self.logger.info("✓ Browser closed")
        
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
