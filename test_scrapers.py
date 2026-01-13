"""
Test script for debugging scrapers
Run this to test each scraper individually and see detailed output
"""
import sys
from scrapers import IndeedDeScraper, StepStoneScraper, XingJobsScraper
import json


def test_scraper(scraper_class, name, keywords="software engineer", location="Berlin", max_pages=3):
    """Test a single scraper"""
    print(f"\n{'='*60}")
    print(f"Testing {name}")
    print(f"{'='*60}")
    print(f"Keywords: {keywords}")
    print(f"Location: {location}")
    print(f"Max Pages: {max_pages}\n")

    try:
        scraper = scraper_class()
        jobs, debug_info = scraper.scrape(keywords, location, max_pages=max_pages)

        print(f"Status Code: {debug_info.get('status_code', 'N/A')}")
        print(f"URL: {debug_info.get('url', 'N/A')}")
        print(f"Pages Scraped: {debug_info.get('pages_scraped', 0)}")
        print(f"Jobs Found: {len(jobs)}")

        if debug_info.get('error'):
            print(f"Error: {debug_info.get('error')}")

        if debug_info.get('selectors_tried'):
            print(f"Selectors Tried: {', '.join(debug_info.get('selectors_tried', []))}")

        if len(jobs) > 0:
            print(f"\nFirst 3 jobs found:")
            for i, job in enumerate(jobs[:3], 1):
                print(f"\n--- Job {i} ---")
                print(json.dumps(job, indent=2, ensure_ascii=False))
        else:
            print("\nNo jobs found!")
            if debug_info.get('html_sample'):
                print("\nHTML Sample (first 500 chars):")
                print(debug_info.get('html_sample')[:500])

        return len(jobs) > 0

    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all scraper tests"""
    print("\n" + "="*60)
    print("JOB SCRAPER TESTING SUITE")
    print("="*60)

    # Get search parameters
    if len(sys.argv) > 1:
        keywords = sys.argv[1]
    else:
        keywords = input("Enter job keywords (default: 'software engineer'): ").strip() or "software engineer"

    if len(sys.argv) > 2:
        location = sys.argv[2]
    else:
        location = input("Enter location (default: 'Berlin'): ").strip() or "Berlin"

    results = {}

    # Test each scraper
    results['Indeed.de'] = test_scraper(IndeedDeScraper, "Indeed.de", keywords, location)
    results['StepStone.de'] = test_scraper(StepStoneScraper, "StepStone.de", keywords, location)
    results['XING Jobs'] = test_scraper(XingJobsScraper, "XING Jobs", keywords, location)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for portal, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{portal}: {status}")

    total_success = sum(results.values())
    print(f"\n{total_success}/{len(results)} scrapers working")

    if total_success == 0:
        print("\n⚠️  No scrapers are working. This could be due to:")
        print("   - Internet connection issues")
        print("   - Job portals blocking automated requests")
        print("   - Changes in portal HTML structure")
        print("   - Geographic restrictions (some portals may be region-locked)")
        print("\n💡 Try using 'Test Mode' in the Streamlit app to see sample data")


if __name__ == "__main__":
    main()
