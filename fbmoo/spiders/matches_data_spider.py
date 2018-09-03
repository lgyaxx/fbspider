from pathlib import Path
import os

import scrapy
from fbmoo.settings import SCRAPED_LINKS


class MatchesDataSpider(scrapy.Spider):
    name = "matches"

    custom_settings = {
        'FEED_URI': SCRAPED_LINKS + 'league_links',
    }

    def start_requests(self):
        # empty feed file first
        with open(self.custom_settings['FEED_URI'], 'w') as feed:
            pass

        url = "http://football-data.co.uk/data.php"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        league_sets_names = response.xpath('//p[@align="left"]')
        league_sets = response.xpath('//p[@align="left"]/following-sibling::table')
        league_links = []
        print(league_sets)
        for index, league_set in enumerate(league_sets):
            print('League set:', league_sets_names[index].css('b::text').extract_first())
            print(league_set.extract())
            league_cells = league_set.css('a::attr(href)').extract()
            league_links += league_cells

        print(league_links)

        for league_link in league_links:
            yield {
                'link': 'http://football-data.co.uk/' + league_link
            }
