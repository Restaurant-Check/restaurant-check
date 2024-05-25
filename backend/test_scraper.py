from scraper.scrape import scraper

def test_scraper():
    url = "https://www.mailisneufahrn.de/"
    output_file = "menu.json"
    result = scraper(url, output_file)
    print(result)
    
if __name__ == "__main__":
    test_scraper()