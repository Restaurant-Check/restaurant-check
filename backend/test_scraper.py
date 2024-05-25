from scraper.scrape import scraper


def test_scraper():
    url = "https://www.mailisneufahrn.de/"
    result = scraper(url)
    print("result ", result)


if __name__ == "__main__":
    test_scraper()
