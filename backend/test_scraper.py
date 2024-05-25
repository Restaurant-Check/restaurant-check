from scraper.scrape import scraper


def test_scraper():
    url = "https://www.mailisneufahrn.de/"
    result, links = scraper(url)
    print("result ", result)
    print("links ", links)


if __name__ == "__main__":
    test_scraper()
