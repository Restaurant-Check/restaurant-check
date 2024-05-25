rm examples/mailineufahrn.json
rm examples/aetna_neufahrn.json
rm examples/levespe.json

scrapy crawl menu_spider -a start_url="https://www.mailisneufahrn.de/" -O examples/mailineufahrn.json   
scrapy crawl menu_spider -a start_url="https://www.aetna-ristorante.de/" -O examples/aetna_neufahrn.json
scrapy crawl menu_spider -a start_url="http://www.levespe.de/" -O examples/levespe.json