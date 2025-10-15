"""
Example usage scripts for eCourts Scraper
Demonstrates how to use the scraper in Python code
"""
import sys
sys.path.append('../src')  # Add src to path

from scraper import ECourtsScraper
from utils import save_to_json, print_banner

def example_1_basic_search():
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic CNR Search")
    print("="*70 + "\n")
    with ECourtsScraper(headless=False) as scraper:
        cnr = "MHAU019999992015"  # Replace with actual CNR
        result = scraper.search_by_cnr(cnr, check_listing=False)
        if result.success:
            print("✅ Case found!")
            print(f"Case Number: {result.case_details.case_number}")
            print(f"Status: {result.case_details.status}")
        else:
            print(f"❌ {result.message}")

def example_2_check_listing():
    print("\n" + "="*70)
    print("EXAMPLE 2: Check Case Listing")
    print("="*70 + "\n")
    with ECourtsScraper(headless=False) as scraper:
        cnr = "MHAU019999992015"
        result = scraper.search_by_cnr(cnr, check_listing=True)
        if result.success:
            print("✅ Case found!")
            if result.is_listed:
                print("📅 Case IS listed!")
                if result.listing_info:
                    print(f"Serial Number: {result.listing_info.serial_number}")
                    print(f"Court: {result.listing_info.court_name}")
            else:
                print("📅 Case is NOT listed today or tomorrow")

def example_3_save_results():
    print("\n" + "="*70)
    print("EXAMPLE 3: Save Results to JSON")
    print("="*70 + "\n")
    with ECourtsScraper(headless=False) as scraper:
        cnr = "MHAU019999992015"
        result = scraper.search_by_cnr(cnr, check_listing=True)
        if result.success:
            filename = f"case_{cnr}"
            filepath = save_to_json(result.to_dict(), filename)
            print(f"✅ Results saved to: {filepath}")

def example_4_multiple_searches():
    print("\n" + "="*70)
    print("EXAMPLE 4: Multiple Case Searches")
    print("="*70 + "\n")
    cnr_list = [
        "MHAU019999992015",
        "DLHC010123452020",
    ]
    with ECourtsScraper(headless=False) as scraper:
        results = []
        for cnr in cnr_list:
            print(f"\nSearching for: {cnr}")
            result = scraper.search_by_cnr(cnr, check_listing=False)
            results.append(result)
            if result.success:
                print(f"  ✅ Found")
            else:
                print(f"  ❌ Not found")
        print("\n" + "-"*70)
        print(f"Total searched: {len(cnr_list)}")
        print(f"Found: {sum(1 for r in results if r.success)}")
        print(f"Not found: {sum(1 for r in results if not r.success)}")

def example_5_error_handling():
    print("\n" + "="*70)
    print("EXAMPLE 5: Error Handling")
    print("="*70 + "\n")
    try:
        with ECourtsScraper(headless=False) as scraper:
            cnr = "INVALID_CNR"
            result = scraper.search_by_cnr(cnr, check_listing=False)
            if result.success:
                print("✅ Success")
            else:
                print(f"❌ Failed: {result.message}")
                if result.error:
                    print(f"Error details: {result.error}")
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("But the program didn't crash!")

def example_6_custom_configuration():
    print("\n" + "="*70)
    print("EXAMPLE 6: Custom Configuration")
    print("="*70 + "\n")
    scraper = ECourtsScraper(headless=False)
    try:
        cnr = "MHAU019999992015"
        result = scraper.search_by_cnr(cnr, check_listing=False)
        print(f"Success: {result.success}")
        print(f"Message: {result.message}")
    finally:
        scraper.close()

def main():
    print_banner()
    print("\n📚 eCourts Scraper - Usage Examples\n")
    print("Choose an example to run:")
    print("  1. Basic CNR search")
    print("  2. Check case listing")
    print("  3. Save results to JSON")
    print("  4. Multiple case searches")
    print("  5. Error handling")
    print("  6. Custom configuration")
    print("  0. Exit")
    while True:
        try:
            choice = input("\nEnter choice (0-6): ").strip()
            if choice == "0":
                print("\nGoodbye! 👋")
                break
            elif choice == "1":
                example_1_basic_search()
            elif choice == "2":
                example_2_check_listing()
            elif choice == "3":
                example_3_save_results()
            elif choice == "4":
                example_4_multiple_searches()
            elif choice == "5":
                example_5_error_handling()
            elif choice == "6":
                example_6_custom_configuration()
            else:
                print("Invalid choice. Please enter 0-6.")
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break

if __name__ == "__main__":
    main()
