import subprocess

def scraper(url: str, output_file: str) -> bool:
    """
    This function will run the Scrapy spider to scrape the menu data from the given URL and save the output to the specified file.
    - url: str - The URL of the restaurant's homepage to scrape.
    - output_file: str - The file name of the output file.
    """
    # Run the Scrapy spider with the given URL and save the output to the specified file
    try:
        process = subprocess.Popen(
            ["scrapy", "crawl", "menu_spider", "-a", f"start_url={url}", "-O", "../"+output_file],
            cwd="backend/scraper",
        )
        process.wait()
        return True
    except Exception as e:
        print(f"Error running scraper: {e}")
        return False
