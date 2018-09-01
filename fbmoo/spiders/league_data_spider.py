import scrapy
from fbmoo.settings import SCRAPED_LINKS


class MatchesDataSpider(scrapy.Spider):
    name = "league_data"

    start_urls = ["http://football-data.co.uk/englandm.php"]

    def parse(self, response):
        seasons = response.xpath('//p[@align="justify"][last()]')
        seasons = response.xpath("//a[preceding-sibling::i[1][contains(., 'Season ')]]")
        print(seasons)
        # for season in seasons:
        #     season_data = season.xpath('./afollowing-sibling::a[@href][1]')
        #     print(season_data)
