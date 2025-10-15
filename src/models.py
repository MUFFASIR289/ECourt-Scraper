"""
Data models for eCourts case information
These classes represent the structure of case data we'll scrape
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass
class CaseDetails:
    cnr: Optional[str] = None
    case_type: Optional[str] = None
    case_number: Optional[str] = None
    case_year: Optional[str] = None
    petitioner: Optional[str] = None
    respondent: Optional[str] = None
    court_name: Optional[str] = None
    court_number: Optional[str] = None
    judge_name: Optional[str] = None
    filing_date: Optional[str] = None
    registration_date: Optional[str] = None
    status: Optional[str] = None
    next_hearing_date: Optional[str] = None

    def to_dict(self):
        return {
            "cnr": self.cnr,
            "case_type": self.case_type,
            "case_number": self.case_number,
            "case_year": self.case_year,
            "petitioner": self.petitioner,
            "respondent": self.respondent,
            "court_name": self.court_name,
            "court_number": self.court_number,
            "judge_name": self.judge_name,
            "filing_date": self.filing_date,
            "registration_date": self.registration_date,
            "status": self.status,
            "next_hearing_date": self.next_hearing_date,
        }

@dataclass
class CaseListing:
    serial_number: Optional[int] = None
    listing_date: Optional[str] = None
    court_name: Optional[str] = None
    court_number: Optional[str] = None
    judge_name: Optional[str] = None
    case_details: Optional[CaseDetails] = None
    purpose: Optional[str] = None

    def to_dict(self):
        return {
            "serial_number": self.serial_number,
            "listing_date": self.listing_date,
            "court_name": self.court_name,
            "court_number": self.court_number,
            "judge_name": self.judge_name,
            "case_details": self.case_details.to_dict() if self.case_details else None,
            "purpose": self.purpose,
        }

@dataclass
class CauseList:
    date: str
    court_complex: Optional[str] = None
    total_cases: int = 0
    listings: List[CaseListing] = field(default_factory=list)

    def to_dict(self):
        return {
            "date": self.date,
            "court_complex": self.court_complex,
            "total_cases": self.total_cases,
            "listings": [listing.to_dict() for listing in self.listings]
        }
    def add_listing(self, listing: CaseListing):
        self.listings.append(listing)
        self.total_cases = len(self.listings)

@dataclass
class SearchResult:
    success: bool = False
    message: str = ""
    case_details: Optional[CaseDetails] = None
    is_listed: bool = False
    listing_info: Optional[CaseListing] = None
    error: Optional[str] = None
    search_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "case_details": self.case_details.to_dict() if self.case_details else None,
            "is_listed": self.is_listed,
            "listing_info": self.listing_info.to_dict() if self.listing_info else None,
            "error": self.error,
            "search_timestamp": self.search_timestamp,
        }
