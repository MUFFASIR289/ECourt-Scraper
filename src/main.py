"""
Main entry point for eCourts Scraper
Provides command-line interface (CLI) for the scraper
"""
import argparse
import sys
import json
from typing import Optional

from scraper import ECourtsScraper
from utils import (
    setup_logger, 
    print_banner, 
    save_to_json, 
    generate_search_filename,
    get_date_string,
    validate_cnr,
    validate_case_details
)
from config import SUCCESS_MESSAGES, ERROR_MESSAGES

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="eCourts Case Scraper - Fetch court case information and listings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --cnr MHAU019999992015 --today
  python main.py --case-type CS --case-number 123 --year 2015 --tomorrow
  python main.py --causelist --today
  python main.py --causelist --tomorrow
  python main.py --cnr MHAU019999992015 --save
  python main.py --cnr MHAU019999992015 --no-headless
        """
    )
    search_group = parser.add_argument_group('Search Options')
    search_group.add_argument(
        '--cnr',
        type=str,
        help='Search by CNR number (16-character alphanumeric)'
    )
    search_group.add_argument(
        '--case-type',
        type=str,
        help='Case type (e.g., CS, CRL.A, W.P.(C))'
    )
    search_group.add_argument(
        '--case-number',
        type=str,
        help='Case number (numeric)'
    )
    search_group.add_argument(
        '--year',
        type=str,
        help='Case year (e.g., 2015)'
    )
    date_group = parser.add_argument_group('Date Options')
    date_group.add_argument(
        '--today',
        action='store_true',
        help='Check if case is listed today'
    )
    date_group.add_argument(
        '--tomorrow',
        action='store_true',
        help='Check if case is listed tomorrow'
    )
    causelist_group = parser.add_argument_group('Cause List Options')
    causelist_group.add_argument(
        '--causelist',
        action='store_true',
        help='Download complete cause list'
    )
    causelist_group.add_argument(
        '--date',
        type=str,
        help='Specific date for cause list (format: DD-MM-YYYY)'
    )
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument(
        '--save',
        action='store_true',
        help='Save results to JSON file'
    )
    output_group.add_argument(
        '--output',
        type=str,
        help='Custom output filename'
    )
    output_group.add_argument(
        '--download-pdf',
        action='store_true',
        help='Download case PDF (if available)'
    )
    browser_group = parser.add_argument_group('Browser Options')
    browser_group.add_argument(
        '--no-headless',
        action='store_true',
        help='Show browser window (useful for debugging)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='eCourts Scraper v1.0'
    )
    return parser

def validate_arguments(args) -> tuple[bool, Optional[str]]:
    has_cnr = args.cnr is not None
    has_case_details = all([args.case_type, args.case_number, args.year])
    has_causelist = args.causelist
    if not (has_cnr or has_case_details or has_causelist):
        return False, "Please provide either --cnr, case details (--case-type, --case-number, --year), or --causelist"
    if has_cnr and has_case_details:
        return False, "Please use either --cnr OR case details, not both"
    if has_cnr:
        is_valid, message = validate_cnr(args.cnr)
        if not is_valid:
            return False, f"Invalid CNR: {message}"
    if has_case_details:
        is_valid, message = validate_case_details(
            args.case_type,
            args.case_number,
            args.year
        )
        if not is_valid:
            return False, f"Invalid case details: {message}"
    if any([args.case_type, args.case_number, args.year]) and not has_case_details:
        return False, "When using case details, you must provide --case-type, --case-number, AND --year"
    return True, None

def print_search_result(result, args):
    print("\n" + "="*70)
    print("SEARCH RESULTS")
    print("="*70)
    if not result.success:
        print(f"\n❌ {result.message}")
        if result.error:
            print(f"   Error: {result.error}")
        return
    print(f"\n✅ {result.message}")
    if result.case_details:
        case = result.case_details
        print("\n📋 CASE DETAILS:")
        print("-" * 70)
        if case.cnr:
            print(f"  CNR Number:        {case.cnr}")
        if case.case_type:
            print(f"  Case Type:         {case.case_type}")
        if case.case_number:
            print(f"  Case Number:       {case.case_number}")
        if case.case_year:
            print(f"  Case Year:         {case.case_year}")
        if case.petitioner:
            print(f"\n  Petitioner:        {case.petitioner}")
        if case.respondent:
            print(f"  Respondent:        {case.respondent}")
        if case.court_name:
            print(f"\n  Court Name:        {case.court_name}")
        if case.court_number:
            print(f"  Court Number:      {case.court_number}")
        if case.judge_name:
            print(f"  Judge:             {case.judge_name}")
        if case.filing_date:
            print(f"\n  Filing Date:       {case.filing_date}")
        if case.registration_date:
            print(f"  Registration Date: {case.registration_date}")
        if case.status:
            print(f"  Status:            {case.status}")
        if case.next_hearing_date:
            print(f"  Next Hearing:      {case.next_hearing_date}")
    if args.today or args.tomorrow:
        print("\n📅 LISTING STATUS:")
        print("-" * 70)
        if result.is_listed and result.listing_info:
            listing = result.listing_info
            print(f"  ✓ Case IS LISTED")
            if listing.listing_date:
                print(f"  Date:              {listing.listing_date}")
            if listing.serial_number:
                print(f"  Serial Number:     {listing.serial_number}")
            if listing.court_name:
                print(f"  Court:             {listing.court_name}")
            if listing.court_number:
                print(f"  Court Number:      {listing.court_number}")
            if listing.judge_name:
                print(f"  Judge:             {listing.judge_name}")
            if listing.purpose:
                print(f"  Purpose:           {listing.purpose}")
        else:
            date_str = "today" if args.today else "tomorrow"
            print(f"  ✗ Case is NOT listed {date_str}")
    print("\n" + "="*70 + "\n")

def save_result(result, args):
    logger = setup_logger()
    filename = args.output if args.output else generate_search_filename(
        cnr=args.cnr,
        case_type=args.case_type,
        case_number=args.case_number,
        case_year=args.year
    )
    filepath = save_to_json(result.to_dict(), filename)
    logger.info(f"✓ Results saved to: {filepath}")
    print(f"\n💾 Results saved to: {filepath}")

def main():
    print_banner()
    parser = create_parser()
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    is_valid, error_message = validate_arguments(args)
    if not is_valid:
        print(f"\n❌ Error: {error_message}\n")
        parser.print_help()
        sys.exit(1)
    logger = setup_logger()
    headless = not args.no_headless
    try:
        logger.info("Starting eCourts Scraper...")
        scraper = ECourtsScraper(headless=headless)
        if args.causelist:
            date = args.date if args.date else None
            logger.info(f"Downloading cause list...")
            cause_list = scraper.download_cause_list(date)
            if cause_list:
                print(f"\n✅ Cause list downloaded successfully")
                # TODO: Display and save cause list
            else:
                print(f"\n❌ Failed to download cause list")
        elif args.cnr:
            check_listing = args.today or args.tomorrow
            result = scraper.search_by_cnr(args.cnr, check_listing=check_listing)
            print_search_result(result, args)
            if args.save:
                save_result(result, args)
        elif args.case_type and args.case_number and args.year:
            logger.info("Search by case details not yet implemented")
            print("\n⚠️  Search by case details is not yet implemented")
            print("Please use --cnr for now")
        scraper.close()
        logger.info("✓ Scraper closed successfully")
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        logger.info("Script interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
