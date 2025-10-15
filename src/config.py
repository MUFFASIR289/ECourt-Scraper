"""
Configuration file for eCourts Scraper
Contains all constants and settings used throughout the project
"""

# ===========================
# URL CONFIGURATIONS
# ===========================
BASE_URL = "https://services.ecourts.gov.in/ecourtindia_v6/"
CASE_STATUS_URL = BASE_URL + "?p=casestatus/index"
CAUSE_LIST_URL = BASE_URL + "?p=cause_list/index"
COURT_ORDERS_URL = BASE_URL + "?p=courtorder/index"

# ===========================
# SCRAPING SETTINGS
# ===========================
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15
REQUEST_TIMEOUT = 30
REQUEST_DELAY = 2
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# ===========================
# FILE PATHS
# ===========================
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
JSON_DIR = os.path.join(DATA_DIR, "json")
PDF_DIR = os.path.join(DATA_DIR, "pdf")
LOG_DIR = os.path.join(DATA_DIR, "logs")

for directory in [DATA_DIR, JSON_DIR, PDF_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

# ===========================
# SEARCH TYPES
# ===========================
SEARCH_BY_CNR = "cnr"
SEARCH_BY_CASE_NUMBER = "case_number"
SEARCH_BY_PARTY_NAME = "party_name"
SEARCH_BY_FIR = "fir"

# ===========================
# DATE FORMATS
# ===========================
ECOURTS_DATE_FORMAT = "%d-%m-%Y"
INTERNAL_DATE_FORMAT = "%Y-%m-%d"
DISPLAY_DATE_FORMAT = "%d %B %Y"

# ===========================
# LOGGING SETTINGS
# ===========================
LOG_FORMAT = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s%(reset)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = os.path.join(LOG_DIR, "ecourts_scraper.log")

# ===========================
# OUTPUT SETTINGS
# ===========================
DEFAULT_OUTPUT_FORMAT = "json"
JSON_INDENT = 4

# ===========================
# BROWSER SETTINGS
# ===========================
HEADLESS_MODE = True
WINDOW_SIZE = "1920,1080"
DISABLE_IMAGES = True

# ===========================
# ERROR MESSAGES
# ===========================
ERROR_MESSAGES = {
    "no_connection": "Unable to connect to eCourts portal. Check your internet connection.",
    "invalid_cnr": "Invalid CNR number. CNR must be 16 characters.",
    "case_not_found": "Case not found. Please verify the case details.",
    "no_listing": "This case is not listed today or tomorrow.",
    "captcha_required": "CAPTCHA verification required. Please solve manually.",
    "timeout": "Request timed out. The server took too long to respond.",
}

SUCCESS_MESSAGES = {
    "case_found": "Case found successfully!",
    "listing_found": "Case is listed!",
    "pdf_downloaded": "PDF downloaded successfully.",
    "data_saved": "Data saved successfully.",
}

CNR_LENGTH = 16
VALID_CASE_TYPES = [
    "CS", "CRL.A", "CRL.M.C", "CRL.R", "CRL.L.P", "FAO", "W.P.(C)",
    "W.P.(CRL)", "ARB.P", "CS(COMM)", "CS(OS)", "EX.APP", "C.M.A",
    "MAC.APP", "RFA", "RSA", "CRLA", "CRLP", "CRLMC"
]

MIN_YEAR = 1950
MAX_YEAR = 2026
