import os
import errno
from pathlib import Path
import json

import scrapy
from fbmoo.settings import DATA_PATH
from fbmoo.settings import SCRAPED_LINKS


import wget


class MatchesDataSpider(scrapy.Spider):
    name = "league_data"

    scrape_root = "http://football-data.co.uk/"

    def start_requests(self):
        start_urls = []
        with open(SCRAPED_LINKS + 'league_links', 'r') as links:
            for cnt, line in enumerate(links):
                url = json.loads(line)
                start_urls.append(url['link'])

        print(start_urls)
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # seasons = response.xpath('//p[@align="justify"][last()]')
        country = response.xpath('//p[@align="left"]/b[contains(., "Data Files: ")]/text()').extract_first()
        country = country.split(": ")[1].lower()
        print("Country:", country)

        store_path = DATA_PATH + country
        try:
            os.makedirs(store_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        seasons = response.xpath("//a[preceding-sibling::i[1][contains(., 'Season ')]]")

        for season in seasons:
            url = season.xpath("@href").extract_first()
            url_segs = url.split("/")
            if len(url_segs) != 3:
                continue
            download_link = self.scrape_root + url
            title = season.xpath("text()").extract_first()

            print("\n-------------------")
            print("Season:", url_segs[1])
            print("File name:", title)
            print("Download link:", download_link)
            print("-------------------")

            season_path = store_path + "/" + url_segs[1]
            try:
                os.makedirs(season_path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            filename = season_path + "/" + title.lower() + '.csv'
            if not Path(filename).exists():
                wget.download(download_link, filename)

