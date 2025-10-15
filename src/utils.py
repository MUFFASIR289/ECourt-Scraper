"""
Utility functions for the eCourts scraper
Helper functions used throughout the project
"""
import os
import json
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging
from config import (
    ECOURTS_DATE_FORMAT, 
    INTERNAL_DATE_FORMAT, 
    DISPLAY_DATE_FORMAT,
    CNR_LENGTH,
    MIN_YEAR,
    MAX_YEAR,
    JSON_DIR
)

def setup_logger(name: str = "ecourts_scraper") -> logging.Logger:
    import colorlog
    logger = colorlog.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)-8s%(reset)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger

def validate_cnr(cnr: str) -> tuple[bool, str]:
    if not cnr:
        return False, "CNR cannot be empty"
    cnr = cnr.strip().replace(" ", "")
    if len(cnr) != CNR_LENGTH:
        return False, f"CNR must be exactly {CNR_LENGTH} characters long"
    if not cnr.isalnum():
        return False, "CNR must contain only letters and numbers"
    return True, "Valid CNR"

def validate_case_details(case_type: str, case_number: str, case_year: str) -> tuple[bool, str]:
    if not all([case_type, case_number, case_year]):
        return False, "All fields (case type, number, and year) are required"
    if not case_number.isdigit():
        return False, "Case number must be numeric"
    try:
        year = int(case_year)
        if year < MIN_YEAR or year > MAX_YEAR:
            return False, f"Year must be between {MIN_YEAR} and {MAX_YEAR}"
    except ValueError:
        return False, "Invalid year format"
    return True, "Valid case details"

def get_date_string(days_offset: int = 0, format_type: str = "internal") -> str:
    target_date = datetime.now() + timedelta(days=days_offset)
    if format_type == "internal":
        date_format = INTERNAL_DATE_FORMAT
    elif format_type == "ecourts":
        date_format = ECOURTS_DATE_FORMAT
    elif format_type == "display":
        date_format = DISPLAY_DATE_FORMAT
    else:
        date_format = INTERNAL_DATE_FORMAT
    return target_date.strftime(date_format)

def convert_date_format(date_str: str, from_format: str, to_format: str) -> Optional[str]:
    try:
        date_obj = datetime.strptime(date_str, from_format)
        return date_obj.strftime(to_format)
    except ValueError:
        return None

def save_to_json(data: Dict[Any, Any], filename: str, directory: Optional[str] = None) -> str:
    if directory is None:
        directory = JSON_DIR
    os.makedirs(directory, exist_ok=True)
    if not filename.endswith('.json'):
        filename += '.json'
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return filepath

def load_from_json(filename: str, directory: Optional[str] = None) -> Optional[Dict[Any, Any]]:
    if directory is None:
        directory = JSON_DIR
    if not filename.endswith('.json'):
        filename += '.json'
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def sanitize_filename(filename: str) -> str:
    invalid_chars = r'[<>:"/\\|?*]'
    filename = re.sub(invalid_chars, '_', filename)
    filename = filename.strip('. ')
    return filename

def generate_search_filename(cnr: Optional[str] = None, 
                            case_type: Optional[str] = None,
                            case_number: Optional[str] = None,
                            case_year: Optional[str] = None) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if cnr:
        base_name = f"search_CNR_{cnr}"
    elif case_type and case_number and case_year:
        base_name = f"search_{case_type}_{case_number}_{case_year}"
    else:
        base_name = "search_unknown"
    return sanitize_filename(f"{base_name}_{timestamp}")

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              eCourts Case Scraper v1.0                   ║
║         Fetch court case listings from eCourts           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)
