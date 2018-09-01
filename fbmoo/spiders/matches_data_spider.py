import scrapy
from fbmoo.settings import SCRAPED_LINKS


class MatchesDataSpider(scrapy.Spider):
    name = "matches"

    start_urls = ["http://football-data.co.uk/data.php"]

    def parse(self, response):
        league_sets_names = response.xpath('//p[@align="left"]')
        league_sets = response.xpath('//p[@align="left"]/following-sibling::table')
        league_cells = []
        league_links = []
        print(league_sets)
        for index, league_set in enumerate(league_sets):
            print('League set:', league_sets_names[index].css('b::text').extract_first())
            print(league_set.extract())
            league_cells = league_set.css('a::attr(href)').extract()
            league_links += league_cells

        print(league_links)

        with open(SCRAPED_LINKS + 'league_links', 'w') as league_file:
            for league_link in league_links:
                league_link = 'http://football-data.co.uk/' + league_link
                league_file.write(league_link + "\n")
