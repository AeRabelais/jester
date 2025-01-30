import pytest
from jester.scrapers.linkedin import LinkedinScraper

TEST_URL: str = "https://www.linkedin.com/hiring/jobs/4000865419/applicants/23262215106/detail/"

@pytest.mark.unit
def test_linkedin():

    scraper = LinkedinScraper(TEST_URL)
    results = scraper.scrape()

    print(results)

    assert False